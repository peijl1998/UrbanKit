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
    }
  },
  watch: {
    attribute() {
      this.reDraw(this.attribute, this.time_step);
    },
    time_step() {
      this.reDraw(this.attribute, this.time_step);
    }
  },
  mounted: function() {
    this.topChart = this.$echarts.init(document.getElementById('top-chart'));
    window.addEventListener('resize', () => {
      this.topChart.resize();
    })
    this.init();
  },
  methods: {
    reDraw(attr, time) {
      if (attr == null) {
        attr = "NULL";
      }
      this.option.title.text = "Beijing_" + attr + "_" + time + "_ Top7";
      this.topChart.setOption(this.option, true);
    },
    init() {
      var tops = ['Haidian', 'Chaoyang', 'Changping', 'Aotizhongxin', 'Xizhimen', 'Dongzhimen', 'Dongcheng'];
      var vals = [23200, 21500, 12500, 8500, 7500, 5500, 4600];
      var name = "Beijing_PM10_1_10 Top7";
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
