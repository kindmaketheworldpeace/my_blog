<template>
    <div class="service_privider">
        <div class="fitter">
            <div style="width: 30%;display: inline-block">
                <el-input size="medium" placeholder="请输入场景名称" v-model="name" class="input-with-select">
                    <el-button slot="append" @click="get_scene_by_name()"
                               icon="el-icon-search"></el-button>

                </el-input>
            </div>
            <div style="float: right;">
                <el-button type="primary" @click="create()">新建场景</el-button>
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
                >
                </el-table-column>
                <el-table-column
                        prop="name"
                        label="场景名称">
                </el-table-column>
                <el-table-column
                        prop="os_type"
                        label="系统类型"
                >
                </el-table-column>
                <el-table-column
                        prop="create_at"
                        label="创建时间"
                >
                </el-table-column>
                <el-table-column
                        fixed="right"
                        label="操作"
                >
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
        <new-edit ref="newEdit" :title="title" @handle-success="handleSuccess" dialog-action="dialogAction"
                  :width="width">
            <div slot="dialog-content">
                <el-tabs v-model="activeName">
                    <el-form ref="refformScene" :label-position="labelPosition" label-width="120px"
                             :model="formScene" :rules="rulesScene">
                        <el-form-item label="场景名称" prop="name">
                            <el-input class="form-content" size="mini" v-model="formScene.name"></el-input>
                        </el-form-item>
                        <el-form-item label="系统类型" prop="os_type">
                            <el-input class="form-content" size="mini" v-model="formScene.os_type"></el-input>
                        </el-form-item>
                        <el-form-item label="所属标段">
                            <el-select v-model="formScene.service_privider" placeholder="请选择">
                                <el-option
                                        v-for="item in options"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="状态">
                            <el-input class="form-content" type="textarea" v-model="formScene.desc"></el-input>
                        </el-form-item>
                    </el-form>
                </el-tabs>
            </div>
        </new-edit>
    </div>
</template>
<script>
    import Container from '../../components/layout/container';
    import Pagination from '@/components/Pagination'
    import NewEdit from '@/components/NewEdit'
    import * as commonValidate from '@/common/js/validate'

    export default {
        components: {'pagination': Pagination, 'new-edit': NewEdit},
        data() {
            return {
                width: '%40',
                title: '',
                totalNumber: 0,
                currentPage: 1,
                pageSize: 10,
                labelPosition: 'right',
                activeName: 'first',
                dialogAction: '',
                tableData: [],
                rulesScene: {
                    name: [
                        {required: true, message: '请输入场景名称'},
                        {max: 20, message: '长度在20个字符之内'},
                        {validator: commonValidate.validateNameUnderline}
                    ],
                    display_name: [
                        {required: true, message: '请输入显示名'},
                        {max: 14, message: '长度在14个字符之内'},
                        {validator: commonValidate.validateChName}
                    ],
                },
                name: '',
                formScene: {
                    name: '',
                    os_type: '',
                    desc: '',
                },
                options: ''
            }
        },
        created() {
            this.get_scene()
        },
        methods: {
            pageSizeChange(val) {
                this.currentPage = val.currentPage
                this.pageSize = val.pageSize
                this.get_scene({page: this.currentPage, page_size: this.pageSize})
            },
            leaveTab(val) {
                let res = true
                this.$refs.refScene.validate((valid) => {
                    if (!valid) {
                        res = false
                    } else {
                        res = true
                    }
                })
                return res
            },
            handleSuccess(dialogAction) {
            },
            create() {
                this.$router.replace('/create_scene')
            },
            get_scene(apiParam) {
                let params = {
                    name: this.name
                }
                params = Object.assign(params, apiParam)
                this.$store.dispatch('scene/getScene', params).then(res => {
                        this.totalNumber = res.data.count
                        this.tableData = res.data.items
                    }
                )
            },
            detail_scene() {
            },
            modify_scene(row) {
                this.title = '编辑场景'
                this.$refs['newEdit'].open()
            },
            delete_scene(row) {
                let params = {
                    id: row.id
                }
                this.$store.dispatch('scene/deleteScene', params).then(res => {
                     this.get_scene()
                    }
                )
            },
            get_scene_by_name() {
                this.get_scene()
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
