<template>
    <div class="bk-import-cmdb">
        <!-- 返回按钮 -->
        <div class="bk-cmdb-btn">
            <bk-button type="default" title="返回节点列表" @click="closeCmdb">
                <i class="bk-icon icon-arrows-left"></i>返回节点列表
            </bk-button>
        </div>
        <!-- 从cmdb导入 -->
        <div class="bk-cmdb-content">
            <!-- tree -->
            <div class="bk-cmdb-tree">
                <cmdb-tree
                    :treeDataList="treeDataList"></cmdb-tree>
            </div>
            <!-- table -->
            <div class="bk-cmdb-table">
                <!-- search -->
                <div class="bk-cmdb-table-search">
                    <cmdb-search></cmdb-search>
                </div>
                <!-- content -->
                <div class="bk-cmdb-table-content">
                    <cmdb-table></cmdb-table>
                </div>
            </div>
        </div>
        <!-- import button -->
        <div class="bk-import-button">
            <bk-button type="primary" title="导入主机">
                导入主机
            </bk-button>
            <bk-button type="default" title="安装/重装">
                安装/重装
            </bk-button>
            <bk-button type="default" title="取消">
                取消
            </bk-button>
        </div>
	</div>
</template>

<script>
    import cmdbTree from './cmdbTree.vue'
    import cmdbSearch from './cmdbSearch.vue'
    import cmdbTable from './cmdbTable.vue'
    export default {
        components: {
            cmdbTree,
            cmdbSearch,
            cmdbTable
        },
        data () {
            return {
                treeDataList: [
                    {
                        name: '蓝鲸',
                        id: 1,
                        has_children: true,
                        showChildren: true,
                        showBackground: true,
                        parent: '',
                        children: [
                            {
                                name: '空闲机',
                                id: 2,
                                has_children: false,
                                showChildren: false,
                                showBackground: false,
                                parent: 1
                            }
                        ]
                    }
                ]
            }
        },
        props: {
            
        },
        computed: {
            
        },
        watch: {
            
        },
        mounted () {
            
        },
        methods: {
            closeCmdb () {
                this.$parent.cmdbSettings.isShow = false
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import '../../../scss/mixins/clearfix.scss';
    @import '../../../scss/mixins/scroller.scss';
    /* 返回按钮 */
    .bk-cmdb-btn {
        height: 72px;
        line-height: 72px;
        background-color: #FAFBFD;
        .icon-arrows-left {
            color: #3A84FF;
            font-weight: bold;
            font-size: 14px;
            margin-right: 5px;
        }
        .bk-button {
            height: 36px;
            line-height: 36px;
        }
    }
    /* 从cmdb导入 */
    .bk-cmdb-content {
        height: 586px;
        border: 1px solid #c3cdd7;
        background-color: #FAFBFD;
        @include clearfix;
        .bk-cmdb-tree {
            float: left;
            width: 240px;
            height: 100%;
            border-right: 1px solid #c3cdd7;
            overflow-y: auto;
            @include scroller;
        }
        .bk-cmdb-table {
            float: left;
            height: 100%;
            width: calc(100% - 240px);
            overflow-y: auto;
            @include scroller;
        }
    }
    .bk-cmdb-table-search {
        padding: 21px 20px;
        background: #fff;
    }
    .bk-cmdb-table-content {
        height: calc(100% - 78px);
        width: 100%;
        overflow-y: auto;
        @include scroller;
    }
    .bk-import-button {
        text-align: center;
        margin: 20px 0;
        .bk-button {
            height: 36px;
            line-height: 36px;
            width: 86px;
            font-size: 14px;
        }
    }
</style>
