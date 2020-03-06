<template>
  <div id="trend-chart" class="map-class">
  </div>
</template>
<script>
export default {
  name: 'Trend',
  props: [],
  data() {
    return {
      trendChart: null,
    }
  },
  mounted: function() {
    this.trendChart = this.$echarts.init(document.getElementById('trend-chart'));
    window.addEventListener('resize', () => {
      this.trendChart.resize();
    })
    this.init();
  },
  methods: {
    init() {
      var Y = ['13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55'];
      var X = [120, 110, 125, 145, 122, 165, 122, 220, 182, 191, 134, 150];
      var option = {
        backgroundColor: '#1C2C41',
        title: {
          text: 'Beijing_PM2.5_Trend',
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
          data: Y
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
          showSymbol: true,
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
          data: X
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
      this.trendChart.setOption(option);
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
