<template>
  <el-container class="full-height">
    <el-tabs type="border-card" tab-position="left" class="full-height-width">
      <el-tab-pane label="Linear">Linear</el-tab-pane>
      <el-tab-pane label="SI-AGAN" class="full-height">
        <!-- SI-AGAN Steps-->
        <el-steps :active="GAN.active" simple>
          <el-step title="Start" icon="el-icon-help"></el-step>
          <el-step title="Configure" icon="el-icon-setting"></el-step>
          <el-step title="Train" icon="el-icon-upload"></el-step>
          <el-step title="Inference" icon="el-icon-star-off"></el-step>
        </el-steps>
        <!-- SI-AGAN Start-->
        <div class="full-height-width" :style="getHeightStyle" v-show="GAN.seen==1">
          <el-row class="center-div">
            <el-button type="primary" style="margin-right: 20px" @click="handle_upload_model()">Upload Model</el-button>
            <el-button type="primary" @click="handle_new_model()">New Model</el-button>
          </el-row>
        </div>
        <!-- SI-AGAN Config-->
        <div class="full-height-width" :style="getHeightStyle" v-show="GAN.seen==2">
          <el-row type="flex" justify="space-between" style="margin-top: 30px">
            <el-col :span="6">
              <el-form label-position="left" label-width="120px" :model="GAN.params">
                <el-form-item label="Learning Rate">
                  <el-input v-model="GAN.params.lr"></el-input>
                </el-form-item>
                <el-form-item label="MS-Radius">
                  <el-input v-model="GAN.params.ms_radius"></el-input>
                </el-form-item>
                <el-form-item label="Worker Number">
                  <el-input v-model="GAN.params.worker_num"></el-input>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
          <div class="next-button-div">
            <el-button type="primary" @click="handle_train_model()">Train</el-button>
          </div>
        </div>
        <!-- SI-AGAN Train-->
        <div class="full-height-width" :style="getHeightStyle" v-show="GAN.seen==3">
          <el-row class="center-div" style="width: 80%">
            <el-progress :text-inside="true" :stroke-width="26" :percentage="GAN.progress" :color="colors"></el-progress>
          </el-row>
        </div>
        <!-- SI-AGAN Inference-->
        <div class="full-height-width" :style="getHeightStyle" v-show="GAN.seen==4">
          <el-row class="center-div" style="width: 60%">
            <el-row type="flex" justify="center">
              <el-col :span="6">
                <el-input placeholder="Input Position" v-model="GAN.inference.input" clearable style="margin-right: 20px">
                </el-input>
              </el-col>
              <el-col :span="4">
                <el-button icon="el-icon-right" circle></el-button>
              </el-col>
              <el-col :span="6">
                <el-input placeholder="Predicted Value" v-model="GAN.inference.output" :disabled="true">
                </el-input>
              </el-col>
            </el-row>
            <br />
            <br />
            <el-row>
              <el-button type="primary" round>Generate HeatMap</el-button>
            </el-row>
            <br />
            <el-row>
              <el-button type="primary" round>&nbsp&nbspDownload Model &nbsp&nbsp</el-button>
            </el-row>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>
  </el-container>
</template>
<script>
export default {
  name: 'Interpolation',
  props: ["attribute", "time_step"],
  data() {
    return {
      colors: [
        { color: '#f56c6c', percentage: 20 },
        { color: '#e6a23c', percentage: 40 },
        { color: '#5cb87a', percentage: 60 },
        { color: '#1989fa', percentage: 80 },
        { color: '#6f7ad3', percentage: 100 }
      ],
      GAN: {
        active: 0,
        seen: 1,
        params: {
          lr: 0.001,
          ms_radius: 1,
          worker_num: 1,
        },
        inference: {
          input: null,
          output: null
        },
        progress: 0,
      }
    }
  },
  watch: {
    attribute() {

    },
    time_step() {

    }
  },
  mounted: function() {

  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.time_step == null;
    },
    getData() {
      /*var promise = ;
      promise.then((response) => {
        this.val = response.data;
      })*/
    },
    handle_upload_model() {
      if (this.is_not_prepared()) {
        this.$message.warning("Data is not prepared. Refresh!");
        return;
      }
      console.log("upload model");
    },
    handle_new_model() {
      if (this.is_not_prepared()) {
        this.$message.warning("Data is not prepared. Refresh!");
        return;
      }
      this.GAN.active = 1;
      this.GAN.seen = 2;
    },
    async handle_train_model() {
      var promise = this.TrainModel("SI-AGAN", this.global_.data_name, this.attribute);
      await promise.then((response) => {
        this.GAN.active = 2;
        this.GAN.seen = 3;
        var start_time_ms = new Date().getTime();
        var limit = 2 * 60 * 1000;

        function loopGetProgress(start, limit, self) {
          var pms = self.GetTrainProgress("SI-AGAN");
          pms.then((response) => {
            var progress = response.data;
            if (self.GAN.progress > progress) {
              console.log("backend progress smaller than current. check it.");
            } else {
              self.GAN.progress = progress;
            }
            if (new Date().getTime() - start < limit && self.GAN.progress < 100) {
              self.sleep(150);
              loopGetProgress(start, limit, self);
            } else if (self.GAN.progress < 100) {
              self.$message.warning("Failed to train. Time Out!");
            } else {
              self.sleep(200);
              self.GAN.active = 3;
              self.GAN.seen = 4;
            }
          })
        }
        loopGetProgress(start_time_ms, limit, this);
      }).catch((error) => {
        this.$message.error("Failed to request backend for training.");
        console.log(error);
      })
    }
  },
  computed: {
    getHeightStyle: function() {
      var height = Math.ceil(window.screen.height * 0.4);
      return {
        "height": height + "px",
      }
    }
  }
}

</script>
<style scoped>
.full-height {
  height: 100%;
}

.full-width {
  width: 100%;
}

.full-height-width {
  height: 100%;
  width: 100%;
}

.center-div {
  position: relative;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
  text-align: center
}

.next-button-div {
  text-align: center;
  margin-top: 40px;
}

</style>
<style>
</style>
