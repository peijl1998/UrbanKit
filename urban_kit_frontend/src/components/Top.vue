<template>
  <div id="top-chart" class="top-class">
  </div>
</template>
<script>
export default {
  name: 'Top',
  props: ["attribute", "time_step"],
  data() {
    return {
      topChart: null,
      option: null,
      tops: [],
      vals: [],
      data_signal: false,
      timeline: [],
    }
  },
  watch: {
    attribute() {
      this.reDraw();
    },
    time_step() {
      this.reDraw();
    }
  },
  mounted: function() {
    this.topChart = this.$echarts.init(document.getElementById('top-chart'));
    window.addEventListener('resize', () => {
      this.topChart.resize();
    })
  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.time_step == null;
    },
    async getData() {
      this.data_signal = false;
      var promise = this.GetTopAttrByTime(this.global_.data_name, this.attribute, this.time_step, 7);
      await promise.then((response) => {
        var data = response.data;
        this.tops = data.tops;
        this.vals = data.vals;
      })
      promise = this.GetTimeLine(this.global_.data_name);
      await promise.then((response) => {
        this.timeline = response.data;
        this.data_signal = true;
      })
    },
    async reDraw() {
      if (this.is_not_prepared()) return true;
      await this.getData();
      if (this.option == null) {
        this.draw();
      } else {
        this.option.yAxis[0].data = this.tops;
        this.option.series[0].data = this.vals;
        this.option.title.text = this.attribute + "_Top7" + "(" +  this.timeline[this.time_step] + ")";
        this.topChart.setOption(this.option, true);
      }
    },
    draw() {
      if (this.data_signal == false) return ;
      var tops = this.tops;
      var vals = this.vals;
      var name = this.attribute + "_Top7" + "(" +  this.timeline[this.time_step] + ")";
      var colorArray = ['#C33B3BFF', "#D3632BFF", '#DD9B21', '#1ace4a', '#4bf3ff', '#4f9aff', '#b250ff'];
      this.option = {
        title: {
          text: name,
          textStyle: {
            fontWeight: 'normal',
            fontSize: 15,
            color: '#F1F1F3'
          },
          left: '0%'
        },
        backgroundColor: '#1C2C41',
        tooltip: {
          show: true,
          formatter: "{b}:{c}"
        },
        grid: {
          left: '2%',
          right: '12%',
          top: "15%",
          bottom: "0%",
          containLabel: true
        },
        xAxis: {
          type: 'value',
          show: false,
          axisTick: {
            show: false
          },
          splitLine: {
            show: false,
          },
        },
        yAxis: [{
            type: 'category',
            axisTick: {
              show: false,
            },
            splitLine: {
              show: false
            },
            inverse: 'true',
            axisLine: {
              show: false,
              lineStyle: {
                color: '#CECECEFF',
              }
            },
            data: tops
          }
        ],
        series: [{
          name: '',
          type: 'bar',
          label: {
            normal: {
              show: true,
              position: 'right',
              formatter: '{c}',
              textStyle: {
                color: 'white'
              }
            }
          },
          itemStyle: {
            normal: {
              show: false,
              color: function(params) {
                let num = colorArray.length;
                return {
                  type: 'linear',
                  colorStops: [{
                    offset: 0,
                    color: 'rgba(11,42,84,.3)'
                  }, {
                    offset: 1,
                    color: colorArray[params.dataIndex % num]
                  }],
                  //globalCoord: false
                }
              },
              barBorderRadius: 70,
              borderWidth: 0,
            }
          },
          barGap: '0%',
          barCategoryGap: '20%',
          data: vals
        }]
      };
      this.topChart.setOption(this.option);
    },
  },
}

</script>
<style>
.top-class {
  width: 100%;
  height: 100%;
}

</style>
