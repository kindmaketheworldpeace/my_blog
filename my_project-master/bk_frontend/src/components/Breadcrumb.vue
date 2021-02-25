<template>
  <div class="bread-crumb">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item
        v-for="(item, index) in to"
        :key="index"
        :to="{ path: item.path }">
        {{item.displayName}}
      </el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>
<script>
/**
 * breadcrumb
 * @desc 面包屑组件
 * @param to {Array} 面包屑数据对象
 * @example <breadcrumb :to="to"></breadcrumb>
 */
  export default {
    props: {
      to: {
        type: Array,
        default: () => []
      }
    }
  }
</script>
