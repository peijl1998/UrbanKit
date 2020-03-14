<template>
  <el-container class="is-vertical full-height">
    <!-- Main UI -->
    <el-row type="flex" justify="space-around" style="height: 70%">
      <el-col :span="6" class="row">
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Tool Box -->
            <div class="panel scrollbar full-height">
              <div class="logo">
                <img src="../../static/logo.png" style="width: 50%; height: 100%" />
              </div>
              <el-collapse accordion class="full-height">
                <el-collapse-item>
                  <template slot="title">
                    <i class="el-icon-map-location"></i>
                    &nbspMap Controller
                  </template>
                  <el-row class="tool-box-row" type="flex" justify="space-between">
                    <el-col :span="6" class="tool-box-col">
                      <div>Time Step: </div>
                    </el-col>
                    <el-col :span="18" class="tool-box-col">
                      <el-slider class="my-slider" show-input v-model="time_step" :step="1" style="width: 100%;">
                      </el-slider>
                    </el-col>
                  </el-row>
                  <el-row class="tool-box-row" type="flex" justify="space-between">
                    <el-col :span="6" class="tool-box-col" style="padding-top: 4px">
                      <div>Attribute: </div>
                    </el-col>
                    <el-col :span="18" class="tool-box-col">
                      <el-select v-model="map_attribute" placeholder="Select..." class="trend-select map-attribute">
                        <el-option v-for="item in trend_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-col>
                  </el-row>
                  <el-row class="tool-box-row" type="flex" justify="space-between">
                    <el-col :span="6" class="tool-box-col">
                      <div>Dot Shape: </div>
                    </el-col>
                    <el-col :span="18" class="tool-box-col">
                      <el-radio-group v-model="dot_shape" class="dot-shape">
                        <el-radio label="circle">Circle</el-radio>
                        <el-radio label="diamond">Diamond</el-radio>
                        <el-radio label="triangle">Tri</el-radio>
                      </el-radio-group>
                    </el-col>
                  </el-row>
                  <el-row class="tool-box-row" type="flex" justify="space-between">
                    <el-col :span="6" class="tool-box-col" style="padding-top: 2px">
                      <div>Dot Size: </div>
                    </el-col>
                    <el-col :span="18" class="tool-box-col">
                      <el-input-number class="dot-size" v-model="dot_size" controls-position="right" :min="5" :max="30"></el-input-number>
                    </el-col>
                  </el-row>
                </el-collapse-item>
                <el-collapse-item>
                  <template slot="title">
                    <i class="el-icon-data-analysis"></i>
                    &nbspCustomed Linechart
                  </template>
                  <el-row class="tool-box-row" type="flex" justify="space-between">
                    <el-col :span="6" class="tool-box-col" style="padding-top: 4px">
                      <div>Attributes: </div>
                    </el-col>
                    <el-col :span="18" class="tool-box-col">
                      <el-select v-model="trend_value" multiple collapse-tags placeholder="Select..." class="trend-select">
                        <el-option v-for="item in trend_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-col>
                  </el-row>
                </el-collapse-item>
                <el-collapse-item>
                  <template slot="title">
                    <i class="el-icon-data-line"></i>
                    &nbspCustomed Histogram
                  </template>
                  <el-row class="tool-box-row" type="flex" justify="space-between">
                    <el-col :span="6" class="tool-box-col">
                      <div>Time Step: </div>
                    </el-col>
                    <el-col :span="18" class="tool-box-col">
                      <el-slider class="my-slider" show-input v-model="hist_time_step" :step="1" style="width: 100%;">
                      </el-slider>
                    </el-col>
                  </el-row>
                  <el-row class="tool-box-row" type="flex" justify="space-between">
                    <el-col :span="6" class="tool-box-col" style="padding-top: 4px">
                      <div>Attribute: </div>
                    </el-col>
                    <el-col :span="18" class="tool-box-col">
                      <el-select v-model="hist_attribute" placeholder="Select..." class="trend-select map-attribute">
                        <el-option v-for="item in trend_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-col>
                  </el-row>
                </el-collapse-item>
                <el-collapse-item>
                  <template slot="title">
                    <i class="el-icon-star-on"></i>
                    &nbspAdvanced Functions
                  </template>
                  <ul class="advanced-func">
                    <li>
                      <el-button type="text" @click="interpolation_visible = true">Spatial Interpolation</el-button>
                    </li>
                    <li>
                      <el-button type="text" @click="prediction_visible = true">Time Series Prediction</el-button>
                    </li>
                    <li>
                      <el-button type="text" @click="detection_visible = true">Time Series Anomaly Detection</el-button>
                    </li>
                    <li>
                      <el-button type="text" @click="heat_visible = true">Heat Map</el-button>
                    </li>
                    <li>
                      <el-button type="text" @click="correlation_visible = true">Correlation Analysis</el-button>
                    </li>
                  </ul>
                </el-collapse-item>
              </el-collapse>
            </div>
          </el-col>
        </el-row>
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Other Plots -->
            <div class="panel" style="height:100%;text-align:left">
              <Top :attribute="map_attribute" :time_step="time_step"></Top>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="12">
        <el-row type="flex" justify="space-around" style="height: 15%">
          <el-col :span="6" class="row">
            <!-- Value1 -->
            <div class="panel">
              <Value index="Average" color="#3B8AC3FF"></Value>
            </div>
          </el-col>
          <el-col :span="6" class="row">
            <!-- Value2 -->
            <div class="panel">
              <Value index="Max" color="#C97035FF"></Value>
            </div>
          </el-col>
          <el-col :span="6" class="row">
            <!-- Value3 -->
            <div class="panel">
              <Value index="Min" color="#FF7F7FFF"></Value>
            </div>
          </el-col>
          <el-col :span="6" class="row">
            <!-- Value4 -->
            <div class="panel">
              <Value index="Median" color="#8C5DA1FF"></Value>
            </div>
          </el-col>
        </el-row>
        <el-row type="flex" justify="space-around" style="height: 85%">
          <el-col :span="24" class="row">
            <!-- Map -->
            <div class="panel" style="height:100%">
              <Map :time_step="time_step" :dot_size="dot_size" :dot_shape="dot_shape" :attribute="map_attribute"></Map>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="6">
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Histogram -->
            <div class="panel" style="height:100%">
              <Hist :attribute="map_attribute" :time_step="time_step"></Hist>
            </div>
          </el-col>
        </el-row>
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Customed Histogram -->
            <div class="panel" style="height:100%">
              <CustomedHist :attribute="hist_attribute" :time_step="hist_time_step"></CustomedHist>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <el-row type="flex" justify="space-around" style="height: 30%">
      <el-col :span="12" class="row-footer">
        <!-- Line/Scatter -->
        <div class="panel" style="height:100%">
          <Trend :attribute="map_attribute"></Trend>
        </div>
      </el-col>
      <el-col :span="12" class="row-footer" style="padding-left: 0">
        <!-- Customed Line/Scatter -->
        <div class="panel" style="height:100%">
          <CustomedTrend :attributes="trend_value"></CustomedTrend>
        </div>
      </el-col>
    </el-row>
    <!--Advanced Functions Modal-->
    <!--Interpolation Modal-->
    <el-dialog title="Spatial Interpolation" :visible.sync="interpolation_visible" width="80%" center>
      <p>1. Linear Interpolation</p>
      <p>2. More advanced Interpolation</p>
      <p>3. GAN Interpolation</p>
    </el-dialog>
    <!--TS Prediction Modal-->
    <el-dialog title="Time Series Prediction" :visible.sync="prediction_visible" width="80%" center>
      <p>1. Linear Interpolation</p>
      <p>2. More advanced Interpolation</p>
      <p>3. GAN Interpolation</p>
    </el-dialog>
    <!--Anomaly Detection Modal-->
    <el-dialog title="Time Series Anomaly Detection" :visible.sync="detection_visible" width="80%" center>
      <p>1. Linear Interpolation</p>
      <p>2. More advanced Interpolation</p>
      <p>3. GAN Interpolation</p>
    </el-dialog>
    <!--Heat Map Modal-->
    <el-dialog title="Time Series Anomaly Detection" :visible.sync="heat_visible" width="80%" center>
      <p>1. Linear Interpolation</p>
      <p>2. More advanced Interpolation</p>
      <p>3. GAN Interpolation</p>
    </el-dialog>
    <!--Correlation Analysis Modal-->
    <el-dialog title="Time Series Anomaly Detection" :visible.sync="correlation_visible" width="80%" center>
      <p>1. Linear Interpolation</p>
      <p>2. More advanced Interpolation</p>
      <p>3. GAN Interpolation</p>
    </el-dialog>
  </el-container>
