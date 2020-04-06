import logging
import torch
import torch.optim as optim
import torch.nn as nn
import torchvision
from torch.autograd import Variable
from UrbanModels.SI_AGAN.model import Generator, Discriminator, FeatureExtractor
from UrbanModels.SI_AGAN.utils import MyDataset
import warnings
from UrbanUtils.IO import ConfigReader, FileUtils

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# filename='model.log',filemode='a')
logger = logging.getLogger(__name__)


def run():
    # ----- Config -----#
    config = ConfigReader.GetModelConfig("SI-AGAN")
    GENERATOR_LR = config["generator_lr"]  # 0.001
    DISCRIMINATOR_LR = config["discriminator_lr"]  # 0.001
    PRE_TRAIN_EPOCH = config["pre_train_epoch"]  # 2
    TRAIN_EPOCH = config["train_epoch"]  # 10
    BATCH_SIZE = config["batch_size"]  # 5
    MODEL_OUT_PATH = config["model_out_path"]  # "../Temp/Generator.pth"
    UP_SAMPLE = 1
    IS_CUDA = False
    log_path = config["log_path"]

    # ----- Variable -----#
    dataset = MyDataset()
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    generator = Generator(16, UP_SAMPLE)
    discriminator = Discriminator()
    # vgg19 = torch.load("D:/Dataset/Model/vgg19-dcbb9e9d.pth")
    # feature_extractor = FeatureExtractor(vgg19)
    feature_extractor = FeatureExtractor(torchvision.models.vgg19(pretrained=True))

    content_criterion = nn.MSELoss()
    adversarial_criterion = nn.BCELoss()

    if IS_CUDA:
        generator.cuda()
        discriminator.cuda()
        feature_extractor.cuda()
        content_criterion.cuda()
        adversarial_criterion.cuda()

    # ----- Pre Train Generator -----#
    optim_generator = optim.Adam(generator.parameters(), lr=GENERATOR_LR)
    optim_discriminator = optim.Adam(discriminator.parameters(), lr=DISCRIMINATOR_LR)

    logger.info('Generator pre-training')
    record_loss = 0.0
    for epoch in range(PRE_TRAIN_EPOCH):
        for i, data in enumerate(dataloader):
            low_res, high_res_real = data
            low_res = low_res.permute(0, 3, 1, 2).float()
            high_res_real = high_res_real.permute(0, 3, 1, 2).float()

            # Generate real and fake inputs
            if IS_CUDA:
                high_res_real = Variable(high_res_real.cuda())
                high_res_fake = generator(Variable(low_res).cuda())
            else:
                high_res_real = Variable(high_res_real)
                high_res_fake = generator(Variable(low_res))

            generator.zero_grad()

            generator_content_loss = content_criterion(high_res_fake, high_res_real)
            generator_content_loss.backward()
            record_loss += generator_content_loss.item()

            optim_generator.step()

            FileUtils.WriteFile("Pre,{}\n".format((epoch*len(dataloader) + i + 1) /
                                                          PRE_TRAIN_EPOCH*len(dataloader)), log_path, "a")
            if i % 10 == 0:
                logger.info("[{}/{}][{}/{}] Pre Train Loss: {}".format(
                    epoch + 1, PRE_TRAIN_EPOCH,
                    i + 1, len(dataloader),
                    record_loss / 10.0
                ))
                record_loss = 0.0

    # ----- Train -----#
    optim_generator = optim.Adam(generator.parameters(), lr=GENERATOR_LR * 0.1)
    optim_discriminator = optim.Adam(discriminator.parameters(), lr=DISCRIMINATOR_LR * 0.1)

    logger.info("Begin Training...")
    FileUtils.WriteFile("Pre,Fin\n", log_path, "a")
    for epoch in range(TRAIN_EPOCH):
        for i, data in enumerate(dataloader):
            low_res, high_res_real = data
            low_res = low_res.permute(0, 3, 1, 2).float()
            high_res_real = high_res_real.permute(0, 3, 1, 2).float()
            # Generate real and fake inputs
            if IS_CUDA:
                high_res_real = Variable(high_res_real.cuda())
                high_res_fake = generator(Variable(low_res).cuda())
                target_real = Variable(torch.rand(high_res_real.shape[0], 1) * 0.5 + 0.7).cuda()
                target_fake = Variable(torch.rand(high_res_fake.shape[0], 1) * 0.3).cuda()
                ones_const = Variable(torch.ones(high_res_fake.shape[0], 1)).cuda()
            else:
                high_res_real = Variable(high_res_real)
                high_res_fake = generator(Variable(low_res))
                target_real = Variable(torch.rand(high_res_real.shape[0], 1) * 0.5 + 0.7)
                target_fake = Variable(torch.rand(high_res_fake.shape[0], 1) * 0.3)
                ones_const = Variable(torch.ones(high_res_fake.shape[0], 1))

            ######### Train discriminator #########
            discriminator.zero_grad()
            discriminator_loss = adversarial_criterion(discriminator(high_res_real), target_real) + \
                                 adversarial_criterion(discriminator(Variable(high_res_fake.data)), target_fake)

            discriminator_loss.backward()
            optim_discriminator.step()

            ######### Train generator #########
            generator.zero_grad()

            real_features = Variable(feature_extractor(high_res_real).data)
            fake_features = feature_extractor(high_res_fake)

            generator_content_loss = content_criterion(high_res_fake, high_res_real) + 0.006 * content_criterion(
                fake_features, real_features)
            generator_adversarial_loss = adversarial_criterion(discriminator(high_res_fake), ones_const)

            generator_total_loss = generator_content_loss + 1e-5 * generator_adversarial_loss

            generator_total_loss.backward()
            optim_generator.step()

            ######### Status and display #########
            FileUtils.WriteFile(
                "Train,{}\n".format((i + 1 + epoch * len(dataloader)) / TRAIN_EPOCH*len(dataloader)),
                log_path, "a")
            logger.info('[{}/{}][{}/{}] Discriminator_Loss: {} Generator_Loss (Content/Advers/Total): {} {} {}'.format(
                epoch + 1, TRAIN_EPOCH,
                i + 1, len(dataloader),
                discriminator_loss.item(),
                generator_content_loss.item(), generator_adversarial_loss.item(), generator_total_loss.item()))

    torch.save(generator, MODEL_OUT_PATH)
