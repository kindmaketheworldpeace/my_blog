<template>
    <div class="bk-cmdb-search-content">
        <!-- agent状态 -->
        <div class="bk-form-content">
            <bk-selector
                :list="agentStatusList"
                :selected.sync="formInfo.agent"
                :searchable="true"
                :placeholder="formInfo.agentPlace"
                :allow-clear="true"
                @item-selected="changeAgent">
            </bk-selector>
        </div>
        <!-- 操作系统 -->
        <div class="bk-form-content">
            <bk-selector
                :list="operatList"
                :selected.sync="formInfo.operat"
                :searchable="true"
                :placeholder="formInfo.operatPlace"
                :allow-clear="true"
                @item-selected="changeOperat">
            </bk-selector>
        </div>
        <!-- 网络区域 -->
        <div class="bk-form-content">
            <bk-selector
                :list="networkList"
                :selected.sync="formInfo.network"
                :searchable="true"
                :placeholder="formInfo.networkPlace"
                :allow-clear="true"
                @item-selected="changeNetwork">
            </bk-selector>
        </div>
        <!-- IP -->
        <div class="bk-form-content bk-form-margin">
            <input
                type="text"
                class="bk-form-input"
                placeholder="请输入服务名称"
                v-model="formInfo.ip"
                @keyup.enter="searchIp">
            <i class="bk-icon icon-search" @click="searchIp"></i>
            <i class="bk-icon icon-close bk-selector-icon clear-icon" @click="clearInfo"></i>
        </div>
	</div>
</template>

<script>
    export default {
        name: 'cmdbSearch',
        data () {
            return {
                agentStatusList: [
                    {name: 'Agent正常', id: 1},
                    {name: 'Agent异常', id: 2}
                ],
                operatList: [
                    {name: 'Windows', id: 'WINDOWS'},
                    {name: 'Linux', id: 'LINUX'},
                    {name: 'AIX', id: 'AIX'}
                ],
                networkList: [
                    {name: 'Jacobston', id: 'Jacobston'},
                    {name: 'Bayerstad', id: 'Bayerstad'},
                    {name: 'Pascalemouth', id: 'Pascalemouth'}
                ],
                formInfo: {
                    agent: '',
                    agentPlace: '请选择',
                    operat: '',
                    operatPlace: '请选择操作系统',
                    network: '',
                    networkPlace: '请选择网络区域',
                    ip: ''
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
            changeAgent (id, data) {
                console.log(id, data)
            },
            changeOperat (id, data) {
                console.log(id, data)
            },
            changeNetwork (id, data) {
                console.log(id, data)
            },
            searchIp () {

            },
            clearInfo () {

            }
        }
    }
</script>

<style lang="scss" scoped>
    @import '../../../scss/mixins/clearfix.scss';
    @import '../../../scss/mixins/scroller.scss';
    .bk-cmdb-search-content {
        @include clearfix;
        .bk-form-content {
            float: left;
            width: 25%;
            padding-right: 20px;
            position: relative;
            &:hover {
                .icon-search {
                    display: none;
                }
                .clear-icon {
                    display: block;
                }
            }
            .icon-search {
                position: absolute;
                right: 0px;
                top: 2px!important;
                padding: 10px;
                cursor: pointer;
                color: #C3CDD7;
            }
            .bk-selector-icon {
                top: 10px!important;
            }
            .clear-icon {
                display: none;
            }
        }
        .bk-form-margin {
            padding-right: 0;
        }
    }
</style>