</template>
<script>
import Value from '@/components/Value';
import Trend from '@/components/Trend';
import CustomedTrend from '@/components/CustomedTrend';
import Hist from '@/components/Hist';
import CustomedHist from '@/components/CustomedHist';
import Top from '@/components/Top';
import Map from '@/components/Map';

export default {
  name: 'Analysis',
  components: {
    Value,
    Trend,
    CustomedTrend,
    Hist,
    CustomedHist,
    Top,
    Map
  },
  data() {
    return {
      interpolation_visible: false,
      prediction_visible: false,
      detection_visible: false,
      heat_visible: false,
      correlation_visible: false,
      time_step: 0,
      hist_time_step: 0,
      hist_attribute: null,
      dot_size: this.config_.dot_size,
      dot_shape: this.config_.dot_shape,
      trend_value: [],
      map_attribute: null,
      trend_options: [{
        value: 'PM25',
        label: 'PM25'
      }, {
        value: 'NO',
        label: 'NO'
      }, {
        value: 'CO',
        label: 'CO'
      }, {
        value: 'CO2',
        label: 'CO2'
      }, {
        value: 'PM10',
        label: 'PM10'
      }],
    }
  },
  mounted: function() {

  },
  methods: {

  },
}

</script>
<style scoped>
.row {
  padding: 1px 1px 1px 1px;
}

