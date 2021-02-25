<template>
    <div class="bk-cloud-area-management">
        <!-- 云区域列表 -->
        <template v-if="!cloudId">
            <!-- button -->
            <div class="bk-add-cloud">
                <bk-button 
                    type="primary" 
                    title="添加云区域"
                    @click="openDictionary">
                    <i class="bk-icon icon-plus"></i>添加云区域
                </bk-button>
            </div>
            <div class="bk-cloud-table">
                <cloud-table></cloud-table>
            </div>
        </template>
        <!-- 单个云区域详情 -->
        <template v-else>
            <div class="bk-add-cloud">
                <bk-button type="default" title="返回云区域" @click="backCloudArea">
                    <i class="bk-icon icon-arrows-left"></i>返回云区域
                </bk-button>
                <div style="float: right;">
                    <bk-button 
                        type="primary" 
                        title="添加云区域"
                        @click="openDictionary">
                        <i class="bk-icon icon-plus"></i>添加云区域
                    </bk-button>
                    <bk-button type="default" title="批量操作">
                        批量操作
                    </bk-button>
                </div>
            </div>
            <div class="bk-cloud-table" v-if="cloudId">
                <cloud-content
                    :cloudId="cloudId"></cloud-content>
            </div>
        </template>
        <!-- 添加云区域 -->
        <div class="bk-dialog-form" v-if="dictDataTable.showDialog">
            <bk-dialog
                :is-show.sync="dictDataTable.showDialog"
                :quick-close="false"
                :draggable="true"
                width="480"
                :title="dictDataTable.title"
                @confirm="submitDictionary"
                @cancel="closeDictionary">
                <div slot="content" style="padding: 0;">
                    <div class="bk-content-message">
                        <i class="bk-icon icon-exclamation-circle-shape "></i>
                        <span>云区域ID由系统自动生成</span>
                    </div>
                    <form class="bk-form">
                        <div class="bk-form-content" style="margin-left: 0">
                            <!-- <p class="bk-form-p">编码 <span class="bk-p-xin">*</span></p> -->
                            <input
                                type="text"
                                class="bk-form-input"
                                v-model.trim="dictDataTable.name"
                                placeholder="请输入云区域名称">
                            <!-- <p class="bk-error-msg">提示错误</p> -->
                        </div>
                    </form>
                </div>
            </bk-dialog>
        </div>
	</div>
</template>

<script>
    import cloudTable from './cloudTable.vue'
    import cloudContent from './cloudContent.vue'
    export default {
        components: {
            cloudTable,
            cloudContent
        },
        data () {
            return {
                // 云区域ID
                cloudId: '',
                // 新增云区域
                dictDataTable: {
                    showDialog: false,
                    title: '添加云区域',
                    name: ''
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
            // 查看云区域详情
            seeCloud (value) {
                this.cloudId = value
            },
            // 返回云区域
            backCloudArea () {
                this.cloudId = ''
            },
            // 新增云区域
            openDictionary () {
                this.dictDataTable.showDialog = true
            },
            submitDictionary () {

            },
            closeDictionary () {
                this.dictDataTable.showDialog = false
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import '../../../scss/mixins/clearfix.scss';
    @import '../../../scss/mixins/scroller.scss';
    .bk-add-cloud {
        height: 72px;
        line-height: 72px;
        background-color: #FAFBFD;
        @include clearfix;
        .icon-plus,
        .icon-arrows-left {
            color: #fff;
            font-weight: bold;
            margin-right: 5px;
        }
        .icon-arrows-left {
            color: #3A84FF;
        }
        .bk-button {
            height: 36px;
            line-height: 36px;
            font-size: 14px;
        }
    }
    .bk-dialog-form {
        .bk-content-message {
            color: #63656E;
            font-size: 12px;
            line-height: 16px;
            .bk-icon {
                color: #C4C6CC;
            }
        }
        .bk-form {
            padding: 20px 0;
        }
    }
</style>