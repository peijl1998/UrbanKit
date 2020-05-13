<template>
  <div style="height:100%">
    <el-row>
      <el-select v-model="method_value" placeholder="Select Method">
        <el-option v-for="item in method_options" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="poi_value" placeholder="Select ID">
        <el-option v-for="item in poi_options" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="attr_value" collapse-tags style="margin-left: 20px;" placeholder="Select Attr">
        <el-option v-for="item in attr_options" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      &nbsp
      <el-button type="success" @click="run">Predict</el-button>
    </el-row>
    <br />
    <el-row type="flex">
      &nbsp
      <el-col :span="2">
        <el-input v-model="params.split" placeholder="Window Size"></el-input>
      </el-col>
      &nbsp
      <el-col :span="2">
        <el-input v-model="params.threshold" placeholder="Threshold"></el-input>
      </el-col>
    </el-row>
    <el-row style="height:80%;width: 100%">
      <div ref="chart" class="map-class">
      </div>
    </el-row>
  </div>
</template>
<script>
require('echarts/extension/bmap/bmap')
export default {
  name: 'AnomalyDetection',
  data() {
    return {
      params: {
        lr: null,
        split: null,
        threshold: null
      },
      poi_options: [],
      attr_options: [],
      method_options: [{ value: "Isolation Forest", label: "Isolation Forest" }],
      poi_value: '',
      attr_value: '',
      method_value: '',
      Chart: null,
    }
  },
  mounted: function() {
    var promise = this.GetIdList(this.global_.data_name);
    promise.then((response) => {
      var data = response.data;
      this.poi_options = []
      for (var i = 0; i < data.length; ++i) {
        if (data[i].length > 0) {
          this.poi_options.push({ value: data[i], label: data[i] });
        }
      }
    });
    promise = this.GetAttrList(this.global_.data_name);
    promise.then((response) => {
      var data = response.data;
      this.attr_options = []
      for (var i = 0; i < data.length; ++i) {
        this.attr_options.push({ value: data[i], label: data[i] });
      }
    });
    this.Chart = this.$echarts.init(this.$refs.chart);
    window.addEventListener('resize', () => {
      this.Chart.resize();
    })
  },
  methods: {
    run() {
      var promise = this.AnomalyDetection(this.global_.data_name, this.attr_value, this.poi_value);
      promise.then((response) => {
        var data = response.data;
        var timeline = [];
        var raw = [];
        var anomaly = []
        //console.log(data)
        for (var i = 0; i < data[0].length; ++i) {
          timeline.push(data[0][i]);
          raw.push(data[1][i]);
          anomaly.push(data[2][i]);
        }
        this.draw(timeline, raw, anomaly);
      });
    },
    draw(timeline, raw, anomaly) {
      var option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            lineStyle: {
              color: '#ADADADFF'
            }
          }
        },
        legend: {
          icon: 'rect',
          itemWidth: 14,
          itemHeight: 5,
          itemGap: 13,
          data: ["normal", "abnormal"],
          right: '4%',
          textStyle: {
            fontSize: 15,
          }
        },
        grid: {
          left: '2%',
          right: '4%',
          bottom: '2%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: '#ADADADFF'
            }
          },
          textStyle: {
            fontSize: 15,
            color: "#000000FF"
          },
          data: timeline,
        }],
        yAxis: [{
          type: 'value',
          name: false,
          axisTick: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#ADADADFF'
            }
          },
          axisLabel: {
            margin: 10,
            textStyle: {
              fontSize: 14
            }
          },
          splitLine: {
            lineStyle: {
              color: '#ADADADFF'
            }
          }
        }],
        series: [{
            name: "normal",
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                width: 1
              }
            },
            itemStyle: {
              normal: {
                color: 'rgb(137,189,27)',
                borderColor: 'rgba(0,136,212,0.2)',
                borderWidth: 12
              }
            },
            data: raw,
          },
          {
            name: "abnormal",
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                width: 1
              }
            },
            itemStyle: {
              normal: {
                color: 'rgb(219,50,51)',
              }
            },
            data: anomaly,
          },
        ]
      };
      option["grid"]["bottom"] = "10%";
      option["dataZoom"] = [{
        type: 'inside',
        start: 0,
        end: 50
      }, {
        start: 0,
        end: 50,
        handleSize: '100%',
        height: 10,
        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleStyle: {
          color: '#A0A0A0FF',
          shadowBlur: 3,
          shadowColor: 'rgba(0, 0, 0, 0.6)',
        },
        textStyle: false,
        bottom: 5,
      }];
      this.Chart.setOption(option);
    }
  },
}

</script>
<style>
.map-class {
  width: 100%;
  height: 100%;
}

.anchorBL {
  display: none;
}

</style>
