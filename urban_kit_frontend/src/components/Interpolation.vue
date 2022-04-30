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
            <el-upload ref="upload" name="SI-AGAN" :action="upload_api" :on-success="handleSuccess" :auto-upload="true">
              <el-button slot="trigger" type="primary" style="margin-right: 20px">Upload Model</el-button>
              <el-button type="primary" @click="handle_new_model()"> New Model </el-button>
            </el-upload>
            <!--<el-button type="primary" style="margin-right: 20px" @click="handle_upload_model()">Upload Model</el-button>-->
          </el-row>
        </div>
        <!-- SI-AGAN Config-->
        <div class="full-height-width" :style="getHeightStyle" v-show="GAN.seen==2">
          <el-row type="flex" justify="space-between" style="margin-top: 30px">
            <el-col :span="7">
              <el-form label-position="left" label-width="80px" :model="GAN.params">
                <el-form-item label="Grid Size">
                  <el-input v-model="GAN.params.grid_size"></el-input>
                </el-form-item>
                <el-form-item label="Radius">
                  <el-input v-model="GAN.params.ms_radius"></el-input>
                </el-form-item>
                <el-form-item label="Bandwith">
                  <el-input v-model="GAN.params.ms_bandwith"></el-input>
                </el-form-item>
              </el-form>
            </el-col>
            <el-col :span="8">
              <el-form label-position="left" label-width="120px" :model="GAN.params">
                <el-form-item label="Generator LR">
                  <el-input v-model="GAN.params.generator_lr"></el-input>
                </el-form-item>
                <el-form-item label="Discriminator LR">
                  <el-input v-model="GAN.params.discriminator_lr"></el-input>
                </el-form-item>
                <el-form-item label="Train Epoch">
                  <el-input v-model="GAN.params.train_epoch"></el-input>
                </el-form-item>
              </el-form>
            </el-col>
            <el-col :span="7">
              <el-form label-position="left" label-width="120px" :model="GAN.params">
                <el-form-item label="Batch Size">
                  <el-input v-model="GAN.params.batch_size"></el-input>
                </el-form-item>
                <el-form-item label="Pre Train Epoch">
                  <el-input v-model="GAN.params.pre_train_epoch"></el-input>
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
                <el-input placeholder="Long,Lat" @ckick="this.si_agan_input_change" v-model="GAN.inference.input" clearable style="margin-right: 20px">
                </el-input>
              </el-col>
              <el-col :span="4">
                <el-button icon="el-icon-right" @click="si_agan_predict_one()" circle></el-button>
              </el-col>
              <el-col :span="6">
                <el-input placeholder="Predicted Value" v-model="GAN.inference.output" :disabled="true">
                </el-input>
              </el-col>
            </el-row>
            <br />
            <br />
            <el-row>
              <el-button type="primary" round @click="si_agan_predict_many()">Generate HeatMap</el-button>
            </el-row>
            <br />
            <el-row>
              <el-button type="primary" @click="download_agan_model()" round>&nbsp&nbspDownload Model &nbsp&nbsp</el-button>
            </el-row>
            <br />
            <el-row>
              <el-button type="warning" @click="agan_reset()" round>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ReSet &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</el-button>
            </el-row>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>
    <el-dialog title="Heat Map Distribution" :visible.sync="heat_visible" width="60%" center class="my_dialog" @opened="opened">
      <div :style="getDialogStyle">
        <div ref="heat_map_chart" style="width: 100%; height: 100%">
        </div>
      </div>
    </el-dialog>
  </el-container>
