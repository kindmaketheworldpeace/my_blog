<template>
    <div>
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="select_scene">
            <el-menu-item v-for="i in test" :key="i.id" index="2">{{i.text}}</el-menu-item>
        </el-menu>
        <el-button type="text" @click="create()">新建规则</el-button>
        <el-button type="text">优先级排序</el-button>
        <el-divider></el-divider>
        <div class="table">
            <el-table
                    :data="tableData"
                    height="100%"
                    border
                    style="width: 100%">
                <el-table-column
                        fixed
                        prop="id"
                        label="编号"
                        width="150">
                </el-table-column>
                <el-table-column
                        prop="name"
                        label="场景名称">
                </el-table-column>
                <el-table-column
                        prop="os_type"
                        label="系统类型"
                        width="120">
                </el-table-column>
                <el-table-column
                        prop="create_at"
                        label="创建时间"
                        width="300">
                </el-table-column>
                <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                    <template slot-scope="scope">
                        <el-button @click="detail_scene(scope.row)" type="text" size="small">详情</el-button>
                        <el-button @click="modify_scene(scope.row)" type="text" size="small">编辑</el-button>
                        <el-button type="text" size="small" @click="delete_scene(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <pagination
                :total="totalNumber"
                @page-size-change="pageSizeChange">
        </pagination>
        <!--<new-edit ref="newEdit" :title="title" @handle-success="handleSuccess" dialog-action="dialogAction"
                  :width="width">
            <div slot="dialog-content">
                <el-tabs v-model="activeName" :before-leave="leaveTab">

                        <el-form ref="refformGroups" :label-position="labelPosition" label-width="120px"
                                 :model="formGroups" :rules="rulesGroups">
                            <el-form-item label="规则名称" prop="name">
                                <el-input class="form-content" size="mini" v-model="formGroups.name"></el-input>
                            </el-form-item>
                            <el-form-item label="状态" prop="display_name">
                                <el-input class="form-content" size="mini" v-model="formGroups.display_name"></el-input>
                            </el-form-item>
                        </el-form>
                </el-tabs>
            </div>
        </new-edit>-->
    </div>
</template>
<script>
    import Container from '../../components/layout/container';
    import Pagination from '@/components/Pagination'
    import NewEdit from '@/components/NewEdit'

    export default {
        components: {'pagination': Pagination, 'new-edit': NewEdit},
        data() {
            return {
                totalNumber: 0,
                currentPage: 1,
                pageSize: 10,
                tableData: [],
                activeIndex: '1',
                test: [{id: 1, text: '标段一'}, {id: 2, text: '标段二'}]
            }
        },
        created() {
            this.get_service_privider()
            this.get_rule()
        },
        methods: {

            get_service_privider() {
                let params = {}
                this.$store.dispatch('serviceprivider/getServicePrivider', params).then(res => {
                        this.tableData = res.data.items
                    }
                )
            },
            pageSizeChange(val) {
                this.currentPage = val.currentPage
                this.pageSize = val.pageSize
                this.get_rule({page: this.currentPage, page_size: this.pageSize})
            },
            create() {
                this.$router.replace('/create_rule')
            },
            get_rule(par) {
            },
            detail_rule() {
            },
            modify_rule(row) {
            },
            delete_rule(row) {
            },
            get_rule_by_name() {
            },
            select_scene() {
            }
        }
    }
</script>
<style lang='scss'>
    .table {
        height: calc(100% - 180px);
        .el-table {
            border-top: 1px solid rgb(235, 238, 245);
        }
    }
</style>
