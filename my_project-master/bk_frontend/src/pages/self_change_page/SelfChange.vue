<template>
  <div class="selfChange">
        <div><span>任务名称:</span><el-input v-model="changeName" placeholder="请输入内容" style="margin-left: 5px;width: 180px"></el-input>
        </div>
      <div style="margin-top: 10px">
          <span>所属标段</span>
          <el-select v-model="tender" placeholder="请选择服务商" style="margin-left: 5px">
    <el-option
      v-for="item in serverList"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
  </el-select>
      </div>
    </div>
</template>
<script>

export default {
    name: 'selfChange',
  data() {
    return {
        changeName: '',
        tender: '',
        serverList: [{
          value: '选项1',
          label: '标段一（嘉为）'
        }, {
          value: '选项2',
          label: '标段二（灵通）'
        }, {
          value: '选项3',
          label: '标段三（康拓扑）'
        }, ]
    }
  },
  created() {
    this.inntCharts()
  },
  methods: {
    inntCharts() {
      // 基于准备好的dom，初始化echarts实例
      let myCharts = this.$echarts.init(document.getElementById('self_chart'));
      // 指定图表的配置项和数据
      let option = {
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        legend: {
          data: ['销量']
        },
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [{
          name: '销量',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }]
      };
      // 使用刚指定的配置项和数据显示图表。
      myCharts.setOption(option);
    }
  },
}
</script>
<style lang='scss'>
    .selfChange{
        position: absolute;
        left:20%;
        margin-top: 10px;
    }
    span {
        font-weight: bold;
    }
</style>
