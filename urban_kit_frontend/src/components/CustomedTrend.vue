<template>
  <div id="customed-trend-chart" class="map-class">
  </div>
</template>
<script>
export default {
  name: 'CustomedTrend',
  props: ["attributes", "id"],
  data() {
    return {
      customedTrendChart: null,
      option: null,
      timeline: [],
      vals: {},
      data_signal: [],
    }
  },
  watch: {
    attributes() {
      this.reDraw();
    },
    id() {
      this.reDraw();
    }
  },
  mounted: function() {
    this.customedTrendChart = this.$echarts.init(document.getElementById('customed-trend-chart'));
    window.addEventListener('resize', () => {
      this.customedTrendChart.resize();
    })
  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attributes.length == 0 || this.id == null;
    },
    async getData() {
      this.data_signal = false;
      var promise = this.GetMultiAttrById(this.global_.data_name, JSON.parse(JSON.stringify(this.attributes)), this.id);
      await promise.then((response) => {
        var data = response.data;
        this.timeline = [];
        this.vals = {};
        for (var i = 0; i < this.attributes.length; ++i) {
          this.vals[this.attributes[i]] = [];
        }
        for (var i = 0; i < data.length; ++i) {
          this.timeline.push(data[i].time);
          for (var j = 0; j < this.attributes.length; ++j) {
            this.vals[this.attributes[j]].push(data[i].value[this.attributes[j]]);
          }
        }
        this.data_signal = true;
      })
    },
    async reDraw() {
      if (this.is_not_prepared()) return;
      await this.getData();
      if (this.option == null) {
        this.draw();
      } else {
        this.option.title.text = this.id + "_Trend";
        this.option.series = this.makeSeries();
        this.option.xAxis[0].data = this.timeline;
        this.scale();
        this.customedTrendChart.setOption(this.option, true);
      }
    },
    draw() {
      if (this.data_signal == false) return;
      var text = this.id + "_Trend";
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
        legend: {
          icon: 'rect',
          itemWidth: 14,
          itemHeight: 5,
          itemGap: 13,
          data: JSON.parse(JSON.stringify(this.attributes)),
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
          data: this.timeline
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
        series: this.makeSeries()
      };
      this.scale();
      this.customedTrendChart.setOption(this.option);
    },
    makeSeries() {
      var color1 = ['rgba(0, 136, 212, 0.3)', 'rgba(219, 50, 51, 0.3)', 'rgba(137, 189, 27, 0.3)'];
      var color2 = ['rgba(0, 136, 212, 0)', 'rgba(219, 50, 51, 0)', 'rgba(137, 189, 27, 0)'];
      var color3 = ['rgb(0,136,212)', 'rgb(219,50,51)', 'rgb(137,189,27)'];
      var color4 = ['rgba(0,136,212,0.2)', 'rgba(219,50,51,0.2)', 'rgba(137,189,2,0.27)']
      var series = [];
      for (var i = 0; i < this.attributes.length; ++i) {
        var temp = {
          name: "-----",
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
              color: false,
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowBlur: 10
            }
          },
          itemStyle: {
            normal: {
              color: 'color3',
              borderColor: 'color4',
              borderWidth: 12
            }
          },
          data: []
        };
        temp.name = this.attributes[i];
        temp.areaStyle.normal.color = new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
          offset: 0,
          color: color1[i]
        }, {
          offset: 0.8,
          color: color2[i]
        }], false);
        temp.itemStyle.normal.color = color3[i];
        temp.itemStyle.normal.borderColor = color4[i];
        temp.data = this.vals[this.attributes[i]];
        series.push(temp);
        console.log(series);
      }
      return series;
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
