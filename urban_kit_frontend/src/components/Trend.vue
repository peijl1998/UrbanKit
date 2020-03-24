<template>
  <div id="trend-chart" class="map-class">
  </div>
</template>
<script>
export default {
  name: 'Trend',
  props: ["attribute", "id"],
  data() {
    return {
      trendChart: null,
      option: null,
      timeline: [],
      vals: [],
      data_signal: false
    }
  },
  watch: {
    attribute() {
      this.reDraw();
    },
    id() {
      console.log("id change.");
      this.reDraw();
    }
  },
  mounted: function() {
    this.trendChart = this.$echarts.init(document.getElementById('trend-chart'));
    window.addEventListener('resize', () => {
      this.trendChart.resize();
    })
  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.id == null;
    },
    async reDraw() {
      if (this.is_not_prepared()) return;
      await this.getData();
      if (this.option == null) {
        this.draw();
      } else {
        this.option.title.text = this.id + "_" + this.attribute + "_Trend";
        this.option.xAxis[0].data = this.vals;
        this.option.series[0].name = this.attribute;
        this.option.series[0].data = this.timeline;
        this.scale();
        this.trendChart.setOption(this.option, true);
      }
    },
    async getData() {
      this.data_signal = false;
      var promise = this.GetAttrById(this.global_.data_name, this.attribute, this.id);
      await promise.then((response) => {
        var data = response.data;
        this.timeline = [];
        this.vals = [];
        for (var i = 0; i < data.length; ++i) {
          this.timeline.push(data[i].time);
          this.vals.push(data[i].value);
        }
        this.data_signal = true;
      })
    },
    draw() {
      if (this.data_signal == false) return;
      var text = this.id + "_" + this.attribute + "_Trend";
      this.option = {
        backgroundColor: '#1C2C41',
        title: {
          text: text,
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
          data: this.timeline,
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
          name: this.attribute,
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
          data: this.vals,
        }]
      };
      this.scale();
      this.trendChart.setOption(this.option);
    },
    scale() {
      if (this.timeline.length > 100) {
        this.option["grid"]["bottom"] = "10%";
        this.option["dataZoom"] = [{
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
      }
    }
  },
}

</script>
<style>
.map-class {
  width: 100%;
  height: 100%;
}

</style>
