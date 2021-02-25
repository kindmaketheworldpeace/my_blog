<template>
    <div class="bk-cloud-area-table">
        <div class="bk-table-div">
            <table class="bk-table has-table-bordered has-table-hover">
                <thead>
                    <tr>
                        <th v-if="machineList.length">
                            <label class="bk-form-checkbox">
                                <input 
                                    type="checkbox" 
                                    name="checkboxOne" 
                                    :checked="allCheck" 
                                    @click="checkAll">
                            </label>
                        </th>
                        <th>云区域（ID）</th>
                        <th>登录 IP</th>
                        <th>节点类型</th>
                        <th>Agent版本</th>
                        <th>节点负载</th>
                        <th>更新时间</th>
                        <th>任务状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                <template v-if="machineList.length">
                    <tr v-for="(item, index) in machineList">
                        <td>
                            <label class="bk-form-checkbox">
                                <input
                                    type="checkbox"
                                    name="checkbox"
                                    :checked="item.check"
                                    @click="checkOne(item, index)">
                            </label>
                        </td>
                        <td>
                            <span>{{item.bk_cloud_name}} ({{item.bk_cloud_id}})</span>
                        </td>
                        <td>
                            <span>{{item.conn_ip}}</span>
                        </td>
                        <td>
                            <span>{{item.node_type}}</span>
                        </td>
                        <td>
                            <span>{{item.version}}</span>
                        </td>
                        <td>
                            <span>123</span>
                        </td>
                        <td>
                            <span>{{item.update_time}}</span>
                        </td>
                        <td>
                            <span>{{item.status}}</span>
                        </td>
                        <td>
                            <span class="bk-tab-cursor bk-lable-primary" style="margin-right: 10px;">编辑</span>
                            <span class="bk-tab-cursor bk-lable-primary" @click="openDeletePopover(item)">删除</span>
                        </td>
                    </tr>
                </template>
                <template v-else>
                    <tr v-cloak>
                        <td colspan="10" class="pagesize">
                            <div class="bk-result">
                                <img src="../../../images/box.png">
                                <div class="bk-page-info">
                                    <p class="bk-p-black">
                                        暂无数据
                                    </p>
                                </div>
                            </div>
                        </td>
                    </tr>
                </template>
                </tbody>
            </table>
        </div>
        <div class="bk-page-info">
            <div class="bk-size-info">
                共计{{customPaging.count}}条<span style="margin: 0 10px;">每页</span>
                <div class="bk-form-content">
                    <bk-selector
                        :list="customPaging.pageList"
                        :selected.sync="customPaging.pagesize">
                    </bk-selector>
                </div><span style="margin-left: 10px;">条</span>
            </div>
            <bk-paging
                v-if="customPaging.total_page !== 1"
                :cur-page.sync="customPaging.page"
                :total-page="customPaging.total_page"
                :size="'small'"
                @page-change="pageChange"
                :type="'compact'"
                class="bk-page-size">
            </bk-paging>
        </div>
        <!-- 删除 -->
        <div class="bk-popup-delete" v-if="deleteInfo.show">
            <bk-dialog
                :is-show.sync="deleteInfo.show"
                :quick-close="false"
                :draggable="true"
                :title="deleteInfo.title"
                :content="deleteInfo.content"
                @confirm="submitDelete"
                @cancel="closeDelete">
            </bk-dialog>
        </div>
	</div>
</template>

<script>
    export default {
        components: {
            
        },
        data () {
            return {
                machineList: [
                    {bk_cloud_name: '测试', bk_cloud_id: '2', conn_ip: '111.15.95.100', node_type: 'Proxy', version: '1.60.20', update_time: '2018-01-19 14:43:16', status: 'SUCCESS', check: false}
                ],
                // 全选
                allCheck: false,
                checkList: [],
                // 分页
                customPaging: {
                    count: 15,
                    total_page: 2,
                    page: 1,
                    pagesize: 10,
                    pageList: [
                        {id: 10, name: 10},
                        {id: 20, name: 20},
                        {id: 30, name: 30},
                        {id: 50, name: 50}
                    ]
                },
                // 删除确认
                deleteInfo: {
                    show: false,
                    info: {},
                    title: '确认删除',
                    content: '删除操作会影响！'
                }
            }
        },
        props: {
            cloudId: {
                type: [String, Number],
                default: ''
            }
        },
        computed: {
            
        },
        watch: {
            
        },
        mounted () {
            console.log(this.cloudId)
        },
        methods: {
            pageChange () {

            },
            checkAll () {
                this.allCheck = !this.allCheck
                this.machineList.forEach(item => {
                    item.check = this.allCheck
                })
                if (this.allCheck) {
                    for (let i = 0; i < this.machineList.length; i++) {
                        let val = true
                        for (let j = 0; j < this.checkList.length; j++) {
                            if (this.machineList[i].id === this.checkList[j].id) {
                                val = false
                                break
                            }
                        }
                        if (val) {
                            this.checkList.push(this.machineList[i])
                        }
                    }
                } else {
                    for (let i = this.checkList.length - 1; i >= 0; i--) {
                        for (let j = 0; j <= this.machineList.length - 1; j++) {
                            if (this.checkList[i] && this.checkList[i].id === this.machineList[j].id) {
                                this.checkList.splice(i, 1)
                            }
                        }
                    }
                }
                this.machineList = JSON.parse(JSON.stringify(this.machineList))
            },
            checkOne (item, index) {
                item.check = !item.check
                this.allCheck = !this.machineList.some(item => {
                    return !item.check
                })
                this.machineList = JSON.parse(JSON.stringify(this.machineList))
                if (item.check) {
                    this.checkList.push(item)
                } else {
                    for (let i = 0; i < this.checkList.length; i++) {
                        if (item.id === this.checkList[i].id) {
                            this.checkList.splice(i, 1)
                            break
                        }
                    }
                }
            },
            // 删除
            openDeletePopover (item) {
                this.deleteInfo.show = true
                this.deleteInfo.info = item
            },
            submitDelete () {

            },
            closeDelete () {
                this.deleteInfo.show = false
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import '../../../scss/mixins/clearfix.scss';
    @import '../../../scss/mixins/scroller.scss';
    @import '../../../scss/mixins/table.scss';
    .bk-cloud-area-table {
        border: 1px solid #c3cdd7;
        border-bottom: none;
        @include table;
        .icon-eye,
        .icon-eye-slash {
            font-size: 14px;
        }
    }
</style>