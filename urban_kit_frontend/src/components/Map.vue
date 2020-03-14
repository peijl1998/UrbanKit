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
      topChart: null,
      bmap: null,
      option: null,
    }
  },
  watch: {
    time_step() {
      this.option.baseOption.timeline.data[1] = this.time_step;
      this.mapChart.setOption(this.option, true);
    },
    attribute() {
      console.log(this.attribute);
    },
    dot_shape() {
      this.option.baseOption.series[0].symbol = this.dot_shape;
      this.mapChart.setOption(this.option, true);
    },
    dot_size() {
      this.option.baseOption.series[0].symbolSize = this.dot_size;
      this.mapChart.setOption(this.option, true);
    },
  },
  mounted: function() {
    this.mapChart = this.$echarts.init(document.getElementById('map-chart'));
    window.addEventListener('resize', () => {
      this.mapChart.resize();
    })
    this.init_time_line();
    this.bmap = this.mapChart.getModel().getComponent('bmap').getBMap();
    /*var mapStyle ={
        features: ["road","building","water","land"],
        style : "dark",
    };
    this.bmap.setMapStyle(mapStyle);*/
  },
  methods: {
    init_time_line() {
      var geoCoordMap = {
        "海门": [116.4694444, 39.9051111],
        "鄂尔多斯": [116.3905556, 39.986],
        "招远": [116.3052778, 39.943],
        "舟山": [116.2565556, 39.887],
        "齐齐哈尔": [116.469, 39.9861111],
      };
      var dataList1 = [
        { name: "海门", value: [116.4694444, 39.9051111, 1] },
        { name: "鄂尔多斯", value: [116.3905556, 39.986, 2] },
        { name: "招远", value: [116.3052778, 39.943, 3] },
        { name: "舟山", value: [116.2565556, 39.887, 4] },
        { name: "齐齐哈尔", value: [116.469, 39.9861111, 5] },
      ];
      var dataList2 = [
        { name: "海门", value: [116.4694444, 39.9051111, 10] },
        { name: "鄂尔多斯", value: [116.3905556, 39.986, 20] },
        { name: "招远", value: [116.3052778, 39.943, 30] },
        { name: "舟山", value: [116.2565556, 39.887, 40] },
        { name: "齐齐哈尔", value: [116.469, 39.9861111, 50] },
      ];
      var dataList3 = [
        { name: "海门", value: [116.4694444, 39.9051111, 5] },
        { name: "鄂尔多斯", value: [116.3905556, 39.986, 10] },
        { name: "招远", value: [116.3052778, 39.943, 15] },
        { name: "舟山", value: [116.2565556, 39.887, 20] },
        { name: "齐齐哈尔", value: [116.469, 39.9861111, 25] },
      ];
      this.option = {
        baseOption: {
          timeline: {
            axisType: 'category',
            show: true,
            lineStyle: {
              color: "#D6D6DB"
            },
            label: {
              color: "#FFFFFF",
            },
            controlStyle: {
              borderColor: "#D6D6DB"
            },
            autoPlay: true,
            playInterval: 1000,
            data: ["2017-1-1", this.time_step, "2017-1-3"]
          },
          tooltip: {
            trigger: 'item',
            formatter: function(params) {
              return params.seriesName + "<br/><strong>" + params.data.name + "</strong>:" + params.data.value[2];
            }
          },
          visualMap: {
            type: 'continuous',
            min: 1,
            max: 50,
            text: ["High", "Low"],
            textStyle: { color: "#FFFFFF" },
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
          bmap: this.getBmap(geoCoordMap),
          series: [{
            symbol: "circle",
            name: "name",
            type: 'effectScatter',
            showEffectOn: 'render',
            rippleEffect: {
              brushType: 'stroke'
            },
            hoverAnimation: true,
            coordinateSystem: 'bmap',
            symbolSize: 10,
            itemStyle: {
              normal: {
                color: "white",
                shadowBlur: 10,
                shadowColor: 'white'
              }
            }
          }],
        },
        options: [
          { series: [{ type: "effectScatter", data: JSON.parse(JSON.stringify(dataList1)) }] },
          { series: [{ type: "effectScatter", data: JSON.parse(JSON.stringify(dataList2)) }] },
          { series: [{ type: "effectScatter", data: JSON.parse(JSON.stringify(dataList3)) }] },
        ]
      }
      this.mapChart.setOption(this.option);
    },
    init() {
      var geoCoordMap = {
        "海门": [116.4694444, 39.9051111],
        "鄂尔多斯": [116.3905556, 39.986],
        "招远": [116.3052778, 39.943],
        "舟山": [116.2565556, 39.887],
        "齐齐哈尔": [116.469, 39.9861111],
      };
      var dataList = [
        { name: "海门", value: [116.4694444, 39.9051111, 9] },
        { name: "鄂尔多斯", value: [116.3905556, 39.986, 12] },
        { name: "招远", value: [116.3052778, 39.943, 10] },
        { name: "舟山", value: [116.2565556, 39.887, 12] },
        { name: "齐齐哈尔", value: [116.469, 39.9861111, 14] },
      ];
      var option = {
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            return params.seriesName + "<br/><strong>" + params.data.name + "</strong>:" + params.data.value[2];
          }
        },
        visualMap: {
          type: 'continuous',
          min: 9,
          max: 14,
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
        bmap: this.getBmap(geoCoordMap),
        series: [{
          symbol: "circle",
          name: "name",
          type: 'effectScatter',
          showEffectOn: 'render',
          rippleEffect: {
            brushType: 'stroke'
          },
          hoverAnimation: true,
          coordinateSystem: 'bmap',
          data: JSON.parse(JSON.stringify(dataList)),
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
      this.mapChart.setOption(option);
    },
    getBmap(geoCoordMap) {
      return {
        center: this.getCenter(geoCoordMap),
        zoom: 12,
        roam: true,
        mapStyle: this.global_.plainMapStyle,
      }
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
