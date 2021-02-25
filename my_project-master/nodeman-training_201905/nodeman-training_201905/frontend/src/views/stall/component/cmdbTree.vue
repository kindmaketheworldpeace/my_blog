<template>
    <ul class="child-node">
        <li class="vue-tree-item" v-for="(item, index) in treeDataList" :key="index">
            <div :class="['tree-node',{'down':item.showChildren,'set-frist-pLeft': treeIndex + 1 === 1,'active': item.showBackground}]" 
                :style="pLeft" @click="toggleChildren(item)">
                <p class="unfold-icon">
                    <i :class="['tree-file',{'bk-icon icon-right-shape':!item.showChildren, 'bk-icon icon-down-shape':item.showChildren}]"></i>
                    <i class="bk-icon icon-plus-square-shape"></i>
                </p>
                <span :class="['name-text', {'chang-width': treeIndex + 1 >= 3}, {'set-width': treeIndex + 1 >= 7}]">{{item.name}}</span>
                <!-- <i :class="['check-icon', {'icon-user-sure': item.checkInfo}]" @click.stop="checkItem(item)"></i> -->
            </div>
            <cmdbTree
                v-if="item.showChildren && item.children"
                :treeDataList="item.children"
                :treeIndex="treeIndex + 1"
                @selectItem = "selectItem"
                @toggle="toggle">
            </cmdbTree>
        </li>
    </ul>
</template>
<script>
export default {
    name: 'cmdbTree',
    props: {
        treeDataList: {
            type: Array,
            default: []
        },
        treeIndex: {
            type: Number,
            default: 0
        }
    },
    data () {
        return {
            pLeft: `padding-left:${15 * (this.treeIndex + 1)}px;`
        }
    },
    methods: {
        // 展开子级
        toggleChildren (item) {
            this.$emit('toggle', item)
        },
        toggle (item) {
            this.$emit('toggle', item)
        },
        // 复选框勾选的数据
        checkItem (item) {
            this.$emit('selectItem', item)
        },
        // 组件内调用组件，需要抛出数据两次
        selectItem (item) {
            this.$emit('selectItem', item)
        }
    }
}
</script>

<style  lang="scss" scoped>
    @import '../stallScss/cmdbTree.scss';
</style>