</template>
<script>
export default {
  name: 'Interpolation',
  props: ["attribute", "time_step"],
  data() {
    return {
      upload_api: "http://" + this.config_.backend + this.global_.apis["upload_model"],
      min_value: -1,
      max_value: 1,
      heatChart: null,
      heat_data: [],
      geos: [],
      heat_visible: false,
      lngExtent: [39.5, 40.6],
      latExtent: [115.9, 116.8],
      cellSizeCoord: [0, 0],
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
          generator_lr: 0.001,
          discriminator_lr: 0.001,
          ms_radius: 25,
          ms_bandwith: 20,
          grid_size: 10,
          pre_train_epoch: 2,
          train_epoch: 10,
          batch_size: 20,
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
    this.update_cell_size();
  },
  methods: {
    opened() {
      this.draw_heat(this.heat_data)
    },
    update_cell_size() {
      this.cellSizeCoord = JSON.parse(JSON.stringify([
        (this.lngExtent[1] - this.lngExtent[0]) / 10,
        (this.latExtent[1] - this.latExtent[0]) / 10
      ]));
    },
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.time_step == null;
    },
    handleSuccess(response, file, fileList) {
      this.sleep(200);
      this.GAN.active = 3;
      this.GAN.seen = 4;
    },
    handle_upload_model() {
      if (this.is_not_prepared()) {
        this.$message.warning("Data is not prepared. Refresh!");
        return;
      }
    },
    handle_new_model() {
      if (this.is_not_prepared()) {
        this.$message.warning("Data is not prepared. Refresh!");
        return;
      }
      this.GAN.active = 1;
      this.GAN.seen = 2;
    },
    download_agan_model() {
      this.DownloadModel("SI-AGAN");
    },
    agan_reset() {
      this.GAN.active = 0;
      this.GAN.seen = 1;
      this.RemoveLog("SI-AGAN")
    },
    async handle_train_model() {
      var promise = this.SetModelParameter("SI-AGAN", this.GAN.params);
      await promise.then((response) => {
        console.log("Set Param success");
      })
      promise = this.TrainModel("SI-AGAN", this.global_.data_name, this.attribute);
      this.GAN.active = 2;
      this.GAN.seen = 3;
      var start_time_ms = new Date().getTime();
      var limit = 10 * 60 * 1000;

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
            self.sleep(1500);
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
    },
    si_agan_predict_one() {
      var input_s = this.GAN.inference.input.split(",");
      if (input_s.length != 2) {
        this.$message.error("your input is wrong.");
        return;
      }
      var long = input_s[0].trim();
      var lat = input_s[1].trim();
      var promise = this.PredictOne(long, lat, "SI-AGAN", this.global_.data_name, this.time_step, this.attribute);
      promise.then((response) => {
        this.GAN.inference.output = response.data;
      }).catch((error) => {
        this.$message.error("predict error!");
      })
    },
    si_agan_input_change() {
      this.GAN.inference.output = null;
    },
    si_agan_predict_many() {
      const loading = this.$loading({
        lock: true,
        text: 'loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      var promise = this.PredictMany("SI-AGAN", this.global_.data_name, this.time_step, this.attribute);
      promise.then((response) => {
        this.latExtent = JSON.parse(JSON.stringify(response.data.lat));
        this.lngExtent = JSON.parse(JSON.stringify(response.data.lng));
        this.heat_data = JSON.parse(JSON.stringify(response.data.value));
        this.min_value = this.heat_data[0].value[2];
        this.max_value = this.heat_data[0].value[2];
        for (var i = 0; i < this.heat_data.length; ++i) {
          if (this.heat_data[i].value[2] < this.min_value) this.min_value = this.heat_data[i].value[2];
          if (this.heat_data[i].value[2] > this.max_value) this.max_value = this.heat_data[i].value[2];
        }
        this.geos = JSON.parse(JSON.stringify(response.data.geo));
        this.update_cell_size();
        this.heat_visible = true;
        setTimeout(() => {
          loading.close()
        }, 1000);
      })
    },
    draw_heat() {
      var option = {
        visualMap: {
          show: false,
          min: this.min_value,
          max: this.max_value,
          splitNumber: 5,
          inRange: {
            color: ['#d94e5d', '#eac736', '#50a3ba'].reverse()
          }
        },
        bmap: {
          center: this.getCenter(this.geos),
          zoom: 10,
          roam: true,
          mapStyle: this.global_.plainMapStyle,
        },
        series: [{
          type: 'heatmap',
          pointSize: 25,
          blurSize: 25,
          coordinateSystem: 'bmap',
          data: JSON.parse(JSON.stringify(this.heat_data)),
        }],
      };
      this.heatChart = this.$echarts.init(this.$refs.heat_map_chart);
      this.heatChart.setOption(option);
    },
    getCenter(data) {
      var geos = data;
      var ret = [0, 0];
      for (var i = 0; i < geos.length; i++) {
        ret[0] += geos[i][0];
        ret[1] += geos[i][1];
      }
      ret[0] /= geos.length;
      ret[1] /= geos.length;
      return ret;
    }
  },
  computed: {
    getHeightStyle: function() {
      var height = Math.ceil(window.screen.height * 0.4);
      return {
        "height": height + "px",
      }
    },
    getDialogStyle: function() {
      var height = Math.ceil(window.screen.height * 0.6);
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
