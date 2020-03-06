<template>
  <div id="customed-hist-chart" class="hist-class">
  </div>
</template>
<script>
export default {
  name: 'CustomedHist',
  props: [],
  data() {
    return {
      customedHistChart: null,
    }
  },
  mounted: function() {
    this.customedHistChart = this.$echarts.init(document.getElementById('customed-hist-chart'));
    window.addEventListener('resize', () => {
      this.customedHistChart.resize();
    })
    this.init();
  },
  methods: {
    init() {
      var X = ['Haidian', 'Chaoyang', 'Changping', 'Aotizhongxin', 'Xizhimen', 'Dongzhimen', 'Dongcheng'];
      var Y = [12500, 14000, 21500, 23200, 24450, 25250, 7500];
      var name = "Beijing_PM10_1_11";
      var option = {
        backgroundColor: '#1C2C41',
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(255,255,255,0.1)',
          axisPointer: {
            type: 'shadow',
            label: {
              show: true,
              backgroundColor: '#7B7DDC'
            }
          }
        },
        grid: {
          left: '2%',
          right: '6%',
          bottom: '1%',
          containLabel: true
        },
        xAxis: {
          data: X,
          axisLine: {
            lineStyle: {
              color: '#ADADADFF'
            }
          },
          axisTick: {
            show: false,
          },
        },
        yAxis: [{
          axisLine: {
            lineStyle: {
              color: '#ADADADFF',
            }
          },
          splitLine: {
            show: false,
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          },
          axisLabel: {
            formatter: '{value} ',
          }
        }],
        legend: {
          data: [name],
          top: 10,
          textStyle: {
            color: 'rgba(55,255,249,1)'
          }
        },
        series: [{
            name: name,
            type: 'bar',
            barWidth: 15,
            barGap: '-100%',
            itemStyle: {
              barBorderRadius: 20,
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                  offset: 0.4,
                  color: "rgba(143, 141, 70, 1)"
                },
                {
                  offset: 1,
                  color: "rgba(8,228,222,0.2)"
                }
              ])
            },
            data: Y
          }

        ]
      };
      if (X.length > 20) {
        option["grid"]["bottom"] = "10%";
        option["dataZoom"] = [{
          type: 'inside',
          start: 0,
          end: 100
        }, {
          start: 0,
          end: 100,
          handleSize: '80%',
          height: 20,
          handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
          handleStyle: {
            color: '#A0A0A0FF',
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.6)',
          },
          bottom: 0,
        }];
      }
      this.customedHistChart.setOption(option);
    },
  },
}

</script>
<style>
.hist-class {
  width: 100%;
  height: 100%;
}

</style>
