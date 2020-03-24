<template>
  <div id="customed-hist-char" class="hist-class">
  </div>
</template>
<script>
export default {
  name: 'CustomedHist',
  props: ["attribute", "time_step"],
  data() {
    return {
      customedHistChart: null,
      option: null,
      timeline: [],
      data_signal: false,
      ids: [],
      vals: [],
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
    this.customedHistChart = this.$echarts.init(document.getElementById('customed-hist-char'));
    window.addEventListener('resize', () => {
      this.customedHistChart.resize();
    })
  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.time_step == null;
    },
    async getData() {
      this.data_signal = false;
      var promise = this.GetAttrByTime(this.global_.data_name, this.attribute, this.time_step);
      await promise.then((response) => {
        var data = response.data;
        this.ids = [];
        this.vals = [];
        for (var i = 0; i < data.length; ++i) {
          this.ids.push(data[i].id);
          this.vals.push(data[i].value);
        }
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
        var name = this.attribute + "(" + this.timeline[this.time_step] + ")";
        this.option.legend.data = [name];
        this.option.series[0].name = name;
        this.scale();
        this.histChart.setOption(this.option, true);
      }
    },
    draw() {
      if (this.data_signal == false) return;
      var name = this.attribute + "(" + this.timeline[this.time_step] + ")";
      this.option = {
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
        legend: {
          top: 10,
          data: [name],
          textStyle: {
            color: 'rgba(55,255,249,1)'
          }
        },
        xAxis: {
          data: this.ids,
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
          splitLine: {
            show: false,
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          },
          axisLine: {
            lineStyle: {
              color: '#ADADADFF',
            }
          },
          axisLabel: {
            formatter: '{value} ',
          }
        }],
        series: [{
          name: name,
          type: 'bar',
          barWidth: 15,
          itemStyle: {
            normal: {
              barBorderRadius: 5,
              color: new this.$echarts.graphic.LinearGradient(
                0, 0, 0, 1,
                [
                  { offset: 0, color: '#956FD4' },
                  { offset: 1, color: '#3EACE5' }
                ]
              )
            }
          },
          data: this.vals
        }]
      };
      this.scale();
      this.customedHistChart.setOption(this.option);
    },
    scale() {
      if (this.data_signal == false) return;
      if (this.ids.length > 9) {
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
.hist-class {
  width: 100%;
  height: 100%;
}

</style>
