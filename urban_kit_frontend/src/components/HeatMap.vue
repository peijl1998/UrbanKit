<template>
  <div style="height:100%">
    <div ref="heat_map_chart" class="map-class">
    </div>
  </div>
</template>
<script>
require('echarts/extension/bmap/bmap')
export default {
  name: 'HeatMap',
  props: ["time_step", "attribute"],
  data() {
    return {
      heatChart: null,
      bmap: null,
      option: null,
      geoCoordMap: null,
      dataList: null,
      data_signal: false,
      min_value: 0,
      max_value: 100,
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
        this.heatChart.setOption(this.option, true);
      }
    },
    async attribute() {
      if (this.is_not_prepared()) return;
      await this.getData();
      if (this.option == null) {
        this.draw();
      } else {
        this.option.visualMap.min = this.min_value;
        this.option.visualMap.max = this.max_value;
        this.option.series[0].data = JSON.parse(JSON.stringify(this.dataList));
        this.heatChart.setOption(this.option, true);
      }
    },
  },
  mounted: function() {
    this.heatChart = this.$echarts.init(this.$refs.heat_map_chart);
    window.addEventListener('resize', () => {
      this.heatChart.resize();
    })
    this.init();
  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.time_step == null;
    },
    async init() {
      if (this.is_not_prepared()) return;
      await this.getData();
      if (this.option == null) {
        this.draw();
      }
    },
    async getData() {
      this.data_signal = false;
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
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
            this.dataList.push({ name: data[i].id, value: this.geoCoordMap[data[i].id].concat(data[i].value) });
            if (data[i].value < this.min_value) this.min_value = data[i].value;
            if (data[i].value > this.max_value) this.max_value = data[i].value;
          }
        }
        this.data_signal = true;
        loading.close();
      })
    },
    draw() {
      if (this.data_signal == false) {
        return;
      }
      this.option = {
        visualMap: {
          show: false,
          min: this.min_value,
          max: this.max_value,
          splitNumber: 5,
          inRange: {
            color: ['#d94e5d', '#eac736', '#50a3ba'].reverse()
          }
        },
        bmap: {
          center: this.getCenter(this.geoCoordMap),
          zoom: 8,
          roam: true,
          mapStyle: this.global_.plainMapStyle,
        },
        series: [{
          type: 'heatmap',
          pointSize: 25,
          blurSize: 25,
          coordinateSystem: 'bmap',
          data: JSON.parse(JSON.stringify(this.dataList)),
        }],
      };
      console.log(JSON.parse(JSON.stringify(this.dataList)));
      this.heatChart.setOption(this.option);
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
