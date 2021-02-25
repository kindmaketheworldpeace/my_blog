<template>
    <div class="bk-cmdb-table-info">
        <div class="bk-table-div">
            <table class="bk-table has-table-bordered has-table-hover">
                <thead>
                    <tr>
                        <th v-if="cmdbList.length">
                            <label class="bk-form-checkbox">
                                <input 
                                    type="checkbox" 
                                    name="checkboxOne" 
                                    :checked="allCheck" 
                                    @click="checkAll">
                            </label>
                        </th>
                        <th>内网 IP</th>
                        <th>外网 IP</th>
                        <th>Agent状态</th>
                        <th>操作系统</th>
                        <th>所属区域</th>
                        <th>维护负责人</th>
                    </tr>
                </thead>
                <tbody>
                <template v-if="cmdbList.length">
                    <tr v-for="(item, index) in cmdbList">
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
                            <span>{{item.conn_ip}}</span>
                        </td>
                        <td>
                            <span>{{item.outer_ip}}</span>
                        </td>
                        <td>
                            <span>{{item.status}}</span>
                        </td>
                        <td>
                            <span>{{item.os_type}}</span>
                        </td>
                        <td>
                            <span>{{item.area}}</span>
                        </td>
                        <td>
                            <span>{{item.account}}</span>
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
	</div>
</template>

<script>
    export default {
        name: 'cmdbTable',
        data () {
            return {
                cmdbList: [
                    // {conn_ip: '117.179.59.76', outer_ip: '111.15.95.100', status: 'SUCCESS', os_type: 'Linux', area: 'Jacobston', account: 'yunyaoyang', check: false},
                    // {conn_ip: '61.140.229.130', outer_ip: '116.224.119.81', status: 'SUCCESS', os_type: 'AIX', area: 'Bayerstad', account: 'v_yuwchen', check: false}
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
                }
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
            // 分页
            pageChange () {

            },
            checkAll () {
                this.allCheck = !this.allCheck
                this.cmdbList.forEach(item => {
                    item.check = this.allCheck
                })
                if (this.allCheck) {
                    for (let i = 0; i < this.cmdbList.length; i++) {
                        let val = true
                        for (let j = 0; j < this.checkList.length; j++) {
                            if (this.cmdbList[i].id === this.checkList[j].id) {
                                val = false
                                break
                            }
                        }
                        if (val) {
                            this.checkList.push(this.cmdbList[i])
                        }
                    }
                } else {
                    for (let i = this.checkList.length - 1; i >= 0; i--) {
                        for (let j = 0; j <= this.cmdbList.length - 1; j++) {
                            if (this.checkList[i] && this.checkList[i].id === this.cmdbList[j].id) {
                                this.checkList.splice(i, 1)
                            }
                        }
                    }
                }
                this.cmdbList = JSON.parse(JSON.stringify(this.cmdbList))
            },
            checkOne (item, index) {
                item.check = !item.check
                this.allCheck = !this.cmdbList.some(item => {
                    return !item.check
                })
                this.cmdbList = JSON.parse(JSON.stringify(this.cmdbList))
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
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import '../../../scss/mixins/clearfix.scss';
    @import '../../../scss/mixins/scroller.scss';
    @import '../../../scss/mixins/table.scss';
    .bk-cmdb-table-info {
        border-top: 1px solid #c3cdd7;
        @include table;
    }
</style>
