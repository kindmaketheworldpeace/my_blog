<template>
    <div class="bk-cloud-area-table">
        <div class="bk-table-div">
            <table class="bk-table has-table-bordered has-table-hover">
                <thead>
                    <tr>
                        <th>云区域</th>
                        <th>云区域 ID</th>
                        <th>Proxy节点数</th>
                        <th>主机数</th>
                        <th>业务数</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                <template v-if="cloudList.length">
                    <tr v-for="(item, index) in cloudList">
                        <td>
                            <span class="bk-tab-cursor bk-lable-primary"
                                @click="seeCloudContent(item)">
                                {{item.bk_cloud_name}}
                            </span>
                            <i class="bk-icon icon-eye"></i>
                            <i class="bk-icon icon-eye-slash"></i>
                        </td>
                        <td>
                            <span>{{item.bk_cloud_id}}</span>
                        </td>
                        <td>
                            <span>{{item.proxy}}</span>
                        </td>
                        <td>
                            <span>{{item.hostsNum}}</span>
                        </td>
                        <td>
                            <span>{{item.businessNum}}</span>
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
                cloudList: [
                    {bk_cloud_name: '测试', bk_cloud_id: '2', proxy: 236, hostsNum: 100, businessNum: 100}
                ],
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
            
        },
        computed: {
            
        },
        watch: {
            
        },
        mounted () {
            
        },
        methods: {
            pageChange () {

            },
            // 查看云区域详情
            seeCloudContent (item) {
                const id = item.bk_cloud_id
                this.$parent.seeCloud(id)
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