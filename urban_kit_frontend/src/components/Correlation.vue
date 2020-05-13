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
      <el-select v-model="attr_values" multiple collapse-tags style="margin-left: 20px;" placeholder="Select Attr">
        <el-option v-for="item in attr_options" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      &nbsp
      <el-button type="success" @click="run">Run</el-button>
    </el-row>
    <el-row style="height:80%;width: 50%">
      <div ref="corr_chart" class="map-class">
      </div>
    </el-row>
  </div>
</template>
<script>
require('echarts/extension/bmap/bmap')
export default {
  name: 'Correlation',
  data() {
    return {
      poi_options: [],
      attr_options: [],
      method_options: [{ value: "DTW", label: "DTW" }, { value: "Pearson", label: "Pearson" }],
      poi_value: '',
      attr_values: [],
      method_value: '',
      corrChart: null,
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
    this.corrChart = this.$echarts.init(this.$refs.corr_chart);
    window.addEventListener('resize', () => {
      this.corrChart.resize();
    })
  },
  methods: {
    run() {
      var promise = this.CalCorr(this.global_.data_name, this.attr_values, this.poi_value, this.method_value);
      promise.then((response) => {
        var data = response.data;
        var vs = [];
        var _min = 1000;
        var _max = -1000;
        for (var i = 0; i < data.length; ++i) {
          vs.push(data[i]);
          if (data[i][2] > _max) _max = data[i][2]
          if (data[i][2] < _min) _min = data[i][2]
        }
        this.draw(this.attr_values, this.attr_values, vs, _min, _max);
      });
    },
    draw(xs, ys, data, _min, _max) {
      data = data.map(function(item) {
        return [item[1], item[0], item[2]];
      });

      console.log(xs)
      console.log(ys)
      console.log(data)

      var option = {
        animation: false,
        grid: {
          left: '3%',
          right: '8%',
          bottom: '8%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: xs,
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          axisLabel: {
            interval: 0,
            rotate: 40

          },
          splitArea: {
            show: true
          },
        },
        yAxis: {
          type: 'category',
          data: ys,
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          axisLabel: {
            interval: 0,
            rotate: 40

          },
          splitArea: {
            show: true
          },
        },
        visualMap: {
          min: _min,
          max: _max,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '1%',
          color: [
            '#22DDDD', '#fec42c', '#80F1BE'
          ]
        },
        series: [{
          name: 'Punch Card',
          type: 'heatmap',
          data: data,
          label: {
            normal: {
              show: true
            }
          },
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowColor: 'rgba(120, 0, 0, 0.5)'
            }
          }
        }]
      };
      this.corrChart.setOption(option);
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
