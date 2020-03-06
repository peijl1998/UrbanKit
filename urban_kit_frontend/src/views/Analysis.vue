<template>
  <el-container class="is-vertical" style="height: 100%">
    <el-row type="flex" justify="space-around" style="height: 70%">
      <el-col :span="6" class="row">
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Tool Box -->
            <div class="panel">
              Tool Box
            </div>
          </el-col>
        </el-row>
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Other Plots -->
            <div class="panel" style="height:100%;text-align:left">
              <Top></Top>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="12">
        <el-row type="flex" justify="space-around" style="height: 15%">
          <el-col :span="6" class="row">
            <!-- Value1 -->
            <div class="panel">
              <Value index="Average" color="#3B8AC3FF"></Value>
            </div>
          </el-col>
          <el-col :span="6" class="row">
            <!-- Value2 -->
            <div class="panel">
              <Value index="Max" color="#C97035FF"></Value>
            </div>
          </el-col>
          <el-col :span="6" class="row">
            <!-- Value3 -->
            <div class="panel">
              <Value index="Min" color="#FF7F7FFF"></Value>
            </div>
          </el-col>
          <el-col :span="6" class="row">
            <!-- Value4 -->
            <div class="panel">
              <Value index="Median" color="#8C5DA1FF"></Value>
            </div>
          </el-col>
        </el-row>
        <el-row type="flex" justify="space-around" style="height: 85%">
          <el-col :span="24" class="row">
            <!-- Map -->
            <div class="panel" style="height:100%">
              <Map></Map>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="6">
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Histogram -->
            <div class="panel" style="height:100%">
              <Hist></Hist>
            </div>
          </el-col>
        </el-row>
        <el-row type="flex" justify="space-around" style="height: 50%">
          <el-col :span="24" class="row">
            <!-- Customed Histogram -->
            <div class="panel" style="height:100%">
              <CustomedHist></CustomedHist>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <el-row type="flex" justify="space-around" style="height: 30%">
      <el-col :span="12" class="row-footer">
        <!-- Line/Scatter -->
        <div class="panel" style="height:100%">
          <Trend></Trend>
        </div>
      </el-col>
      <el-col :span="12" class="row-footer" style="padding-left: 0">
        <!-- Customed Line/Scatter -->
        <div class="panel" style="height:100%">
          <CustomedTrend></CustomedTrend>
        </div>
      </el-col>
    </el-row>
  </el-container>
</template>
<script>
import Value from '@/components/Value';
import Trend from '@/components/Trend';
import CustomedTrend from '@/components/CustomedTrend';
import Hist from '@/components/Hist';
import CustomedHist from '@/components/CustomedHist';
import Top from '@/components/Top';
import Map from '@/components/Map';

export default {
  name: 'Analysis',
  components: {
    Value,
    Trend,
    CustomedTrend,
    Hist,
    CustomedHist,
    Top,
    Map
  },
  data() {
    return {

    }
  },
  mounted: function() {

  },
  methods: {

  },
}

</script>
<style scoped>
.row {
  padding: 1px 1px 1px 1px;
}

.row-footer {
  padding: 1px 2px 2px 2px;
}

.el-col {
  color: white;
  background: black;
}

/*#1C2C41;*/
.panel {
  background: #1C2C41;
  height: 100%;
}

</style>
