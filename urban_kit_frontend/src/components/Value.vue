<template>
  <div class="value-style">
    <el-dropdown size="mini" @command="handleCommand">
      <span class="el-dropdown-link">
        {{this.index}}<i class="el-icon-arrow-down"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="Q1">Q1</el-dropdown-item>
        <el-dropdown-item command="Mean">Mean</el-dropdown-item>
        <el-dropdown-item command="Q3">Q3</el-dropdown-item>
        <el-dropdown-item command="Variance">Variance</el-dropdown-item>
        <el-dropdown-item command="Minimum">Minimum</el-dropdown-item>
        <el-dropdown-item command="Median">Median</el-dropdown-item>
        <el-dropdown-item command="Maximum">Maximum</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <div class="number" v-bind:style="{color:this.color}">{{val}}</div>
  </div>
</template>
<script>
export default {
  name: 'Value',
  props: ["color", "index"],
  data() {
    return {
      val: 123456789,
    }
  },
  mounted: function() {
    console.log(this.color);
  },
  methods: {
    handleCommand(command) {
      this.index = command;
      // calculate val by index
    }
  },
}

</script>
<style>
.value-style {
  margin: 0 auto;
  position: relative;
  top: 50%;
  /*偏移*/
  transform: translateY(-50%);
}

.el-dropdown-link {
  cursor: pointer;
  color: #C6C6C6FF;
}

.el-icon-arrow-down {
  font-size: 12px;
}

.number {
  margin-top: 3%;
  font-size: 18px;
  font-weight: 1000;
}

</style>
