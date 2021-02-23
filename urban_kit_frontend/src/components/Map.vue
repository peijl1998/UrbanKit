<template>
  <div style="height:100%">
    <div id="map-chart" class="map-class">
    </div>
  </div>
</template>
<script>
require('echarts/extension/bmap/bmap')
export default {
  name: 'Map',
  props: ["time_step", "attribute", "dot_shape", "dot_size"],
  data() {
    return {
      mapChart: null,
      bmap: null,
      option: null,       
      geoCoordMap: null,
      dataList: null,
      min_value: 0,
      max_value: 100,
      data_signal: false,
    }
  },
  watch: {
    async time_step() {
      if (this.is_not_prepared()) return;
      await this.getData();
      if (this.option == null) {
        this.draw();
      } else {
        this.option.visualMap.min = this.min_value;
        this.option.visualMap.max = this.max_value;
        this.option.series[0].data = JSON.parse(JSON.stringify(this.dataList));
        this.mapChart.setOption(this.option, true);
      }
    },
    async attribute() {
      if (this.is_not_prepared()) return;
      await this.getData();
      if (this.option == null) {
        this.draw();
      } else {
        this.option.series[0].name = this.attribute;
        this.option.visualMap.min = this.min_value;
        this.option.visualMap.max = this.max_value;
        this.option.series[0].data = JSON.parse(JSON.stringify(this.dataList));
        this.mapChart.setOption(this.option, true);
      }
    },
    dot_shape() {
      if (this.option == null) {
        this.draw();
      } else {
        this.option.series[0].symbol = this.dot_shape;
        this.mapChart.setOption(this.option, true);
      }
    },
    dot_size() {
      if (this.option == null) {
        this.draw();
      } {
        this.option.series[0].symbolSize = this.dot_size;
        this.mapChart.setOption(this.option, true);
      }
    },
  },
  mounted: function() {
    this.mapChart = this.$echarts.init(document.getElementById('map-chart'));
    window.addEventListener('resize', () => {
      this.mapChart.resize();
    })
  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.time_step == null;
    },
    async getData() {
      this.data_signal = false;
      var promise = this.GetIdPosition(this.global_.data_name);
      await promise.then((response) => {
        this.geoCoordMap = response.data;
      })
      promise = this.GetAttrByTime(this.global_.data_name, this.attribute, this.time_step);
      await promise.then((response) => {
        var data = response.data;
        this.dataList = []
        if (data.length > 0) {
          this.min_value = data[0].value;
          this.max_value = data[0].value;
        }
        for (var i = 0; i < data.length; ++i) {
          if (this.geoCoordMap.hasOwnProperty(data[i].id)) {
            this.dataList.push({ name: data[i].id, value: this.geoCoordMap[data[i].id].concat(data[i].value) })
            if (data[i].value < this.min_value) this.min_value = data[i].value;
            if (data[i].value > this.max_value) this.max_value = data[i].value;
          }
        }
        this.data_signal = true;
      })
    },
    draw() {
      if (this.is_not_prepared() || this.data_signal == false) {
        return;
      }
      this.option = {
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            return params.seriesName + "<br /><strong>" + params.data.name + "</strong>:" + params.data.value[2];
          }
        },
        visualMap: {
          type: 'continuous',
          min: this.min_value,
          max: this.max_value,
          text: ["High", "Low"],
          textStyle: { color: "#D6D6DB" },
          itemWidth: 10,
          orient: "horizontal",
          top: "1%",
          left: "1%",
          opacity: "50%",
          calculable: false,
          inRange: {
            color: ['#393C74', '#4575b4', '#76AACB', '#abd9e9', '#AFE1EE', '#ffffbf', '#fee090', '#fdae61', '#E07251', '#BD3932', '#8C0C2A']
          },
        },
        bmap: {
          center: this.getCenter(this.geoCoordMap),
          zoom: 10,
          roam: true,
          mapStyle: this.global_.plainMapStyle,
        },
        series: [{
          symbol: "circle",
          name: this.attribute,
          type: 'effectScatter',
          showEffectOn: 'render',
          rippleEffect: {
            brushType: 'stroke'
          },
          hoverAnimation: true,
          coordinateSystem: 'bmap',
          data: JSON.parse(JSON.stringify(this.dataList)),
          symbolSize: 10,
          itemStyle: {
            normal: {
              color: "white",
              shadowBlur: 10,
              shadowColor: 'white'
            }
          }
        }],
      };
      this.mapChart.setOption(this.option);
    },
    getCenter(data) {
      var geos = Object.values(data);
      var ret = [0, 0];
      for (var i = 0; i < geos.length; i++) {
        ret[0] += geos[i][0];
        ret[1] += geos[i][1];
      }
      ret[0] /= geos.length;
      ret[1] /= geos.length;
      return ret;
    },
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
