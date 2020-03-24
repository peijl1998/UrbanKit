<template>
  <div class="value-style">
    <el-dropdown size="mini" @command="handleCommand">
      <span class="el-dropdown-link">
        {{this.self_index}}<i class="el-icon-arrow-down"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="Q1">Q1</el-dropdown-item>
        <el-dropdown-item command="Mean">Mean</el-dropdown-item>
        <el-dropdown-item command="Q3">Q3</el-dropdown-item>
        <el-dropdown-item command="Variance">Variance</el-dropdown-item>
        <el-dropdown-item command="Min">Min</el-dropdown-item>
        <el-dropdown-item command="Median">Median</el-dropdown-item>
        <el-dropdown-item command="Max">Max</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <div class="number" v-bind:style="{color:this.color}">{{val}}</div>
  </div>
</template>
<script>
export default {
  name: 'Value',
  props: ["color", "index", "attribute", "time_step"],
  data() {
    return {
      val: "——",
      self_index: "Mean",
    }
  },
  watch: {
    attribute() {
      this.reCal();
    },
    time_step() {
      this.reCal();
    }
  },
  mounted: function() {
    this.self_index = this.index;
  },
  methods: {
    is_not_prepared() {
      return this.global_.data_name == null || this.attribute == null || this.time_step == null;
    },
    getData() {
      var promise = this.GetIdStatByTime(this.global_.data_name, this.attribute, this.time_step, this.self_index);
      promise.then((response) => {
        this.val = response.data;
      })
    },
    reCal() {
      if (this.is_not_prepared()) return ;
      this.getData();
    },
    handleCommand(command) {
      this.self_index = command;
      if (this.is_not_prepared()) return ;
      this.getData();
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
