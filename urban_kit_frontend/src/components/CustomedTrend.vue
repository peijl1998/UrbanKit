<template>
  <div id="customed-trend-chart" class="map-class">
  </div>
</template>
<script>
export default {
  name: 'CustomedTrend',
  props: [],
  data() {
    return {
      customedTrendChart: null,
    }
  },
  mounted: function() {
    this.customedTrendChart = this.$echarts.init(document.getElementById('customed-trend-chart'));
    window.addEventListener('resize', () => {
      this.customedTrendChart.resize();
    })
    this.init();
  },
  methods: {
    init() {
      var X = ['13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55'];
      var Y1 = [120, 110, 125, 145, 122, 165, 122, 220, 182, 191, 134, 150];
      var Y2 = [220, 182, 125, 145, 122, 191, 134, 150, 120, 110, 165, 122];
      var Y3 = [220, 182, 191, 134, 150, 120, 110, 125, 145, 122, 165, 122];
      var option = {
        backgroundColor: '#1C2C41',

        title: {
          text: 'Customed Trend',
          textStyle: {
            fontWeight: 'normal',
            fontSize: 15,
            color: '#F1F1F3'
          },
          left: '0%'
        },
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
          data: ['PM2.5', 'NO2', 'PM10'],
          right: '4%',
          textStyle: {
            fontSize: 12,
            color: '#F1F1F3'
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
          data: X
        }],
        yAxis: [{
          type: 'value',
          name: 'mm³',
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
          name: 'PM2.5',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              width: 1
            }
          },
          areaStyle: {
            normal: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(0, 136, 212, 0.3)'
              }, {
                offset: 0.8,
                color: 'rgba(0, 136, 212, 0)'
              }], false),
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {
              color: 'rgb(0,136,212)',
              borderColor: 'rgba(0,136,212,0.2)',
              borderWidth: 12

            }
          },
          data: Y1
        }, {
          name: 'NO2',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              width: 1
            }
          },
          areaStyle: {
            normal: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(219, 50, 51, 0.3)'
              }, {
                offset: 0.8,
                color: 'rgba(219, 50, 51, 0)'
              }], false),
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {

              color: 'rgb(219,50,51)',
              borderColor: 'rgba(219,50,51,0.2)',
              borderWidth: 12
            }
          },
          data: Y2
        }, {
          name: 'PM10',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              width: 1
            }
          },
          areaStyle: {
            normal: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(137, 189, 27, 0.3)'
              }, {
                offset: 0.8,
                color: 'rgba(137, 189, 27, 0)'
              }], false),
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {
              color: 'rgb(137,189,27)',
              borderColor: 'rgba(137,189,2,0.27)',
              borderWidth: 12

            }
          },
          data: Y3
        }]
      };
      if (X.length > 100) {
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
      if (X.length > 100) {
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
      this.customedTrendChart.setOption(option);
    },
  },
}

</script>
<style>
.map-class {
  width: 100%;
  height: 100%;
}

</style>
