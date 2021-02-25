<template>
    <div class="editChange">
        任务名称：
        <el-input v-model="changeName" placeholder="请输入任务名称"></el-input>
        所属标段：
        <el-select v-model="tender" placeholder="请选择">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
      </el-select>
        变更类型：
        <el-radio v-model="changeType" label="1">常规变更</el-radio>
        <el-radio v-model="changeType" label="2">自定义变更</el-radio>
        系统类型：
        <el-radio v-model="systemType" label="3">windows</el-radio>
        <el-radio v-model="systemType" label="4">linux</el-radio>
        <div id="changeDetail">
            变更场景：
            <el-select v-model="changeScene" placeholder="请选择">
    <el-option
      v-for="item in options"
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
        name: 'editChange',
        data() {
            return {
                changeName: '',
                changeScene: '',
                changeType: '1',
                systemType: '2',
                tender: '',
                options: [{
                    value: '选项1',
                    label: '标段一--嘉为'
                }, {
                    value: '选项2',
                    label: '标段二--灵通'
                }, {
                    value: '选项3',
                    label: '标段三--康拓扑'
                }],
            }
        }
    }
</script>

<style scoped>
 #changeDetail{
     border: 2px solid slateblue;
     width: 600px;
     height: 400px;
 }
</style>