.row-footer {
  padding: 1px 2px 2px 2px;
}

.el-col {
  color: white;
  background: black;
}

.tool-box-col {
  background: #1D344D;
  font-family: 'Microsoft Yahei', 'Avenir', Helvetica, Arial, sans-serif;
  font-weight: 100;
  text-align: left;
  padding-left: 2%;
}

.tool-box-row {
  width: 100%;
  padding-right: 5%;
  padding-bottom: 10px;
}

/*#1C2C41;*/
.panel {
  background: #1C2C41;
  height: 100%;
}

.logo {
  width: 100%;
  height: 16%;
}

.scrollbar {
  overflow: auto
}

.scrollbar::-webkit-scrollbar {
  width: 10px;
  height: 1px;
}

.scrollbar::-webkit-scrollbar-thumb {
  border-radius: 0px;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  background: #1C2C41;
}

.scrollbar::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  border-radius: 0px;
  background: #A5A5A5;
}

.full-height {
  height: 100%;
}

</style>
<style scoped>
.advanced-func {
  text-align: left;
  margin: 0 0 0 0;
}

.advanced-func>>>.el-button {
  padding: 0 0 0 0 !important;
}

.advanced-func>>>.el-button--text {
  font-family: 'Microsoft Yahei', 'Avenir', Helvetica, Arial, sans-serif;
  color: #DCDDDF !important;
  font-size: 12px;
  font-weight: 100;

}

.advanced-func>>>.el-button--text:hover {
  color: #409EFF !important;
}

.map-attribute>>>.el-input__inner {
  color: white;
}

.trend-select {
  margin-top: 2px;
}

.trend-select>>>.el-tag.el-tag--info {
  background-color: #8686AB;
  border-color: #e9e9eb;
  color: #DCDDDF;
}

.trend-select>>>.el-tag {
  font-size: 9px;
}

.trend-select>>>.el-input__inner {
  border: 1px solid #424A5B;
  height: 30px;
  background: #1D344D !important;
}

.trend-select>>>.el-input__icon {
  line-height: 0px;
}

.dot-shape>>>.el-radio__input.is-checked+.el-radio__label {
  color: white;
}

/*1C2C41*/
.dot-shape>>>.el-radio__inner {
  width: 12px;
  height: 12px;
}

.dot-shape>>>.el-radio {
  color: #ADADADFF;
  margin-right: 15px;
}

.dot-shape>>>.el-radio__input.is-checked,
  {
  border-color: #3B71A4 !important;
  background: #3B71A4 !important;
}

.dot-shape>>>.el-radio__inner:hover {
  border-color: #3B71A4;
}

.dot-size {
  width: 70px;
  padding-top: 5px;
  height: 15px !important;
}


.dot-size>>>.el-input__inner {
  background-color: #1D344D;
  border: 0px;
  color: #ADADADFF;
  padding: 0 0 0 0;
  text-align: left;
  height: 20px !important;
  position: absolute !important;
}

.dot-size>>>.el-input-number__decrease,
.dot-size>>>.el-input-number__increase {
  border: none;
  height: 0px !important;
  line-height: 0px !important;
  background: #1D344D;
  color: #ADADADFF;
}

.my-slider>>>.el-input-number__decrease,
.my-slider>>>.el-input-number__increase {
  border: none;
}

.my-slider>>>.el-input-number__decrease,
.my-slider>>>.el-input-number__increase,
.my-slider>>>.el-input--small,
.my-slider>>>.el-input__inner {
  height: 15px !important;
  line-height: 0px !important;
  padding: 0 0 0 0 !important;
  background: #1D344D;
  color: #ADADADFF;
}

.my-slider>>>.el-input__inner {
  border: 0px solid white;
}

</style>
<style>
.el-slider__runway,
.show-input {
  margin: 9px 0px 0 0;
  margin-right: 130px !important;
}

.el-slider__button {
  border: 1px solid #3B71A4;
  width: 12px;
  height: 12px;
}

.el-slider__bar {
  background-color: #3B71A4;
}

.el-slider__input {
  padding: 0 0 0 0;
  margin: 5px 0 0 0;
  background: #1C2C41 !important;
}

.el-collapse,
.el-collapse-item__wrap {
  border: none;
}

.el-collapse-item__header {
  background: #1C2C41 !important;
  height: 27px;
  color: white;
  border: none;
}

.el-collapse-item__content {
  background: #1D344D !important;
  color: white;
  border: none;
  padding: 0 0 0 0;
}

.el-slider,
.el-slider--with-input {
  padding: 0 0 0 0;
  margin: 0 0 0 0;
}

</style>
