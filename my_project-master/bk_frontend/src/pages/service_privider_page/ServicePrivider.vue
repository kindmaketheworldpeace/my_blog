<template>
    <div class="service_privider">
        <div class="fitter">
                <div style="width: 30%;display: inline-block">
                    <el-input size="medium" placeholder="请输入运维单位" v-model="name" class="input-with-select">
                        <el-button slot="append" @click="get_service_privider_by_name()"
                                   icon="el-icon-search"></el-button>
                    </el-input>
                </div>
                <div style="float: right;">
                    <el-button type="primary" @click="create()">新建标段</el-button>
                </div>
        </div>
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
                        prop="description"
                        label="名称">
                </el-table-column>
                <el-table-column
                        prop="name"
                        label="运维单位"
                        width="120">
                </el-table-column>
                <el-table-column
                        prop="checkers"
                        label="技术复核"
                        width="300">
                </el-table-column>
                <el-table-column
                        prop="approvers"
                        label="管理复核"
                        width="300">
                </el-table-column>

                <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                    <template slot-scope="scope">
                        <el-button @click="modify(scope.row)" type="text" size="small">编辑</el-button>
                        <el-button type="text" size="small" @click="delete_service_privider(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <pagination
                :total="totalNumber"
                @page-size-change="pageSizeChange">
        </pagination>
        <el-dialog
                title="新建标段"
                :visible.sync="centerDialogVisible"
                width="30%"
                center>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>名称：</span>
                </div>
                <el-input style="width: 70%" v-model="description" placeholder="请输入内容"></el-input>
            </div>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>运维单位：</span>
                </div>
                <el-input style="width: 70%" v-model="name" placeholder="请输入内容"></el-input>
            </div>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>技术复核：</span>
                </div>
                <el-select v-model="checkers" multiple placeholder="请选择">
                    <el-option
                            v-for="item in bk_user"
                            :key="item.bk_username"
                            :label="item.bk_username"
                            :value="item.bk_username">
                    </el-option>
                </el-select>
            </div>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>管理复核：</span>
                </div>
                <el-select v-model="approvers" multiple placeholder="请选择">
                    <el-option
                            v-for="item in bk_user"
                            :key="item.bk_username"
                            :label="item.bk_username"
                            :value="item.bk_username">
                    </el-option>
                </el-select>
            </div>
            <span slot="footer" class="dialog-footer">
    <el-button @click="centerDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="create_service_privider()">确 定</el-button>
  </span>
        </el-dialog>
        <el-dialog
                title="编辑标段"
                :visible.sync="modify_centerDialogVisible"
                width="30%"
                center>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>名称：</span>
                </div>
                <el-input style="width: 70%" v-model="description" placeholder="请输入内容"></el-input>
            </div>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>运维单位：</span>
                </div>
                <el-input style="width: 70%" v-model="name" placeholder="请输入内容"></el-input>
            </div>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>技术复核：</span>
                </div>
                <el-input style="width: 70%" v-model="checkers" placeholder="请输入内容"></el-input>
            </div>
            <div style="margin-top: 15px">
                <div style="width: 25%;display:inline-block">
                    <span>管理复核：</span>
                </div>
                <el-input style="width: 70%" v-model="approvers" placeholder="请输入内容"></el-input>
            </div>
            <span slot="footer" class="dialog-footer">
    <el-button @click="modify_centerDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="modify_service_privider()">确 定</el-button>
  </span>
        </el-dialog>
    </div>

</template>
<script>
    import Container from '../../components/layout/container';
    import Pagination from '@/components/Pagination'

    export default {
        components: {'pagination': Pagination},
        data() {
            return {
                totalNumber: 0,
                currentPage: 1,
                pageSize: 10,
                centerDialogVisible: false,
                modify_centerDialogVisible: false,
                tableData: [],
                name: '',
                description: '',
                checkers: '',
                approvers: '',
                id: '',
                bk_user: [],
            }
        },
        created() {
            this.get_service_privider()
            this.get_bk_user()
        },
        methods: {
            get_bk_user() {
                let params = {}
                this.$store.dispatch('serviceprivider/get_bk_user', params).then(res => {
                        this.bk_user = res.data
                        console.log(this.bk_user)
                    }
                )
            },
            create() {
                this.centerDialogVisible = true
                this.id = ''
                this.name = ''
                this.description = ''
                this.checkers = ''
                this.approvers = ''
            },
            pageSizeChange(val) {
                this.currentPage = val.currentPage
                this.pageSize = val.pageSize
                this.get_service_privider({page: this.currentPage, page_size: this.pageSize})
            },
            delete_service_privider(row) {
                let params = {
                    id: row.id
                }
                this.$store.dispatch('serviceprivider/deleteServicePrivider', params).then(res => {
                        this.get_service_privider()
                    }
                )
            },
            create_service_privider() {
                let params = {
                    id: this.id,
                    name: this.name,
                    description: this.description,
                    checkers: this.checkers,
                    approvers: this.approvers
                }
                this.$store.dispatch('serviceprivider/createServicePrivider', params).then(res => {
                        this.get_service_privider()
                        this.centerDialogVisible = false
                    }
                )
            },
            modify_service_privider() {
                let params = {
                    id: this.id,
                    name: this.name,
                    description: this.description,
                    checkers: this.checkers,
                    approvers: this.approvers
                }
                // params = Object.assign(params, apiParam)
                this.$store.dispatch('serviceprivider/modifyServicePrivider', params).then(res => {
                        this.get_service_privider()
                        this.modify_centerDialogVisible = false
                    }
                )
            },
            modify(row) {
                this.modify_centerDialogVisible = true
                this.id = row.id
                this.name = row.name
                this.description = row.description
                this.checkers = row.checkers
                this.approvers = row.approvers
            },
            get_service_privider_by_name() {
                this.get_service_privider()
            },
            get_service_privider(apiParam) {
                let params = {
                    page: this.currentPage,
                    page_size: this.pageSize,
                    name__contains: this.name
                }
                params = Object.assign(params, apiParam)
                this.$store.dispatch('serviceprivider/getServicePrivider', params).then(res => {
                        this.totalNumber = res.data.count
                        this.tableData = res.data.items
                        console.log(this.tableData)
                    }
                )
            }
        }

    }
</script>
<style lang='scss'>
    span {
    }

    .service_privider {
        height: 100%;
        padding: 15px 20px 0 20px;
        background: #fff;
    }

    .new {
        height: 100%;
        padding: 15px 20px 0 20px;
        background: #fff;
        #self_chart {
            width: 500px;
            height: 500px;
        }
    }

    .table {
        height: calc(100% - 180px);
        .el-table {
            border-top: 1px solid rgb(235, 238, 245);
        }
    }
</style>
