<template>
    <div class="agent-stall">
        <!-- 配置详情 -->
        <div class="bk-stall-config"  v-show="!openStatus">
            <!-- 筛选版块 -->
            <!-- <div class="bk-stall-select">
                <div class="bk-form-item mr30">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m.search.cluster')}} </label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="queryData.querySetList"
                            :setting-key="'id'"
                            :selected.sync="queryData.selectList.defaultSet"
                            :disabled="queryData.query.keyword !== '' || queryData.queryDisabled.set"
                            @item-selected="querySelected">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-form-item mr30">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m.search.modules')}} </label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="queryData.queryModuleList"
                            :selected.sync="queryData.selectList.defaultModule"
                            :disabled="queryData.isDisabled || queryData.query.keyword !== '' || queryData.queryDisabled.module"
                            @item-selected="moduleSelected">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m.search.changeCloud')}} </label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="queryData.searchCloud"
                            :selected.sync="queryData.selectList.defaultCloud"
                            :disabled="queryData.query.keyword !== '' || queryData.queryDisabled.cloud"
                            @item-selected="cloudSelected">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-form-btn">
                    <button
                        class="bk-button bk-primary"
                        :disabled="queryData.query.keyword !== '' || queryData.queryDisabled.searchBtn || (queryData.selectList.defaultSet === -1 && queryData.selectList.defaultModule === -1 && queryData.selectList.defaultCloud === -1)"
                        @click="getQueryInfo">{{$t('m.search.screen')}}
                    </button>
                </div>
                <div class="bk-form-item bk-selcet">
                    <div class="bk-form-content">
                        <input
                            type="text"
                            class="bk-form-input"
                            :placeholder="$t('m.search.searchContent')"
                            v-model="queryData.query.keyword"
                            :disabled="queryData.query.bk_cloud_id !== '' || queryData.selectList.defaultModule !== -1 || queryData.selectList.defaultSet !== -1 || queryData.queryDisabled.searchInput"
                            @keydown.enter="searchInfo">
                        <i class="bk-icon icon-search" @click="searchInfo"></i>
                    </div>
                </div>
            </div> -->
            <!-- 导航区域板块 -->
            <div class="bk-stall-tab" v-if="appId === appId" v-bkloading="{isLoading: isDataLoading}">
                <!-- 头部导航 -->
                <div class="bk-stall-tap">
                    <tabAgent :type="'fill'" v-if="!isCloudLoading" :active-name="tabName" @tab-changed="tabChanged" ref="childs">
                        <tabpanelAgent name="allarea" :title="$t('m.tabControl.allArea')" :show="!!(cloudNameList.length)" :id="''">
                            <div class="p20 bk-stall-blank">
                                <!-- <button
                                    class="bk-button bk-primary"
                                    :class="{'is-disabled': cloneNode}"
                                    :title="$t('m.tabControl.copyGood')">
                                    <span>{{$t('m.tabControl.copyGood')}}</span></button>
                                <button
                                    class="bk-button bk-primary"
                                    :class="{'is-disabled': cloneNode}"
                                    :title="$t('m.tabControl.copyBad')">
                                    <span>{{$t('m.tabControl.copyBad')}}</span></button> -->
                            </div>
                        </tabpanelAgent>
                        <tabpanelAgent name="directArea" :title="$t('m.tabControl.directArea')" :id="''" v-show="!showAreaCloud" :show="!showAreaCloud">
                            <div class="p20 bk-stall-blank">
                                <button
                                    class="bk-button bk-primary"
                                    :class="{'is-disabled': cmdbSettings.isShow}"
                                    @click="addArea">
                                    <span><i class="bk-icon icon-plus"></i> {{$t('m.tabControl.addAgent')}}</span>
                                </button>
                                <button
                                    class="bk-button bk-default"
                                    :class="{'is-disabled': addAreaAgent}"
                                    @click="openAddCmdb">
                                    <span>{{$t('m.tabControl.importCmdb')}}</span>
                                </button>
                                <button
                                    class="bk-button bk-default bk-file-btn"
                                    :class="{'is-disabled': addAreaAgent}"
                                    @click="openExcelInfo">
                                    <span>{{$t('m.addNewInfo.excelInfo')}}</span>
                                    <!-- <input v-if="!addAreaAgent" id="upload" type="file" class="bk-file-input" @change="addExcelArea" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"> -->
                                </button>
                                <!-- <button class="bk-button bk-primary is-disabled">配置更新</button>
                                <button class="bk-button bk-primary is-disabled">二进制更新</button> -->
                                <div class="bk-disabled-btn">
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.updata}"
                                        :title="$t('m.operateStep.upgrade')"
                                        @click="batchOpear('UPGRADE')">
                                        <span>{{$t('m.operateStep.upgrade')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.reset}"
                                        :title="$t('m.operateStep.reinstall')"
                                        @click="batchOpear('REINSTALL')">
                                        <span>{{$t('m.operateStep.reinstall')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.unload}"
                                        :title="$t('m.operateStep.uninstall')"
                                        @click="batchOpear('UNINSTALL')" >
                                        <span>{{$t('m.operateStep.uninstall')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.remove}"
                                        :title="$t('m.operateStep.remove')"
                                        @click="batchOpear('REMOVE')">
                                        <span>{{$t('m.operateStep.remove')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.compile}"
                                        :title="$t('m.operateStep.compile')"
                                        @click="batchOpear('SAVE', 'status')" >
                                        <span>{{$t('m.operateStep.compile')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': stopInfo.status}"
                                        :title="$t('m.operateStep.stop')"
                                        @click="openAgentAll">
                                        <span>{{$t('m.operateStep.stop')}}</span>
                                    </button>
                                </div>
                            </div>
                        </tabpanelAgent>
                        <tabpanelAgent
                            :name="item.name"
                            :title="item.bk_cloud_name"
                            :id="item.bk_cloud_id"
                            v-for="(item, index) in cloudNameList"
                            :show="item.is_visible">
                            <div class="p20 bk-stall-blank">
                                <button class="bk-button bk-primary" :class="{'is-disabled': curCloudProxyStatus.total >= 2}" @click="addProxy">
                                    <span><i class="bk-icon icon-plus"></i>{{$t('m.tabControl.addProxy')}}</span>
                                </button>
                                <button class="bk-button bk-primary" :class="{'is-disabled': curCloudProxyStatus.valid_count <= 0}" @click="addCloud">
                                    <span><i class="bk-icon icon-plus"></i>{{$t('m.tabControl.addPagent')}}</span>
                                </button>
                                <button class="bk-button bk-default" :class="{'is-disabled': addAreaAgent || curCloudProxyStatus.valid_count <= 0}" @click="openAddCmdb">
                                    <span>{{$t('m.tabControl.importCmdb')}}</span>
                                </button>
                                <!-- 批量导入 -->
                                <button
                                    class="bk-button bk-default bk-file-btn"
                                    :class="{'is-disabled': curCloudProxyStatus.valid_count <= 0}"
                                    @click="openExcelInfo">
                                    <span>{{$t('m.addNewInfo.excelInfo')}}</span>
                                    <!-- <input v-if="!curCloudProxyStatus.valid_count <= 0" id="upload" type="file" class="bk-file-input" @change="addExcelArea" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"> -->
                                </button>
                                <!-- <button class="bk-button bk-primary is-disabled">配置更新</button>
                                <button class="bk-button bk-primary is-disabled">二进制更新</button> -->
                                <div class="bk-disabled-btn">
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.updata}"
                                        :title="$t('m.operateStep.upgrade')"
                                        @click="batchOpear('UPGRADE')">
                                        <span>{{$t('m.operateStep.upgrade')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.reset}"
                                        :title="$t('m.operateStep.reinstall')"
                                        @click="batchOpear('REINSTALL')">
                                        <span>{{$t('m.operateStep.reinstall')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.unload}"
                                        :title="$t('m.operateStep.uninstall')"
                                        @click="batchOpear('UNINSTALL')" >
                                        <span>{{$t('m.operateStep.uninstall')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.remove}"
                                        :title="$t('m.operateStep.remove')"
                                        @click="batchOpear('REMOVE')">
                                        <span>{{$t('m.operateStep.remove')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': installStatus.compile}"
                                        :title="$t('m.operateStep.compile')"
                                        @click="batchOpear('SAVE', 'status')" >
                                        <span>{{$t('m.operateStep.compile')}}</span></button>
                                    <button
                                        class="bk-button bk-primary"
                                        :class="{'is-disabled': stopInfo.status}"
                                        :title="$t('m.operateStep.stop')"
                                        @click="openAgentAll">
                                        <span>{{$t('m.operateStep.stop')}}</span>
                                    </button>
                                </div>
                            </div>
                        </tabpanelAgent>
                        <!-- 云区域管理 -->
                        <tabpanelAgent :name="lastIndex" :title="$t('m.tabControl.cloudManag')">
                            <div class="bk-cloud-manage">
                                <cloud-area-manage></cloud-area-manage>
                            </div>
                            <!-- <div class="p20 bk-stall-blank bk-list-add">
                                <div class="bk-cloud-list">
                                    <ul>
                                        <li v-for="(item, index) in cloudNameList">
                                            <div v-show="!item.changeSta">
                                                <div class="bk-cloud-operate">
                                                    <p class="bk-cloud-name">{{item.bk_cloud_name}} <span style="color: #dce3ea">[{{item.bk_cloud_id}}]</span></p>
                                                    <div class="bk-cloud-icon">
                                                        <div class="bk-icon-erae">
                                                            <i class="bk-icon icon-delete" @click="deleteCloud(item)"></i>
                                                            <div class="bk-icon-delete" v-show="item.changeDel">
                                                                <p>{{$t('m.addCloud.deleteArea')}}</p>
                                                                <div>
                                                                    <button class="bk-button bk-default bk-button-mini" @click="cancelCloud(item)">
                                                                        <span>{{$t('m.clickBtn.cancel')}}</span>
                                                                    </button>
                                                                </div>
                                                                <span class="bk-cloud-squera"></span>
                                                            </div>
                                                            <div class="bk-icon-delete" v-show="item.delOpen">
                                                                <p style="line-height: 40px;">{{$t('m.addCloud.openCloud')}}</p>
                                                                <div>
                                                                    <button class="bk-button bk-primary bk-button-mini" @click="changeDelete(item)">
                                                                        <span>{{$t('m.clickBtn.confirm')}}</span>
                                                                    </button>
                                                                    <button class="bk-button bk-default bk-button-mini" @click="deleteCloud(item)">
                                                                        <span>{{$t('m.clickBtn.cancel')}}</span>
                                                                    </button>
                                                                </div>
                                                                <span class="bk-cloud-squera"></span>
                                                            </div>
                                                        </div>
                                                        <div class="bk-icon-erae">
                                                            <i class="bk-icon icon-edit" @click="changeCloud(item)"></i>
                                                        </div>
                                                        <div class="bk-icon-erae">
                                                            <i class="bk-icon icon-eye-slash" @click="changeSee(item, 'slash')" v-show="!item.is_visible"></i>
                                                            <i class="bk-icon bk-icon icon-eye" @click="changeSee(item, 'eye')" v-show="item.is_visible"></i>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="bk-cloud-info">
                                                    <span class="bk-operate-su bk-opera">{{item.hosts.RUNNING}}</span>
                                                    <span class="bk-operate-er bk-opera">{{item.hosts.TERMINATED}}</span>
                                                    <span class="bk-operate-gray bk-opera">{{item.hosts.UNKNOWN}}</span>
                                                </div>
                                            </div>
                                            <div class="bk-cloud-change" v-show="item.changeSta">
                                                <div class="bk-form-item">
                                                    <input
                                                        type="text"
                                                        class="bk-form-input"
                                                        v-model="item.bk_cloud_name">
                                                </div>
                                                <div class="bk-chang-oper">
                                                    <span @click="saveCloud(item, index)">{{$t('m.clickBtn.save')}}</span>
                                                    <span class="bk-ml10" @click="changeCloud(item)">{{$t('m.clickBtn.cancel')}}</span>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                                    <div class="bk-cloud-line" v-show="cloudNameList.length"></div>
                                    <div class="bk-cloud-add" >
                                        <p v-show="!cloudNameOpera.showAdd">
                                            <span @click="cloudAddName"><span><i class="bk-icon icon-plus"></i></span>{{$t('m.addCloud.newCloud')}}</span>
                                        </p>
                                        <div class="bk-cloud-change" v-show="cloudNameOpera.showAdd">
                                            <div class="bk-form-item">
                                                <input
                                                    type="text"
                                                    class="bk-form-input"
                                                    :placeholder="$t('m.addCloud.cloudPlace')"
                                                    v-model="addCloudName"
                                                    maxlength="64"
                                                    :class="{'bk-input-checked': verify.cloud}">
                                            </div>
                                            <div class="bk-chang-oper">
                                                <span @click="addCloudInfo">{{$t('m.clickBtn.add')}}</span>
                                                <span class="bk-ml10" @click="cloudAddName">{{$t('m.clickBtn.cancel')}}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div> -->
                        </tabpanelAgent>
                    </tabAgent>
                </div>
                <!-- 所有区域列表 -->
                <div class="bk-tab-info" v-show="tabName === 'allarea'">
                    <table class="bk-table has-table-hover">
                        <thead>
                            <tr>
                                <th style="width: 15%" class="pl30">
                                    <label class="bk-form-checkbox bk-checkbox-small bk-sple-class">
                                        <input type="checkbox" name="checkbox1" :checked="cloudStatus" @click="cloudInput" :disabled="!cloudList.length">
                                    </label>
                                    {{$t('m.headTab.area')}}
                                </th>
                                <th style="width: 10%">{{$t('m.addNode.address')}}</th>
                                <th style="width: 10%">{{$t('m.addNode.nodeType')}}</th>
                                <th style="width: 10%" class="bk-center">
                                        <span class="bk-cursor" @click="sortList('agent_status')">
                                            {{$t('m.headTab.status')}} <i class="bk-icon icon-sort"></i>
                                        </span>
                                    </th>
                                    <th style="width: 15%">
                                        <span class="bk-cursor" @click="sortList('update_time')">
                                            {{$t('m.headTab.updateTime')}} <i class="bk-icon icon-sort"></i>
                                        </span>
                                    </th>
                                <th style="width: 15%">{{$t('m.headTab.step')}}</th>
                                <th style="width: 25%" class="bk-center">{{$t('m.addNode.operation')}}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-if="cloudList.length">
                                <tr v-for="(item, index) in cloudList" >
                                    <td class="pl30" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                        <label class="bk-form-checkbox bk-checkbox-small bk-sple-class">
                                            <input
                                                type="checkbox"
                                                name="checkbox1"
                                                :checked="item.checkedBox"
                                                :disabled="!(item.doObj.stop)"
                                                @click="cloudInputValue(index, item)">
                                        </label>
                                        <div class="bk-div-class">
                                            <span v-show="item.bk_cloud_id === '0'" :class="{'bk-span-imcc': !(item.doObj.stop)}">{{$t('m.tabControl.directArea')}}</span>
                                            <span v-show="item.bk_cloud_id !== '0'" :class="{'bk-span-imcc': !(item.doObj.stop)}">{{item.cloudName?item.cloudName:'--'}}</span>
                                        </div>
                                    </td>
                                    <td :class="{'bk-span-imcc': !(item.doObj.stop)}">{{item.conn_ip}}</td>
                                    <td :class="{'bk-orgen':item.node_type === 'PROXY','bk-blue': item.node_type === 'AGENT','bk-blue': item.node_type === 'PAGENT', 'bk-span-imcc': !(item.doObj.stop)}">{{item.nodeName}}</td>
                                    <td class="bk-center" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                        <span v-if="item.status"
                                              class="bk-span-blue"
                                              :class="{'bk-span-gray': item.status[0].status === 'UNKNOWN' || item.status[0].status === 'FAILED'}">{{item.status[0].version || '--'}}</span>
                                    </td>
                                    <td :class="{'bk-span-imcc': !(item.doObj.stop)}">{{item.update_time}}</td>
                                    <td @click="openStallStep(item)" class="bk-cursor">
                                        <img class="bk-rotation bk-img-icon" src="../../images/running.png" v-show="item.job_result.status === 'QUEUE' || item.job_result.status === 'RUNNING'">
                                        <span class="status-text" :class="{'bk-span-red':item.job_result.status === 'FAILED', 'bk-span-green':item.job_result.status === 'SUCCESS'}">{{item.job_result.step}}</span>
                                        <img src="../../images/word.png" class="ml10 bk-img-icon">
                                    </td>
                                    <td class="bk-center">
                                        <a href="javascript:void(0);"
                                            :class="['bk-text-button', {'is-disabled': item.doObj.sava}]"
                                            @click="openCompileInfo('SAVE', item)">
                                        {{$t('m.operateStep.compile')}}</a>
                                        <a href="javascript:void(0);"
                                            :class="['bk-text-button', {'is-disabled': item.doObj.reinstall}]"
                                            @click="openTerm(item, 'REINSTALL')">
                                        {{$t('m.operateStep.reinstall')}}</a>
                                        <a href="javascript:void(0);"
                                            :class="['bk-text-button', {'is-disabled': item.doObj.uninstall}]"
                                            @click="openTerm(item, 'UNINSTALL')">
                                        {{$t('m.operateStep.uninstall')}}</a>
                                        <a href="javascript:void(0);"
                                            :class="['bk-text-button', {'is-disabled': item.doObj.remove}]"
                                            @click="openTerm(item, 'REMOVE')">
                                        {{$t('m.operateStep.remove')}}</a>
                                        <a href="javascript:void(0);"
                                            :class="['bk-text-button', {'is-disabled': item.doObj.stop}]"
                                            @click="openTerm(item, 'STOP')">
                                        {{$t('m.operateStep.stop')}}</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="bk-cursor pagesize" colspan="7">
                                        <div class="bk-table-page-top">
                                            <bk-paging
                                                <bk-paging
                                                :cur-page.sync="customPaging.page2"
                                                :total-page="customPaging.totalPage2"
                                                :type="'compact'"
                                                @page-change="getInfomation">
                                            </bk-paging>
                                        </div>
                                    </td>
                                </tr>
                            </template>
                            <template v-else>
                                <tr v-cloak>
                                    <td colspan="7" class="pagesize">
                                        <div class="bk-result">
                                            <img src="../../images/box.png">
                                            <p>{{$t('m.tabControl.data')}}</p>
                                        </div>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
                <!-- 直连区域列表 -->
                <div class="bk-tab-info" v-show="tabName === 'directArea' && !showAreaCloud">
                    <!-- 添加直连区域Agent信息 -->
                    <agent-node
                        v-show="addAreaAgent && !cmdbSettings.isShow"
                        :app-id="appId"
                        :cmdb-list="cmdb.list"
                        :excel-list="saveUpdata.infoList"
                        :tab-name="tabName"
                        :length="cloudList.length"
                        @hideEditor="toggleAgentEditor"
                        @success="agentActionSuccess"></agent-node>
                    <!-- 直连区域列表-->
                    <div class="bk-stall-area">
                        <table class="bk-table has-table-hover">
                            <thead>
                                <tr>
                                    <th style="width: 16%" class="pl30">
                                        <label class="bk-form-checkbox bk-checkbox-small bk-sple-class">
                                            <input type="checkbox" name="checkbox1" :checked="cloudStatus" @click="cloudInput" :disabled="!cloudList.length">
                                        </label>
                                        {{$t('m.addNode.address')}}
                                    </th>
                                    <th style="width: 10%">{{$t('m.addNode.nodeType')}}</th>
                                    <th style="width: 10%" class="bk-center">
                                        <span class="bk-cursor" @click="sortList('agent_status')">
                                            {{$t('m.headTab.status')}} <i class="bk-icon icon-sort"></i>
                                        </span>
                                    </th>
                                    <th style="width: 14%">
                                        <span class="bk-cursor" @click="sortList('update_time')">
                                            {{$t('m.headTab.updateTime')}} <i class="bk-icon icon-sort"></i>
                                        </span>
                                    </th>
                                    <th style="width: 20%">{{$t('m.headTab.step')}}</th>
                                    <th style="width: 30%" class="bk-center">{{$t('m.addNode.operation')}}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template v-if="cloudList.length">
                                    <tr v-for="(item, index) in cloudList">
                                        <td class="pl30" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                            <label class="bk-form-checkbox bk-checkbox-small bk-sple-class">
                                                <input
                                                    type="checkbox"
                                                    name="checkbox1"
                                                    :checked="item.checkedBox"
                                                    :disabled="!(item.doObj.stop)"
                                                    @click="cloudInputValue(index, item)">
                                            </label>
                                            {{item.conn_ip}}
                                        </td>
                                        <td class="bk-blue" :class="{'bk-span-imcc': !(item.doObj.stop)}">{{item.nodeName}}</td>
                                        <td class="bk-center" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                            <span v-if="item.status"
                                                  class="bk-span-blue"
                                                  :class="{'bk-span-gray': item.status[0].status === 'UNKNOWN' || item.status[0].status === 'FAILED'}">{{item.status[0].version || '--'}}</span>
                                        </td>
                                        <td :class="{'bk-span-imcc': !(item.doObj.stop)}">{{item.update_time}}</td>
                                        <td @click="openStallStep(item)" class="bk-cursor">
                                            <img class="bk-rotation bk-img-icon" src="../../images/running.png" v-show="item.job_result.status === 'QUEUE' || item.job_result.status === 'RUNNING'">
                                            <span class="status-text" :class="{'bk-span-red':item.job_result.status === 'FAILED', 'bk-span-green':item.job_result.status === 'SUCCESS'}">{{item.job_result.step}}</span>
                                            <img src="../../images/word.png" class="ml10 bk-img-icon">
                                        </td>
                                        <td class="bk-center">
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.sava}]"
                                                @click="openCompileInfo('SAVE', item)">
                                            {{$t('m.operateStep.compile')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.reinstall}]"
                                                @click="openTerm(item, 'REINSTALL')">
                                            {{$t('m.operateStep.reinstall')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.uninstall}]"
                                                @click="openTerm(item, 'UNINSTALL')">
                                            {{$t('m.operateStep.uninstall')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.remove}]"
                                                @click="openTerm(item, 'REMOVE')">
                                            {{$t('m.operateStep.remove')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.stop}]"
                                                @click="openTerm(item, 'STOP')">
                                            {{$t('m.operateStep.stop')}}</a>
                                        </td>
                                    </tr>
                                    <tr class="pagesize">
                                        <td class="bk-position" colspan="6">
                                            <div class="bk-table-page-top">
                                                <bk-paging
                                                    <bk-paging
                                                    :cur-page.sync="customPaging.page2"
                                                    :total-page="customPaging.totalPage2"
                                                    :type="'compact'"
                                                    @page-change="getInfomation">
                                                </bk-paging>
                                            </div>
                                        </td>
                                    </tr>
                                </template>
                                <template v-else>
                                    <tr v-cloak>
                                        <td colspan="6" class="pagesize">
                                            <div class="bk-result">
                                                <!-- <img src="../../images/box.png"> -->
                                                <div class="bk-page-info" style="text-align: center;">
                                                    <p class="bk-p-black" @click="addArea" style="cursor: pointer;">
                                                        {{$t('m.addInfo.agent.add')}}
                                                    </p>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                        <div class="bk-stall-shade" v-show="addShade"></div>
                    </div>
                </div>
                <!-- 云区域列表 -->
                <div class="bk-tab-info" v-show="tabName === item.name" v-for="(item, index) in cloudNameList">
                    <!-- 添加云区域Agent信息 -->
                    <agent-node
                        v-show="addAreaAgent"
                        :app-id="appId"
                        :cmdb-list="cmdb.list"
                        :excel-list="saveUpdata.infoList"
                        :tab-name="tabName"
                        :length="cloudList.length"
                        :cloud-id="item.bk_cloud_id"
                        @hideEditor="toggleAgentEditor"
                        @success="agentActionSuccess"></agent-node>
                    <!-- 添加proxy节点 -->
                    <p-agent-node
                        v-show="aProxy"
                        :app-id="appId"
                        :tab-name="tabName"
                        :length="cloudList.length"
                        :add-num="curCloudProxyStatus.total"
                        @hideEditor="toggleProxyEditor"
                        @success="pAgentActionSuccess"
                        :cloud-id="item.bk_cloud_id"></p-agent-node>
                    <!--云区域列表-->
                    <div class="bk-stall-area">
                        <table class="bk-table has-table-hover">
                            <thead>
                                <tr>
                                    <th style="width: 16%" class="pl30">
                                        <label class="bk-form-checkbox bk-checkbox-small bk-sple-class">
                                            <input
                                                type="checkbox"
                                                name="checkbox1"
                                                :checked="cloudStatus"
                                                @click="cloudInput"
                                                :disabled="!cloudList.length">
                                        </label>
                                        {{$t('m.addNode.address')}}
                                    </th>
                                    <th style="width: 10%">{{$t('m.addNode.nodeType')}}</th>
                                    <th style="width: 10%" class="bk-center">
                                        <span class="bk-cursor" @click="sortList('agent_status')">
                                            {{$t('m.headTab.status')}} <i class="bk-icon icon-sort"></i>
                                        </span>
                                    </th>
                                    <th style="width: 14%">
                                        <span class="bk-cursor" @click="sortList('update_time')">
                                            {{$t('m.headTab.updateTime')}} <i class="bk-icon icon-sort"></i>
                                        </span>
                                    </th>
                                    <th style="width: 20%">{{$t('m.headTab.step')}}</th>
                                    <th style="width: 30%" class="bk-center">{{$t('m.addNode.operation')}}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template v-if="proxyList.length">
                                    <tr v-for="(item, index) in proxyList">
                                        <td class="pl30" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                            <label class="bk-form-checkbox bk-checkbox-small bk-sple-class">
                                                <input
                                                    type="checkbox"
                                                    name="checkbox1"
                                                    :checked="item.checkedBox"
                                                    @click="cloudInputValue(index, item)"
                                                    :disabled="(item.node_type === cloudProxy.status && cloudProxy.agent) || !(item.doObj.stop)">
                                            </label>
                                            {{item.conn_ip}} / {{item.cascade_ip}}
                                        </td>
                                        <td :class="{'bk-orgen':item.node_type === 'PROXY','bk-blue': item.node_type === 'AGENT','bk-blue': item.node_type === 'PAGENT','bk-span-imcc': !(item.doObj.stop)}">{{item.nodeName}}</td>
                                        <td class="bk-center" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                            <span v-if="item.status"
                                                  class="bk-span-blue"
                                                  :class="{'bk-span-gray': item.status[0].status === 'UNKNOWN' || item.status[0].status === 'FAILED'}">{{item.status[0].version || '--'}}</span>
                                        </td>
                                        <td :class="{'bk-span-imcc': !(item.doObj.stop)}">{{item.update_time}}</td>
                                        <td @click="openStallStep(item)" class="bk-cursor">
                                            <img class="bk-rotation bk-img-icon" src="../../images/running.png" v-show="item.job_result.status === 'QUEUE' || item.job_result.status === 'RUNNING'">
                                            <span class="status-text" :class="{'bk-span-red':item.job_result.status === 'FAILED', 'bk-span-green':item.job_result.status === 'SUCCESS'}">{{item.job_result.step}}</span>
                                            <img src="../../images/word.png" class="ml10 bk-img-icon">
                                        </td>
                                        <td class="bk-center">
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.sava}]"
                                                @click="openCompileInfo('SAVE', item)">
                                            {{$t('m.operateStep.compile')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.reinstall}]"
                                                @click="openTerm(item, 'REINSTALL')">
                                            {{$t('m.operateStep.reinstall')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.uninstall}]"
                                                @click="openTerm(item, 'UNINSTALL')">
                                            {{$t('m.operateStep.uninstall')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.remove}]"
                                                @click="openTerm(item, 'REMOVE')">
                                            {{$t('m.operateStep.remove')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.stop}]"
                                                @click="openTerm(item, 'STOP')">
                                            {{$t('m.operateStep.stop')}}</a>
                                        </td>
                                    </tr>
                                    <tr v-show="agentList.length">
                                        <td colspan="6" class="bk-tr-line"></td>
                                    </tr>
                                    <tr v-for="(item, index) in agentList">
                                        <td class="pl30" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                            <label class="bk-form-checkbox bk-checkbox-small bk-sple-class">
                                                <input
                                                    type="checkbox"
                                                    name="checkbox1"
                                                    :checked="item.checkedBox"
                                                    @click="cloudInputValue(index, item)"
                                                    :disabled="(item.node_type === cloudProxy.status && cloudProxy.agent) || !(item.doObj.stop)">
                                            </label>
                                            {{item.conn_ip}}
                                        </td>
                                        <td :class="{'bk-orgen':item.node_type === 'PROXY','bk-blue': item.node_type === 'AGENT','bk-blue': item.node_type === 'PAGENT','bk-span-imcc': !(item.doObj.stop)}">{{item.nodeName}}</td>
                                        <td class="bk-center" :class="{'bk-span-imcc': !(item.doObj.stop)}">
                                            <span v-if="item.status"
                                                  class="bk-span-blue"
                                                  :class="{'bk-span-gray': item.status[0].status === 'UNKNOWN' || item.status[0].status === 'FAILED'}">{{item.status[0].version || '--'}}</span>
                                        </td>
                                        <td :class="{'bk-span-imcc': !(item.doObj.stop)}">{{item.update_time}}</td>
                                        <td @click="openStallStep(item)" class="bk-cursor">
                                            <img class="bk-rotation bk-img-icon" src="../../images/running.png" v-show="item.job_result.status === 'QUEUE' || item.job_result.status === 'RUNNING'">
                                            <span class="status-text" :class="{'bk-span-red':item.job_result.status === 'FAILED', 'bk-span-green':item.job_result.status === 'SUCCESS'}">{{item.job_result.step}}</span>
                                            <img src="../../images/word.png" class="ml10 bk-img-icon">
                                        </td>
                                        <td class="bk-center">
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.sava}]"
                                                @click="openCompileInfo('SAVE', item)">
                                            {{$t('m.operateStep.compile')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.reinstall}]"
                                                @click="openTerm(item, 'REINSTALL')">
                                            {{$t('m.operateStep.reinstall')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.uninstall}]"
                                                @click="openTerm(item, 'UNINSTALL')">
                                            {{$t('m.operateStep.uninstall')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.remove}]"
                                                @click="openTerm(item, 'REMOVE')">
                                            {{$t('m.operateStep.remove')}}</a>
                                            <a href="javascript:void(0);"
                                                :class="['bk-text-button', {'is-disabled': item.doObj.stop}]"
                                                @click="openTerm(item, 'STOP')">
                                            {{$t('m.operateStep.stop')}}</a>
                                        </td>
                                    </tr>
                                    <tr class="pagesize">
                                        <td class="bk-position" colspan="6">
                                            <div class="bk-table-page-top">
                                                <bk-paging
                                                    <bk-paging
                                                    :cur-page.sync="customPaging.page2"
                                                    :total-page="customPaging.totalPage2"
                                                    :type="'compact'"
                                                    @page-change="getInfomation">
                                                </bk-paging>
                                            </div>
                                        </td>
                                    </tr>
                                </template>
                                <template v-else>
                                    <tr v-cloak>
                                        <td colspan="6" class="pagesize">
                                            <div class="bk-result">
                                                <!-- <img src="../../images/box.png"> -->
                                                <div class="bk-page-info">
                                                    <div class="bk-p-black">
                                                        1. {{$t('m.addInfo.proxy.add')}}
                                                        <p class="bk-p-gray" @click="addProxy" style="cursor: pointer;">
                                                            {{$t('m.addInfo.proxy.info')}}
                                                        </p>
                                                    </div>
                                                    <div class="bk-p-black">
                                                        2. {{$t('m.addInfo.proxy.status')}}
                                                        <p class="bk-p-gray">
                                                            {{$t('m.addInfo.proxy.statusInfo')}}
                                                        </p>
                                                    </div>
                                                    <p class="bk-p-black">
                                                        {{$t('m.addInfo.proxy.cloud')}}
                                                    </p>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                        <div class="bk-stall-shade" v-show="addShade"></div>
                    </div>
                </div>
            </div>
            <!-- 弹框板块 -->
            <div class="bk-open-win">
                <bk-sideslider :is-show.sync="customSettings.isShow" :title="customSettings.title" :width="700" :quick-close="true">
                    <div class="p20 bk-open-window" slot="content">
                        <!-- 详细安装步骤 -->
                        <div class="bk-install-step" v-show="customSettings.title === $t('m.openSlider.stepInfo')" id="bkStep">
                            <div class="bk-step-info" v-html="stepInfo"></div>
                        </div>
                        <!-- 编辑 -->
                        <div class="bk-compile-info" v-show="customSettings.title === $t('m.operateStep.compile')">
                            <div class="bk-compile-nav">
                                <ul>
                                    <li v-for="(item, index) in complieList"
                                        :class="{'bk-border-bottom': complieIndex.index === index}"
                                        @click="changeComplie(item, index)"
                                        v-show="item.status">{{item.name}}</li>
                                </ul>
                            </div>
                            <div class="bk-compile-state">
                                <p>
                                    <span>1.  </span>
                                    <span>
                                        {{$t('m.openSlider.attention.stepOne')}}
                                    </span>
                                </p>
                                <p>
                                    <span>2.  </span>
                                    <span>
                                        {{$t('m.openSlider.attention.stepTwo')}}
                                    </span>
                                </p>
                                <p style="padding-top: 0px;">
                                    <span>3.  </span>
                                    <span>
                                        {{$t('m.openSlider.attention.stepThree')}}
                                    </span>
                                </p>
                            </div>
                            <!-- windows编辑框 -->
                            <div class="bk-compile-input" v-show="complieIndex.windows">
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.address')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            class="bk-form-input"
                                            v-model="compileInfo.connIp"
                                            :placeholder="$t('m.openSlider.compileOpear.please')"
                                            disabled="disabled"
                                            @input="compileAgent('connIp')">
                                    </div>
                                </div>
                                <!-- <div class="bk-form-item">
                                    <label class="bk-label"><span>cygwin</span></label>
                                    <div class="bk-form-content">
                                        <label class="bk-form-checkbox bk-checkbox-small">
                                            <input type="checkbox" name="checkbox1" :checked="compileInfo.hasCygwin">
                                        </label>
                                    </div>
                                </div> -->
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>SSH{{$t('m.addNode.port')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.ssh"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            :class="{'bk-input-checked': compileInfo.verify.port}"
                                            @input="compileAgent('ssh')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.account')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.account"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterAct')"
                                            :class="{'bk-input-checked': compileInfo.verify.acc}"
                                            @input="compileAgent('account')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.verify')}}</span></label>
                                    <div class="bk-form-content">
                                        <div class="bk-form-change">
                                            <bk-selector
                                                class="bk-form-stall"
                                                :selected.sync="compileInfo.way"
                                                :list="compileInfo.agentWay">
                                            </bk-selector>
                                        </div>
                                        <div class="bk-form-show">
                                            <input
                                                type="password"
                                                class="bk-form-input bk-input-bom bk-input-normal bk-pass-width"
                                                v-model="compileInfo.password"
                                                v-show="compileInfo.way === 'PASSWORD'"
                                                :placeholder="$t('m.addNode.passInput')"
                                                :class="{'bk-input-checked': compileInfo.verify.pass}"
                                                @input="compileAgent('way')">
                                            <button class="bk-button bk-default bk-input-bom" v-show="compileInfo.way === 'KEY'"><i class="bk-icon icon-plus"></i>{{$t('m.addNode.upload')}}</button>
                                            <input type="file" class="bk-input-miyao" v-show="compileInfo.way === 'KEY'"
                                            :value='a'
                                            @change="readFile($event)">
                                            <span class="bk-file-info">{{compileInfo.nameFile}}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <button
                                        class="bk-button bk-primary"
                                        @click="compileAgentInfo('SAVE', 'indentify', '')">
                                        {{$t('m.clickBtn.save')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.reinstall"
                                        @click="compileAgentInfo('REINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.reinstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.uninstall"
                                        @click="compileAgentInfo('UNINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.uninstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.remove"
                                        @click="compileAgentInfo('REMOVE', 'indentify', '')">{{$t('m.openSlider.compileOpear.remove')}}</button>
                                </div>
                            </div>
                            <!-- windowscygwin编辑框 -->
                            <div class="bk-compile-input" v-show="complieIndex.windowsCyg">
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.address')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            class="bk-form-input"
                                            v-model="compileInfo.connIp"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            disabled="disabled"
                                            @input="compileAgent('connIp')">
                                    </div>
                                </div>
                                <!-- <div class="bk-form-item">
                                    <label class="bk-label"><span>cygwin</span></label>
                                    <div class="bk-form-content">
                                        <label class="bk-form-checkbox bk-checkbox-small">
                                            <input type="checkbox" name="checkbox1" :checked="compileInfo.hasCygwin">
                                        </label>
                                    </div>
                                </div> -->
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>SSH{{$t('m.addNode.port')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.ssh"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            :class="{'bk-input-checked': compileInfo.verify.port}"
                                            @input="compileAgent('ssh')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.account')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.account"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterAct')"
                                            :class="{'bk-input-checked': compileInfo.verify.acc}"
                                            @input="compileAgent('account')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.verify')}}</span></label>
                                    <div class="bk-form-content">
                                        <div class="bk-form-change">
                                            <bk-selector
                                                class="bk-form-stall"
                                                :selected.sync="compileInfo.way"
                                                :list="compileInfo.agentWay">
                                            </bk-selector>
                                        </div>
                                        <div class="bk-form-show">
                                            <input
                                                type="password"
                                                class="bk-form-input bk-input-bom bk-input-normal bk-pass-width"
                                                v-model="compileInfo.password"
                                                v-show="compileInfo.way === 'PASSWORD'"
                                                :placeholder="$t('m.addNode.passInput')"
                                                :class="{'bk-input-checked': compileInfo.verify.pass}"
                                                @input="compileAgent('way')">
                                            <button class="bk-button bk-default bk-input-bom" v-show="compileInfo.way === 'KEY'"><i class="bk-icon icon-plus"></i> {{$t('m.addNode.upload')}}</button>
                                            <input type="file" class="bk-input-miyao" v-show="compileInfo.way === 'KEY'"
                                            :value='a'
                                            @change="readFile($event)">
                                            <span class="bk-file-info">{{compileInfo.nameFile}}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <button
                                        class="bk-button bk-primary"
                                        @click="compileAgentInfo('SAVE', 'indentify', '')">
                                        {{$t('m.clickBtn.save')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.reinstall"
                                        @click="compileAgentInfo('REINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.reinstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.uninstall"
                                        @click="compileAgentInfo('UNINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.uninstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.remove"
                                        @click="compileAgentInfo('REMOVE', 'indentify', '')">{{$t('m.openSlider.compileOpear.remove')}}</button>
                                </div>
                            </div>
                            <!-- linux编辑框 -->
                            <div class="bk-compile-input" v-show="complieIndex.linux">
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.address')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            class="bk-form-input"
                                            v-model="compileInfo.connIp"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            disabled="disabled"
                                            @input="compileAgent('connIp')">
                                    </div>
                                </div>
                                <div class="bk-form-item" v-show="!!(compileInfo.cascade_ip) && tabName !== 'directArea'">
                                    <label class="bk-label"><span>{{$t('m.addNode.outerip')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            class="bk-form-input"
                                            v-model="compileInfo.cascade_ip"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            disabled="disabled"
                                            @input="compileAgent('loginIp')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>SSH{{$t('m.addNode.port')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.ssh"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            :class="{'bk-input-checked': compileInfo.verify.port}"
                                            @input="compileAgent('ssh')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.account')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.account"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterAct')"
                                            :class="{'bk-input-checked': compileInfo.verify.acc}"
                                            @input="compileAgent('account')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.verify')}}</span></label>
                                    <div class="bk-form-content">
                                        <div class="bk-form-change">
                                            <bk-selector
                                                class="bk-form-stall"
                                                :selected.sync="compileInfo.way"
                                                :list="compileInfo.agentWay">
                                            </bk-selector>
                                        </div>
                                        <div class="bk-form-show">
                                            <input
                                                type="password"
                                                class="bk-form-input bk-input-bom bk-input-normal"
                                                v-model="compileInfo.password"
                                                v-show="compileInfo.way === 'PASSWORD'"
                                                :placeholder="$t('m.addNode.passInput')"
                                                :class="{'bk-input-checked': compileInfo.verify.pass}"
                                                @input="compileAgent('way')">
                                            <button class="bk-button bk-default bk-input-bom" v-show="compileInfo.way === 'KEY'"><i class="bk-icon icon-plus"></i> {{$t('m.addNode.upload')}}</button>
                                            <input type="file" class="bk-input-miyao" v-show="compileInfo.way === 'KEY'"
                                            :value='a'
                                            @change="readFile($event)">
                                            <span class="bk-file-info">{{compileInfo.nameFile}}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <button
                                        class="bk-button bk-primary"
                                        @click="compileAgentInfo('SAVE', 'indentify', '')">
                                        {{$t('m.clickBtn.save')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.reinstall"
                                        @click="compileAgentInfo('REINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.reinstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.uninstall"
                                        @click="compileAgentInfo('UNINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.uninstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.remove"
                                        @click="compileAgentInfo('REMOVE', 'indentify', '')">{{$t('m.openSlider.compileOpear.remove')}}</button>
                                </div>
                            </div>
                            <!-- AIX编辑框 -->
                            <div class="bk-compile-input" v-show="complieIndex.aix">
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.address')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            class="bk-form-input"
                                            v-model="compileInfo.connIp"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            disabled="disabled"
                                            @input="compileAgent('connIp')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>SSH{{$t('m.addNode.port')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.ssh"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterPort')"
                                            :class="{'bk-input-checked': compileInfo.verify.port}"
                                            @input="compileAgent('ssh')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.account')}}</span></label>
                                    <div class="bk-form-content">
                                        <input
                                            type="text"
                                            v-model="compileInfo.account"
                                            class="bk-form-input"
                                            :placeholder="$t('m.openSlider.compileOpear.enterAct')"
                                            :class="{'bk-input-checked': compileInfo.verify.acc}"
                                            @input="compileAgent('account')">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label"><span>{{$t('m.addNode.verify')}}</span></label>
                                    <div class="bk-form-content">
                                        <div class="bk-form-change">
                                            <bk-selector
                                                class="bk-form-stall"
                                                :selected.sync="compileInfo.way"
                                                :list="compileInfo.agentWay">
                                            </bk-selector>
                                        </div>
                                        <div class="bk-form-show">
                                            <input
                                                type="password"
                                                class="bk-form-input bk-input-bom bk-input-normal"
                                                v-model="compileInfo.password"
                                                v-show="compileInfo.way === 'PASSWORD'"
                                                :placeholder="$t('m.addNode.passInput')"
                                                :class="{'bk-input-checked': compileInfo.verify.pass}"
                                                @input="compileAgent('way')">
                                            <button class="bk-button bk-default bk-input-bom" v-show="compileInfo.way === 'KEY'"><i class="bk-icon icon-plus"></i> {{$t('m.addNode.upload')}}</button>
                                            <input type="file" class="bk-input-miyao" v-show="compileInfo.way === 'KEY'"
                                            :value='a'
                                            @change="readFile($event)">
                                            <span class="bk-file-info">{{compileInfo.nameFile}}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <button
                                        class="bk-button bk-primary"
                                        @click="compileAgentInfo('SAVE', 'indentify', '')">
                                        {{$t('m.clickBtn.save')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.reinstall"
                                        @click="compileAgentInfo('REINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.reinstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.uninstall"
                                        @click="compileAgentInfo('UNINSTALL', 'indentify', '')">{{$t('m.openSlider.compileOpear.uninstall')}}</button>
                                    <button
                                        class="bk-button bk-default"
                                        :disabled="compileInfo.doObj.remove"
                                        @click="compileAgentInfo('REMOVE', 'indentify', '')">{{$t('m.openSlider.compileOpear.remove')}}</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </bk-sideslider>
                <!-- 导入CMDB -->
                <!-- <bk-sideslider :is-show.sync="cmdbSettings.isShow" :title="cmdbSettings.title" :width="553" :quick-close="true">
                    <div class="p20 bk-open-window" slot="content">
                        <div class="bk-add-cmdb">
                            <ul class="bk-first-ul">
                                <li v-for="(item, index) in addCmdb">
                                    <p>
                                        <i class="bk-icon icon-right-shape" v-show="!item.iconStatus" @click="changTypeStatus(index,item)"></i>
                                        <i class="bk-icon icon-down-shape" v-show="item.iconStatus" @click="changTypeStatus(index,item)"></i>
                                        <label class="bk-form-checkbox bk-checkbox-small">
                                            <input
                                                type="checkbox"
                                                name="checkbox1"
                                                :checked="item.typeStatus"
                                                :disabled="cmdb.continue"
                                                @click="changeCmdb(index,item)">
                                        </label>
                                        <span class="bk-ul-word" @click="changTypeStatus(index,item)">{{item.SetName}}</span>
                                    </p>
                                    <ul v-if="item.Children" class="bk-second-ul">
                                        <li v-for="(info, innum) in item.Children" v-show="item.iconStatus">
                                            <label class="bk-form-checkbox bk-checkbox-small">
                                                <input
                                                    type="checkbox"
                                                    name="checkbox1"
                                                    :disabled="cmdb.continue"
                                                    :checked="info.childrenStatus"
                                                    @click="changeSmallStatus(index,innum,info)">
                                            </label>
                                            <span class="bk-ul-word">{{info.ModuleName}}[{{info.HOSTS.length}}]</span>
                                        </li>
                                    </ul>
                                </li>
                            </ul>
                            <div class="bk-cmdb-note" v-show="cmdb.note">
                                <h4>Note：</h4>
                                <div class="bk-note-p">
                                    <p v-for="item in cmdb.nodeInfo">{{item}}</p>
                                    <p>{{$t('m.openSlider.cmdb.installNum')}}： {{showOne.length}}</p>
                                </div>
                                <div class="bk-note-other">
                                    <p v-show="!(showOne.status)">{{$t('m.openSlider.cmdb.continue')}}</p>
                                    <p>{{$t('m.openSlider.cmdb.return')}}</p>
                                </div>
                            </div>
                            <div class="bk-cmdb-btn">
                                <div v-show="cmdb.add">
                                    <button class="bk-button bk-primary" @click="lookNodeInfo">{{$t('m.clickBtn.import')}}</button>
                                    <button class="bk-button bk-default" @click="cmdbSettings.isShow=false">{{$t('m.clickBtn.return')}}</button>
                                </div>
                                <div v-show="cmdb.continue">
                                    <button class="bk-button bk-primary" @click="continueNodeInfo" :class="{'is-disabled': showOne.status}">{{$t('m.clickBtn.continue')}}</button>
                                    <button class="bk-button bk-default" @click="goBackCmdb">{{$t('m.clickBtn.return')}}</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </bk-sideslider>
 -->            </div>
            <!-- 删除二次弹窗 -->
            <div class="bk-open-shade" v-show="termDelete.shade"></div>
            <div class="bk-open-deletedoc" v-show="termDelete.deleteOpenTerm">
                <div class="bk-doc-top">
                    <p :class="{'bk-p': !stopInfo.showthis}">{{$t('m.message.comfireOpera')}}</p>
                </div>
                <div v-show="stopInfo.showthis" class="bk-dcos-ther">
                    <p>{{$t('m.otherAdd.someStop')}}(id: {{compileInfo.id}})</p>
                </div>
                <div class="bk-doc-btn">
                    <button class="bk-button bk-primary bk-width" @click="termTask" v-show="termDelete.val === 'STOP'">{{$t('m.clickBtn.confirm')}}</button>
                    <button class="bk-button bk-primary bk-width" @click="compileAgentInfo" v-show="termDelete.val !== 'STOP'">{{$t('m.clickBtn.confirm')}}</button>
                    <button class="bk-button bk-default bk-width ml10" @click="closeAll">{{$t('m.clickBtn.cancel')}}</button>
                </div>
            </div>
            <div class="bk-open-deletedoc" v-show="stopInfo.shopShow">
                <div class="bk-doc-top">
                    <p>{{$t('m.otherAdd.allStop')}}</p>
                </div>
                <div class="bk-doc-btn">
                    <button class="bk-button bk-primary bk-width" @click="stopAllAgent">{{$t('m.clickBtn.confirm')}}</button>
                    <button class="bk-button bk-default bk-width ml10" @click="openAgentAll">{{$t('m.clickBtn.cancel')}}</button>
                </div>
            </div>
        </div>
		<!-- <app-exception></app-exception> -->
        <!-- excel导入文件 -->
        <div class="bk-open-win">
            <bk-sideslider
                :is-show.sync="excelOpen.show"
                :title="$t('m.addNewInfo.excelInfo')"
                :width="700"
                :quick-close="true"
                @shown="closeSilder">
                <div class="p20 bk-open-window" slot="content">
                    <div class="bk-excel-top">
                        <span class="bk-excel-icon">！</span>
                        <span class="bk-excel-blue">{{$t('m.addNewInfo.excelInfo')}}: </span>
                        <span>{{$t('m.addNewInfo.info')}}:</span>
                        <span style="margin-left: 10px; color: #3c96ff; cursor: pointer;" @click="downLoadExcel">
                            <i class="bk-icon icon-download"></i>{{$t('m.addNewInfo.downloadTemplate')}}
                        </span>
                    </div>
                    <div class="bk-tab-info" style="border: 1px solid #c3cdd7; margin: 0 30px 36px; border-bottom: none;">
                        <table class="bk-table has-table-hover">
                            <thead>
                                <tr>
                                    <th>{{$t('m.addNewInfo.address')}}</th>
                                    <th>{{$t('m.addNewInfo.operat')}}</th>
                                    <th>{{$t('m.addNewInfo.port')}}</th>
                                    <th>{{$t('m.addNewInfo.account')}}</th>
                                    <th>{{$t('m.addNewInfo.password')}}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>111.111.111.111</td>
                                    <td>LINUX</td>
                                    <td>8080</td>
                                    <td>root</td>
                                    <td>123456</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="bk-excel-input">
                        <span>+ {{$t('m.addNewInfo.upload')}}</span>
                        <input v-if="!addAreaAgent"
                            id="upload"
                            type="file"
                            class="bk-file-input"
                            @change="addExcelArea"
                            accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                            :value="excelOpen.excelVal">
                        <span style="position: absolute; bottom: -35px; left: 0px;" v-if="!!excelOpen.excelName">
                            <span class="bk-excel-radiu">
                                <i class="bk-icon icon-check-1"></i>
                            </span>
                            <span style="color: #737987; font-size: 12px;">{{excelOpen.excelName}}</span>
                        </span>
                    </div>
                    <div class="bk-excel-btn" style="margin-top: 65px; text-align: center;">
                        <bk-button type="primary" :title="$t('m.addNewInfo.reload')" @click="excelSubmit" :disabled="!excelOpen.excelName">
                            {{$t('m.addNewInfo.reload')}}
                        </bk-button>
                    </div>
                </div>
            </bk-sideslider>
        </div>
        <!-- 高级设置 -->
        <div class="bk-advanced-info" v-if="showSet">
            <advanced-set 
                v-if="nodeType" 
                :cloudId="allIdNum"
                :appId="appId"
                :nodeType="nodeType"
                @hideEditor="toggleAgentEditor"
                @success="agentActionSuccess"></advanced-set>
        </div>
        <div class="bk-cmdb-content" v-if="cmdbSettings.isShow">
            <cmdb></cmdb>
        </div>
	</div>
</template>

<script>
    import agentNode from './agent.vue'
    import pAgentNode from './p-agent.vue'
    import tabAgent from './tab-agent.vue'
    import tabpanelAgent from './tabpanel-agent.vue'
    import advancedSet from '../common/advancedSet.vue'
    import cmdb from './component/importCmdb.vue'
    import cloudAreaManage from './component/cloudAreaManage.vue'

    export default {
        data () {
            return {
                // 高级设置
                showSet: false,
                nodeType: '',
                // 显示隐藏直连区域
                showAreaCloud: '',
                cloudShow: true,
                a: '',
                // 列表数据loading显示
                isDataLoading: true,
                isCloudLoading: true,
                // 确认终止二次弹框
                termDelete: {
                    deleteOpenTerm: false,
                    shade: false,
                    val: ''
                },
                // 验证信息
                verify: {
                    cloud: false
                },
                // 添加Agent
                addAreaAgent: false,
                // 添加云区域Proxy
                aProxy: false,
                // 选项卡切换的name
                tabName: 'directArea',
                // 所有区域选框状态
                allArr: [],
                allStatus: false,
                // 记录云区域id值
                allIdNum: '0',
                // 控制复制节点的状态
                cloneNode: true,
                // 直连区域选框状态
                areaCheckList: [],
                // 批量操作判断状态
                areaDoInfo: {
                    updata: false,
                    sava: false,
                    reinstall: false,
                    uninstall: false,
                    remove: false,
                    stop: false
                },
                // 头部云区域列表
                cloudNameList: [],
                lastIndex: 'addCloud',
                addClickCloud: false,
                // 云区域选框状态
                cloudStatus: false,
                cloudProxy: {
                    agent: false,
                    status: ''
                },
                // 云区域列表数据
                cloudList: [],
                proxyList: [],
                agentList: [],
                // 添加云名称
                addCloudName: '',
                // 直连区域分页配置
                customPaging: {
                    page1: 1,
                    totalPage1: 2,
                    page2: 1,
                    totalPage2: 2,
                    page_size: 10
                },
                // 详细安装步骤配置
                customSettings: {
                    isShow: false,
                    title: this.$t('m.operateStep.compile')
                },
                cmdbSettings: {
                    isShow: false,
                    title: this.$t('m.tabControl.importCmdb')
                },
                compStatus: false,
                // 编辑选项
                complieList: [
                    {
                        title: 'WINDOWS',
                        status: false,
                        name: 'Windows'
                    },
                    {
                        title: 'WINDOWSCYGWIN',
                        status: false,
                        name: 'Windows(Cygwin)'
                    },
                    {
                        title: 'LINUX',
                        status: false,
                        name: 'Linux'
                    },
                    {
                        title: 'AIX',
                        status: false,
                        name: 'AIX'
                    }
                ],
                complieIndex: {
                    windows: true,
                    windowsCyg: true,
                    linux: true,
                    aix: true,
                    index: 0
                },
                statusItem: false,
                // 编辑信息
                compileInfo: {
                    tastId: '',
                    connIp: '',
                    loginIp: '',
                    inps: '',
                    hasCygwin: false,
                    ssh: '',
                    account: '',
                    way: 'PASSWORD',
                    password: '',
                    agentWay: [
                        {
                            id: 'PASSWORD',
                            name: this.$t('m.addNode.password')
                        },
                        {
                            id: 'KEY',
                            name: this.$t('m.addNode.key')
                        }
                    ],
                    verify: {
                        ip: false,
                        cascade_ip: false,
                        port: false,
                        acc: false,
                        pass: false
                    },
                    doObj: {
                        reinstall: false,
                        uninstall: false,
                        remove: false
                    },
                    bk_cloud_id: '1',
                    node_type: 'PAGENT',
                    id: null,
                    os_type: '',
                    key: '',
                    nameFile: ''
                },
                // 编辑请求状态
                compileAgentStatus: false,
                // 导入CMDB
                addCmdb: [],
                cmdb: {
                    node: false,
                    continue: false,
                    add: true,
                    list: [],
                    nodeInfo: [],
                    wipeList: []
                },
                showOne: {
                    status: false,
                    length: 0
                },
                // 安装步骤详情信息
                stepInfo: '',
                // 安装选取状态
                installStatus: {
                    updata: true,
                    reset: true,
                    unload: true,
                    break: true,
                    remove: true,
                    compile: true
                },
                // 模糊查询列表数据
                queryData: {
                    query: {
                        bk_module_id: '',
                        bk_set_id: '',
                        bk_cloud_id: '',
                        keyword: '',
                        dataInfo: {},
                        popList: []
                    },
                    // 模糊查询标记
                    queryCode: '',
                    // 模糊查询数据
                    querySetList: [],
                    queryModuleList: [],
                    searchCloud: [],
                    selectList: {
                        defaultSet: -1,
                        defaultModule: -1,
                        defaultCloud: -1
                    },
                    isDisabled: true,
                    queryDisabled: {
                        set: false,
                        module: false,
                        cloud: false,
                        searchBtn: false,
                        searchInput: false
                    },
                    keepInfo: {
                        selectList: {
                            defaultSet: -1,
                            defaultModule: -1,
                            defaultCloud: -1
                        },
                        dataInfo: {}
                    }
                },
                // 可用的proxy数量
                curCloudProxyStatus: {
                    total: 0,
                    valid_count: 0
                },
                // 日志id
                logId: '',
                addShade: false,
                proxySatus: false,
                // 排序
                sortStatus: {
                    sort: false,
                    status: '',
                    time: true,
                    theSta: true,
                    job_status: 'job_status'
                },
                errorCode: true,
                cloudNameOpera: {
                    operaName: [],
                    operaTotal: false,
                    showAdd: false,
                    total: 0
                },
                // 云区域管理
                cloudManage: {
                    saveStatus: false
                },
                statusCloud: false,
                operateStatus: {
                    tableInfo: false,
                    checkStatus: false
                },
                // 终止状态
                stopInfo: {
                    list: [],
                    status: true,
                    timeOut: '',
                    shopShow: false,
                    showthis: false
                },
                saveUpdata: {
                    infoName: ''
                },
                file: '',
                // excel文件导入
                excelOpen: {
                    show: false,
                    excelVal: '',
                    excelName: '',
                    status: false
                }
            }
        },
        components: {
            agentNode,
            pAgentNode,
            tabAgent,
            tabpanelAgent,
            advancedSet,
            cmdb,
            cloudAreaManage
        },
        methods: {
            // 高级设置
            showAdvancedOpen (type) {
                this.showSet = !this.showSet
                this.nodeType = type
            },
            closeAdvanced () {
                this.showSet = !this.showSet
            },
            // 新增终止需求
            allStop () {
                clearInterval(this.$store.state.stall.timeOut)
                this.$store.state.stall.timeOut = setInterval(() => {
                    let appId = this.appId
                    let id = this.allIdNum
                    this.$store.dispatch('stall/stopNum', {appId, id}).then(res => {
                        this.stopInfo.list = res.data.running_task_id_list
                        this.stopInfo.status = !(this.stopInfo.list.length)
                    }, res => {
                        this.stopInfo.status = false
                        clearInterval(this.$store.state.stall.timeOut)
                    })
                }, 2000)
            },
            stopAllAgent () {
                let appId = this.appId
                let params = {
                    bk_cloud_id: this.allIdNum
                }
                this.$store.dispatch('stall/stopSame', {appId, params}).then(res => {
                    this.openAgentAll()
                    this.$bkMessage({
                        message: 'SUCCESS',
                        theme: 'success'
                    })
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            openAgentAll () {
                if (this.stopInfo.status) { return }
                this.termDelete.shade = !this.termDelete.shade
                this.stopInfo.shopShow = !this.stopInfo.shopShow
            },
            checkProxyStatus () {
                if (!this.allIdNum) return
                let appId = this.appId
                let params = {
                    bk_cloud_id: this.allIdNum
                }
                // 验证proxy可用的个数
                this.$store.dispatch('stall/checkProxy', {appId, params}).then(res => {
                    if (res.result) {
                        this.curCloudProxyStatus = res.data
                    } else {
                        this.curCloudProxyStatus = {
                            total: 0,
                            valid_count: 0
                        }
                    }
                }, res => {
                    this.curCloudProxyStatus = {
                        total: 0,
                        valid_count: 0
                    }
                })
            },
            /*
            ** 添加Agent成功后的回调
            */
            agentActionSuccess () {
                this.addAreaAgent = !this.addAreaAgent
                this.addShade = !this.addShade
                this.cmdb.list = []
                this.getInfomation()
                this.addArea()
                this.toggleAgentEditor()
            },
            /*
            ** 切换列表
            */
            tabChanged (name) {
                this.tabName = name
                this.allStop()
                if (this.tabName === 'addCloud') {
                    this.getCloudInfo()
                }
                if (this.tabName === 'directArea') {
                    this.allIdNum = '0'
                } else {
                    for (let i = 0; i < this.cloudNameList.length; i++) {
                        if (name === this.cloudNameList[i].name) {
                            this.allIdNum = this.cloudNameList[i].bk_cloud_id
                            break
                        }
                    }
                }
                this.proxySatus = true
                this.proxyList = []
                this.areaCheckList = []
                this.$nextTick(() => {
                    if (this.$refs.childs) {
                        this.$refs.childs.closeOpen()
                    }
                })
                if (!this.queryData.queryCode) {
                    this.restoreData()
                    this.getInfomation()
                }
                this.restoreData()
            },
            restoreData () {
                this.clearData()
                this.addAreaAgent = false
                this.addShade = false
                this.aProxy = false
                this.customPaging = {
                    page1: 1,
                    totalPage1: 2,
                    page2: 1,
                    totalPage2: 2,
                    page_size: 10
                }
                // 清空agent，proxy显示状态
                this.curCloudProxyStatus = {
                    total: 0,
                    valid_count: 0
                }
                this.cloudStatus = false
                // 清空cmdb导入数据
                this.cmdb = {
                    node: false,
                    continue: false,
                    add: true,
                    list: [],
                    nodeInfo: [],
                    wipeList: []
                }
                // 清空选中的列表数
                this.cloudProxy = {
                    agent: false,
                    status: ''
                }
                // 清空排序数据
                this.sortStatus = {
                    sort: false,
                    status: '',
                    time: true,
                    theSta: true,
                    job_status: 'job_status'
                }
                for (let i = 0; i < this.cloudNameList.length; i++) {
                    this.cloudNameList[i].changeSta = false
                    this.cloudNameList[i].changeDel = false
                    this.cloudNameList[i].delOpen = false
                }
                this.cloudNameOpera.showAdd = false
                this.addCloudName = ''
                this.clearQueryInfo()
            },
            clearQueryInfo () {
                // 清空模糊查询的数据
                this.queryData.queryCode = ''
                this.queryData.query = {
                    bk_module_id: '',
                    bk_set_id: '',
                    bk_cloud_id: '',
                    keyword: ''
                }
                this.queryData.selectList = {
                    defaultSet: -1,
                    defaultModule: -1,
                    defaultCloud: -1
                }
                this.queryData.isDisabled = true
                this.queryData.queryDisabled = {
                    set: false,
                    module: false,
                    cloud: false,
                    searchBtn: false,
                    searchInput: false
                }
            },
            /*
            ** 获取页面数据传参
            */
            getInfomation () {
                let obj = {}
                let params = ''
                if (this.queryData.queryCode) {
                    obj = {
                        bk_module_id: this.queryData.query.bk_module_id,
                        bk_set_id: this.queryData.query.bk_set_id,
                        bk_cloud_id: this.queryData.query.bk_cloud_id,
                        keyword: this.queryData.query.keyword,
                        page_size: this.customPaging.page_size,
                        page: this.customPaging.page2
                    }
                    if (this.tabName === 'allarea') {
                        // obj.status = '0'
                    } else {
                        obj.bk_cloud_id = this.queryData.query.bk_cloud_id
                    }
                } else {
                    if (this.tabName === 'allarea') {
                        obj = {
                            status: '0',
                            page_size: this.customPaging.page_size,
                            page: this.customPaging.page2
                        }
                    } else {
                        obj = {
                            bk_cloud_id: this.allIdNum,
                            page_size: this.customPaging.page_size,
                            page: this.customPaging.page2
                        }
                    }
                }
                if (this.sortStatus.sort) {
                    obj.order_by = this.sortStatus.status
                }

                for (let key in obj) {
                    params += key + '=' + obj[key] + '&'
                }
                params = params.substring(0, params.lastIndexOf('&'))
                if (this.tabName !== 'allarea' && this.tabName !== 'directArea') {
                    this.proxyListInfo()
                    this.checkProxyStatus()
                }
                this.getInfo(params)
            },
            /*
            ** 获取列表数据信息
            */
            getInfo (params) {
                if (this.appId === null) {
                    return
                }
                this.agentList = []
                let appId = this.appId
                this.isDataLoading = true
                this.$store.dispatch('stall/getDataInfo', {appId, params}).then((res) => {
                    this.cloudList = res.data.items
                    for (let t = 0; t < this.cloudList.length; t++) {
                        if (!this.cloudList[t].status.length) {
                            this.cloudList[t].status.push({
                                host_id: this.cloudList[t].id,
                                job_result: {
                                    status: '',
                                    step: '--'
                                },
                                status: 'UNKNOWN',
                                version: ''
                            })
                        }
                    }
                    this.customPaging.totalPage2 = res.data.total_page
                    for (let i = 0; i < this.cloudList.length; i++) {
                        const curCloud = this.cloudList[i]
                        if (curCloud.node_type === 'AGENT') {
                            curCloud.nodeName = 'Agent'
                        } else if (curCloud.node_type === 'PAGENT') {
                            curCloud.nodeName = 'P-Agent'
                        } else {
                            curCloud.nodeName = 'Proxy'
                        }
                        // 区分Agent和Proxy的列表数据
                        if (curCloud.node_type === 'PROXY') {
                            this.proxyList.push(curCloud)
                        } else {
                            this.agentList.push(curCloud)
                        }
                        if (this.tabName === 'allarea') {
                            this.allArr.push(false)
                        }
                        // 给列表数据添加一个选中状态
                        curCloud.checkedBox = false
                        // 给列表数据添加禁用操作状态
                        this.juegeObj(curCloud)
                        // 分页以后，保留选中状态
                        for (let j = 0; j < this.areaCheckList.length; j++) {
                            if (this.areaCheckList[j].id === curCloud.id) {
                                curCloud.checkedBox = true
                            }
                        }
                    }
                    if (this.tabName !== 'allarea' && this.tabName !== 'directArea') {
                        for (let i = 0; i < this.proxyList.length; i++) {
                            this.cloudList.unshift(this.proxyList[i])
                        }
                    }
                    // 去除重复的proxyList中的数据
                    for (let i = 0; i < this.proxyList.length - 1; i++) {
                        for (let j = i + 1; j < this.proxyList.length; j++) {
                            if (this.proxyList[i].id === this.proxyList[j].id) {
                                this.proxyList.splice(j, 1)
                            }
                        }
                    }
                    if (this.cloudList.length !== 0) {
                        this.cloudStatus = this.getTrue(this.cloudList)
                    }
                    if (this.tabName === 'allarea') {
                        for (let i = 0; i < this.cloudList.length; i++) {
                            this.cloudList[i].cloudName = ''
                        }
                        for (let j = 0; j < this.cloudNameList.length; j++) {
                            for (let i = 0; i < this.cloudList.length; i++) {
                                if (this.cloudNameList[j].bk_cloud_id === this.cloudList[i].bk_cloud_id) {
                                    this.cloudList[i].cloudName = this.cloudNameList[j].bk_cloud_name
                                }
                            }
                        }
                    }
                    this.$store.state.stall.timeOutCheck = setTimeout(() => {
                        this.checkAgentInfo()
                    }, 10000)
                    this.isDataLoading = false
                }, res => {
                    this.isDataLoading = false
                })
            },
            /*
            ** 状态和时间的排序
            */
            sortList (value) {
                this.sortStatus.sort = true
                if (value === 'agent_status') {
                    if (this.sortStatus.theSta) {
                        this.sortStatus.theSta = false
                        this.sortStatus.status = '-' + value
                    } else {
                        this.sortStatus.theSta = true
                        this.sortStatus.status = value
                    }
                    if (this.sortStatus.time) {
                        this.sortStatus.status += ',' + 'update_time'
                    } else {
                        this.sortStatus.status += ',' + '-update_time'
                    }
                } else {
                    if (this.sortStatus.time) {
                        this.sortStatus.time = false
                        this.sortStatus.status = '-' + value
                    } else {
                        this.sortStatus.time = true
                        this.sortStatus.status = value
                    }
                    if (this.sortStatus.theSta) {
                        this.sortStatus.status += ',' + 'agent_status'
                    } else {
                        this.sortStatus.status += ',' + '-agent_status'
                    }
                }
                this.getInfomation()
            },
            /*
            ** 获取proxyList的列表信息
            */
            proxyListInfo () {
                if (this.appId === null) {
                    return
                }
                this.proxybug = true
                let params = ''
                let obj = {
                    bk_cloud_id: this.allIdNum,
                    node_type: 'PROXY'
                }
                for (let key in obj) {
                    params += key + '=' + obj[key] + '&'
                }
                params = params.substring(0, params.lastIndexOf('&'))
                this.agentList = []
                let appId = this.appId
                this.isDataLoading = true
                this.$store.dispatch('stall/getDataInfo', {appId, params}).then((res) => {
                    this.proxyList = res.data.items
                    for (let t = 0; t < this.proxyList.length; t++) {
                        if (!this.proxyList[t].status.length) {
                            this.proxyList[t].status.push({
                                host_id: this.proxyList[t].id,
                                job_result: {
                                    status: '',
                                    step: '--'
                                },
                                status: 'UNKNOWN',
                                version: ''
                            })
                        }
                    }
                    for (let i = 0; i < this.proxyList.length; i++) {
                        const curCloud = this.proxyList[i]
                        if (curCloud.node_type === 'AGENT') {
                            curCloud.nodeName = 'Agent'
                        } else if (curCloud.node_type === 'PAGENT') {
                            curCloud.nodeName = 'P-Agent'
                        } else {
                            curCloud.nodeName = 'Proxy'
                        }
                        curCloud.checkedBox = false

                        this.juegeObj(curCloud)

                        for (let j = 0; j < this.areaCheckList.length; j++) {
                            if (this.areaCheckList[j].id === curCloud.id) {
                                curCloud.checkedBox = true
                            }
                        }
                    }
                    for (let i = 0; i < this.proxyList.length - 1; i++) {
                        for (let j = i + 1; j < this.proxyList.length; j++) {
                            if (this.proxyList[i].id === this.proxyList[j].id) {
                                this.proxyList.splice(j, 1)
                            }
                        }
                    }
                }, res => {
                    this.isDataLoading = false
                })
            },
            /*
            ** 查询Agent状态（轮询操作）
            */
            checkAgentInfo () {
                if (this.appId === null) {
                    return
                }
                let arr = []
                for (let i = 0; i < this.cloudList.length; i++) {
                    // if (this.cloudList[i].job_result.status === 'QUEUE' || this.cloudList[i].job_result.status === 'RUNNING') {
                    arr.push(this.cloudList[i].id)
                    // }
                }
                if (arr.length === 0) {
                    return
                }

                let appId = this.appId
                let id = arr.join()
                this.$store.dispatch('stall/lookAgent', {appId, id}).then((res) => {
                    let valList = []
                    for (let i = 0; i < res.data.length; i++) {
                        if (res.data[i].name === 'gseagent') {
                            valList.push(res.data[i])
                        }
                    }
                    this.checkInfo(valList, this.cloudList)
                    if (this.proxyList.length) {
                        this.checkInfo(valList, this.proxyList)
                    }
                    if (this.agentList.length) {
                        this.checkInfo(valList, this.agentList)
                    }

                    this.checkProxyStatus()
                })
            },
            /*
            ** 轮询状态的赋值
            */
            checkInfo (data, arr) {
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < arr.length; j++) {
                        const curCloud = arr[j]
                        if (data[i].host_id === curCloud.id) {
                            curCloud.status[0].status = data[i].status
                            curCloud.status[0].version = data[i].version
                            curCloud.job_result.step = data[i].job_result.step
                            curCloud.job_result.status = data[i].job_result.status

                            this.juegeObj(curCloud)
                        }
                    }
                    if (data[i].is_deleted) {
                        this.proxyList = []
                        this.getInfomation()
                        break
                    }
                }
            },
            // 初始默认列表数据禁用操作状态
            juegeObj (objCloud) {
                if (this.agentList.length && this.proxyList.length) {
                    for (let i = 0; i < this.proxyList.length; i++) {
                        if (this.proxyList[i].doObj) {
                            this.proxyList[i].doObj.remove = true
                            this.proxyList[i].doObj.uninstall = true
                        }
                    }
                }
                objCloud.doObj = {
                    updata: false,
                    sava: false,
                    reinstall: false,
                    uninstall: false,
                    remove: false,
                    stop: false
                }
                if (objCloud.job_result.status === 'QUEUE' || objCloud.job_result.status === 'RUNNING') {
                    objCloud.doObj.sava = true
                    objCloud.doObj.reinstall = true
                    objCloud.doObj.uninstall = true
                    objCloud.doObj.remove = true
                    objCloud.checkedBox = false
                } else {
                    objCloud.doObj.stop = true
                }

                if (objCloud.status[0].status === 'UNKNOWN') {
                    objCloud.doObj.updata = true
                    objCloud.doObj.uninstall = true
                }
            },
            /*
            ** 选中set
            */
            querySelected (index, data) {
                // 选中set以后给queryModuleList进行赋值操作
                this.queryData.queryModuleList = []
                this.queryData.query.bk_set_id = data.bk_set_id
                let temp = 0
                if (data.name === this.$t('m.otherWord.all')) {
                    for (let i = 0; i < this.addCmdb.length; i++) {
                        temp += this.addCmdb[i].Children.length
                        for (let j = 0; j < this.addCmdb[i].Children.length; j++) {
                            let obj = {}
                            if (i === 0) {
                                obj.id = j + 1
                            } else {
                                obj.id = temp + j + 1
                            }
                            obj.name = this.addCmdb[i].Children[j].ModuleName
                            obj.bk_module_id = this.addCmdb[i].Children[j].ModuleID
                            this.queryData.queryModuleList.push(obj)
                        }

                        this.queryData.isDisabled = !this.queryData.queryModuleList
                    }
                    let allObj = {
                        id: 0,
                        name: this.$t('m.otherWord.all'),
                        bk_module_id: ''
                    }
                    this.queryData.queryModuleList.unshift(allObj)
                } else {
                    for (let i = 0; i < this.addCmdb.length; i++) {
                        if (data.id === i + 1) {
                            let allObj = {
                                id: 0,
                                name: this.$t('m.otherWord.all'),
                                bk_module_id: ''
                            }
                            this.queryData.queryModuleList.push(allObj)
                            for (let j = 0; j < this.addCmdb[i].Children.length; j++) {
                                let obj = {}
                                obj.id = j + 1
                                obj.name = this.addCmdb[i].Children[j].ModuleName
                                obj.bk_module_id = this.addCmdb[i].Children[j].ModuleID
                                this.queryData.queryModuleList.push(obj)
                            }

                            this.queryData.isDisabled = !this.queryData.queryModuleList
                            return
                        }
                    }
                }
            },
            moduleSelected (index, data) {
                this.queryData.query.bk_module_id = data.bk_module_id
            },
            cloudSelected (index, data) {
                this.queryData.query.bk_cloud_id = data.id
                this.queryData.query.dataInfo = data
                this.allIdNum = data.id
            },
            /*
            ** 获取模糊查询搜索框数据
            */
            getAddCmdbInfo () {
                this.queryData.querySetList = []
                for (let i = 0; i < this.addCmdb.length; i++) {
                    let obj = {}
                    obj.id = i + 1
                    obj.name = this.addCmdb[i].SetName
                    obj.bk_set_id = this.addCmdb[i].SetID
                    this.queryData.querySetList.push(obj)
                }
                let allObj = {
                    id: 0,
                    name: this.$t('m.otherWord.all'),
                    bk_set_id: ''
                }
                this.queryData.querySetList.unshift(allObj)
            },
            getQueryInfo () {
                if (this.queryData.queryDisabled.set || this.queryData.queryDisabled.module || this.queryData.queryDisabled.cloud || this.queryData.queryDisabled.searchBtn || this.queryData.queryDisabled.searchInput) {
                    return
                }
                if (this.queryData.selectList.defaultCloud === -1 && this.queryData.selectList.defaultModule === -1 && this.queryData.selectList.defaultSet === -1) {
                    return
                }
                if (this.queryData.selectList.defaultCloud === -1) {
                    this.$bkMessage({
                        message: this.$t('m.message.searchCloud'),
                        theme: 'error'
                    })
                    return
                }
                this.queryData.queryCode = this.$t('m.otherWord.fuzzy')
                let num = 0
                let m = 0

                let bkUl = document.getElementById('bk-tab2')
                for (let i = 0; i < this.cloudNameList.length; i++) {
                    let str = this.cloudNameList[i].bk_cloud_name
                    if (str === (this.queryData.query.dataInfo.name)) {
                        num = i
                        break
                    }
                }
                let s = 0
                for (let i = 0; i < num; i++) {
                    if (!this.cloudNameList[i].is_visible) {
                        s += 1
                    }
                }

                // bk_module_id: this.queryData.query.bk_module_id,
                // bk_set_id: this.queryData.query.bk_set_id,
                // bk_cloud_id: this.queryData.query.bk_cloud_id,
                // keyword: this.queryData.query.keyword,
                // page_size: this.customPaging.page_size,
                // page: this.customPaging.page2
                this.queryData.keepInfo.selectList = this.queryData.selectList.defaultSet
                this.queryData.keepInfo.defaultModule = this.queryData.selectList.defaultModule
                this.queryData.keepInfo.defaultCloud = this.queryData.selectList.defaultCloud
                this.queryData.keepInfo.dataInfo = this.queryData.query.dataInfo
                this.queryData.keepInfo.query = this.queryData.query

                let ulOffsetWidth = bkUl.offsetWidth
                let liWidth = 0
                let t = Math.floor(ulOffsetWidth / 120)
                for (let i = 0; i < bkUl.childNodes.length; i++) {
                    liWidth += bkUl.childNodes[i].offsetWidth
                    if (liWidth >= ulOffsetWidth) {
                        if (num - s >= t - 2) {
                            this.getInfomation()
                            this.$refs.childs.showClick(this.queryData.query.dataInfo.tagName)
                            this.$refs.childs.overToggleTab(num - i + 2)
                            this.restoreData()
                            this.queryData.selectList.defaultSet = this.queryData.keepInfo.selectList
                            this.queryData.selectList.defaultModule = this.queryData.keepInfo.defaultModule
                            this.queryData.selectList.defaultCloud = this.queryData.keepInfo.defaultCloud
                            this.queryData.query.dataInfo = this.queryData.keepInfo.dataInfo
                            this.queryData.query = this.queryData.keepInfo.query
                            return
                        } else {
                            this.getInfomation()
                            this.tabChanged(this.queryData.query.dataInfo.tagName)
                            this.restoreData()
                            this.queryData.selectList.defaultSet = this.queryData.keepInfo.selectList
                            this.queryData.selectList.defaultModule = this.queryData.keepInfo.defaultModule
                            this.queryData.selectList.defaultCloud = this.queryData.keepInfo.defaultCloud
                            this.queryData.query.dataInfo = this.queryData.keepInfo.dataInfo
                            this.queryData.query = this.queryData.keepInfo.query
                            return
                        }
                    }
                }
                if (liWidth < ulOffsetWidth) {
                    this.getInfomation()
                    this.tabChanged(this.queryData.query.dataInfo.tagName)
                    this.restoreData()
                    this.queryData.selectList.defaultSet = this.queryData.keepInfo.selectList
                    this.queryData.selectList.defaultModule = this.queryData.keepInfo.defaultModule
                    this.queryData.selectList.defaultCloud = this.queryData.keepInfo.defaultCloud
                    this.queryData.query.dataInfo = this.queryData.keepInfo.dataInfo
                    this.queryData.query = this.queryData.keepInfo.query
                }
            },
            searchInfo () {
                if (this.queryData.queryDisabled.set || this.queryData.queryDisabled.module || this.queryData.queryDisabled.cloud || this.queryData.queryDisabled.searchBtn || this.queryData.queryDisabled.searchInput || !(this.queryData.query.keyword)) {
                    return
                }
                this.queryData.query.bk_cloud_id = this.allIdNum
                this.queryData.queryCode = this.$t('m.otherWord.fuzzy')
                this.getInfomation()
                this.restoreData()
            },
            pAgentActionSuccess () {
                this.getInfomation()
                this.toggleAgentEditor()
                this.aProxy = false
                this.addAreaAgent = false
                this.addShade = false
                this.queryData.queryDisabled = {
                    set: false,
                    module: false,
                    cloud: false,
                    searchBtn: false,
                    searchInput: false
                }
            },
            /*
            ** 查询云区域数据
            */
            getCloudInfo () {
                if (this.appId === null) {
                    return
                }
                this.isCloudLoading = true
                this.queryData.searchCloud = []
                let appId = this.appId
                this.$store.dispatch('stall/getCloudInfo', {appId}).then((res) => {
                    const num = 3
                    this.cloudNameList = res.data
                    if (!this.cloudNameList.length) {
                        this.queryData.searchCloud.push({
                            id: '0',
                            name: this.$t('m.tabControl.directArea'),
                            tagName: 'directArea'})
                    } else {
                        this.queryData.searchCloud.push({
                            id: '0',
                            name: this.$t('m.tabControl.directArea'),
                            tagName: 'directArea'}, {
                            id: '',
                            name: this.$t('m.tabControl.allArea'),
                            tagName: 'allarea'})
                    }
                    for (let i = 0; i < this.cloudNameList.length; i++) {
                        this.cloudNameList[i].changeSta = false
                        this.cloudNameList[i].changeDel = false
                        this.cloudNameList[i].delOpen = false
                        this.cloudNameList[i].name = 'cloudName' + (i + num)
                        if (this.cloudNameList[i].is_visible) {
                            this.queryData.searchCloud.push({
                                id: this.cloudNameList[i].bk_cloud_id,
                                name: this.cloudNameList[i].bk_cloud_name,
                                tagName: this.cloudNameList[i].name})
                        }
                    }
                    if (this.addClickCloud) {
                        this.tabName = 'cloudName' + (this.cloudNameList.length + num - 1)
                        this.restoreData()
                        this.allIdNum = this.cloudNameList[this.cloudNameList.length - 1].bk_cloud_id
                        this.getInfomation()
                        this.addClickCloud = false
                    }
                    if (this.cloudShow) {
                        this.cloudShow = false
                        if (this.showAreaCloud) {
                            if (!this.cloudNameList.length) {
                                this.tabChanged('addCloud')
                            } else {
                                this.tabChanged('cloudName3')
                            }
                        }
                    }
                    this.isCloudLoading = false
                }, res => {
                    this.isCloudLoading = false
                })
            },
            /*
            ** 添加云区域数据
            */
            addCloudInfo () {
                if (this.statusCloud) { return }
                this.statusCloud = true
                if (!this.addCloudName) {
                    this.$bkMessage({
                        message: this.$t('m.message.cloudName'),
                        theme: 'error'
                    })
                    this.verify.cloud = true
                    return
                }
                const strObj = {
                    all: this.$t('m.tabControl.allArea'),
                    direac: this.$t('m.tabControl.directArea'),
                    cloudSome: this.$t('m.tabControl.cloudManag')
                }
                if (this.addCloudName === strObj.all || this.addCloudName === strObj.direac || this.addCloudName === strObj.cloudSome) {
                    this.$bkMessage({
                        message: this.$t('m.message.cloudClash'),
                        theme: 'error'
                    })
                    return
                }
                for (let i = 0; i < this.cloudNameList.length; i++) {
                    if (this.addCloudName === this.cloudNameList[i].bk_cloud_name) {
                        this.$bkMessage({
                            message: this.$t('m.message.cloudExist'),
                            theme: 'error'
                        })
                        return
                    }
                }

                let params = {}
                let appId = this.appId
                params.bk_cloud_name = this.addCloudName

                this.$store.dispatch('stall/addCloudInfo', {appId, params}).then((res) => {
                    if (res.result) {
                        this.$bkMessage({
                            message: this.$t('m.message.cloudSuccess'),
                            theme: 'success'
                        })
                        this.addClickCloud = true
                        res.data.name = 'cloudName' + (this.cloudNameList.length + 4)
                        res.data.changeSta = false
                        res.data.changeDel = false
                        res.data.delOpen = false
                        this.cloudNameList.push(res.data)
                        this.queryData.searchCloud.push({
                            id: res.data.bk_cloud_id,
                            name: res.data.bk_cloud_name,
                            tagName: res.data.name})
                        this.$refs.childs.addNewItem(res.data)
                        this.addCloudName = ''
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.statusCloud = false
                })
            },
            /*
            ** 改变选框状态
            */
            getTrue (arr) {
                return !arr.some((ar) => !ar.checkedBox)
            },
            changeTrue (arr) {
                return !arr.some((ar) => ar.checkedBox)
            },
            // 分装选取方法
            changeStatus (list) {
                this.areaDoInfo = {
                    updata: false,
                    sava: false,
                    reinstall: false,
                    uninstall: false,
                    remove: false,
                    stop: false
                }

                if (list.length) {
                    this.installStatus = {
                        updata: false,
                        reset: false,
                        unload: false,
                        break: false,
                        remove: false,
                        compile: false
                    }
                } else {
                    this.installStatus = {
                        updata: true,
                        reset: true,
                        unload: true,
                        break: true,
                        remove: true,
                        compile: true
                    }
                }
            },
            // 云区域
            cloudInputValue (index, item) {
                let length = this.cloudList.length
                item.checkedBox = !item.checkedBox
                this.cloudStatus = this.getTrue(this.cloudList)
                this.cloneNode = this.changeTrue(this.cloudList)

                if (this.areaCheckList.length !== this.cloudList.length && item.checkedBox) {
                    this.areaCheckList.push(item)
                }

                for (let i = this.areaCheckList.length - 1; i >= 0; i--) {
                    if (this.areaCheckList[i].id === item.id && !item.checkedBox) {
                        this.areaCheckList.splice(i, 1)
                    }
                }
                this.changeStatus(this.areaCheckList)

                if (this.allIdNum) {
                    for (let i = 0; i < this.proxyList.length; i++) {
                        if (!this.proxyList[i].checkedBox) {
                            this.cloudStatus = false
                            return
                        } else {
                            if (this.agentList.length) {
                                for (let j = 0; j < this.agentList.length; j++) {
                                    if (!this.agentList[j].checkedBox) {
                                        this.cloudStatus = false
                                        return
                                    } else {
                                        this.cloudStatus = true
                                    }
                                }
                            } else {
                                this.cloudStatus = true
                            }
                        }
                    }
                }
                // if (this.areaCheckList.length === 0) {
                //     this.cloudProxy.agent = false
                // } else {
                //     if (item.node_type === 'PROXY') {
                //         this.cloudProxy.agent = true
                //         this.cloudProxy.status = 'PAGENT'
                //     } else if (item.node_type === 'PAGENT') {
                //         this.cloudProxy.agent = true
                //         this.cloudProxy.status = 'PROXY'
                //     }
                // }
                // for (let i = this.areaCheckList.length - 1; i >= 0; i--) {
                //     if (this.cloudProxy.agent === true && (this.areaCheckList[i].node_type === this.cloudProxy.status)) {
                //         for (let j = 0; j < this.cloudList.length; j++) {
                //             if (this.areaCheckList[i].id === this.cloudList[j].id) {
                //                 this.cloudList[j].checkedBox = false
                //             }
                //         }
                //         this.areaCheckList.splice(i, 1)
                //     }
                // }
            },
            cloudInput () {
                this.cloudProxy.agent = false
                // this.areaCheckList = []
                this.cloudStatus = !this.cloudStatus
                if (this.cloudStatus) {
                    for (let i = 0; i < this.cloudList.length; i++) {
                        this.cloudList[i].checkedBox = true
                        this.areaCheckList.push(this.cloudList[i])
                    }
                    for (let j = 0; j < this.proxyList.length; j++) {
                        this.proxyList[j].checkedBox = true
                        // this.areaCheckList.push(this.proxyList[i])
                    }
                } else {
                    for (let i = 0; i < this.cloudList.length; i++) {
                        this.cloudList[i].checkedBox = false
                        for (let j = this.areaCheckList.length - 1; j >= 0; j--) {
                            if (this.areaCheckList[j].id === this.cloudList[i].id) {
                                this.areaCheckList.splice(j, 1)
                            }
                        }
                    }
                    for (let j = 0; j < this.proxyList.length; j++) {
                        this.proxyList[j].checkedBox = false
                        // this.areaCheckList.push(this.proxyList[i])
                    }
                }
                for (let i = this.areaCheckList.length - 1; i >= 0; i--) {
                    if (this.areaCheckList[i].job_result.status === 'RUNNING' || this.areaCheckList[i].job_result.status === 'QUEUE') {
                        this.areaCheckList.splice(i, 1)
                    }
                }
                for (let i = 0; i < this.cloudList.length; i++) {
                    if (this.cloudList[i].job_result.status === 'RUNNING' || this.cloudList[i].job_result.status === 'QUEUE') {
                        this.cloudList[i].checkedBox = false
                    }
                }
                this.cloudStatus = this.getTrue(this.cloudList)
                this.cloneNode = this.changeTrue(this.cloudList)
                this.changeStatus(this.areaCheckList)
            },
            /*
            ** 显示和隐藏添加直连区域Agent框
            */
            addArea () {
                if (this.excelOpen.status) {
                    this.saveUpdata.infoList = []
                }
                this.addAreaAgent = true
                this.addShade = true
                this.queryData.queryDisabled = {
                    set: true,
                    module: true,
                    cloud: true,
                    searchBtn: true,
                    searchInput: true
                }
            },
            openExcelInfo () {
                if (this.aProxy) {
                    this.addCloud()
                    return
                }
                if (this.tabName === 'directArea') {
                    if (this.addAreaAgent) {
                        this.excelOpen.show = false
                    } else {
                        this.excelOpen.show = true
                    }
                } else {
                    if (this.addAreaAgent || this.curCloudProxyStatus.valid_count <= 0) {
                        this.excelOpen.show = false
                    } else {
                        this.excelOpen.show = true
                    }
                }
            },
            addExcelArea (e) {
                if (this.addAreaAgent) { return }
                if (!e.target.files[0]) { return }
                let fileInfo = e.target.files[0]
                let fileName = fileInfo.name
                this.saveUpdata.infoName = fileName

                let fileReg = /.xlsx$/
                if (fileReg.test(fileName)) {
                    this.excelOpen.excelName = fileName
                    let _this = this
                    let inputDOM = this.$refs.inputer
                    // 通过DOM取文件数据
                    this.file = event.currentTarget.files[0]
                    // 是否将文件读取为二进制字符串
                    let rABS = false
                    let f = this.file
                    let reader = new FileReader()
                    // if (!FileReader.prototype.readAsBinaryString) {
                    FileReader.prototype.readAsBinaryString = (f) => {
                        let binary = ''
                        // 是否将文件读取为二进制字符串
                        let rABS = false
                        let pt = this
                        // 读取完成的数据
                        let wb
                        let outdata
                        let reader = new FileReader()
                        reader.onload = (e) => {
                            let bytes = new Uint8Array(reader.result)
                            let length = bytes.byteLength
                            for (let i = 0; i < length; i++) {
                                binary += String.fromCharCode(bytes[i])
                            }
                            let XLSX = require('xlsx')
                            wb = XLSX.read(binary, {
                                type: 'binary'
                            })
                            // outdata就是你想要的东西
                            outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]])
                            // 保存数据
                            this.saveUpdata.infoList = outdata
                        }
                        reader.readAsArrayBuffer(f)
                    }
                    if (rABS) {
                        reader.readAsArrayBuffer(f)
                    } else {
                        reader.readAsBinaryString(f)
                    }
                } else {
                    this.$bkMessage({
                        message: this.$t('m.addNewInfo.fileError'),
                        theme: 'error'
                    })
                }
            },
            excelSubmit () {
                if (!this.excelOpen.excelName) { return }
                this.excelOpen.show = !this.excelOpen.show
                this.addAreaAgent = true
                this.addShade = true
                this.queryData.queryDisabled = {
                    set: true,
                    module: true,
                    cloud: true,
                    searchBtn: true,
                    searchInput: true
                }
                this.excelOpen.excelName = ''
                this.excelOpen.excelVal = ''
                this.excelOpen.status = false
            },
            closeSilder () {
                this.excelOpen.status = true
                this.excelOpen.excelName = ''
                this.excelOpen.excelVal = ''
            },
            // 下载模板
            downLoadExcel () {
                require.ensure([], () => {
                    const { exportJson } = require('../../vendor/Export2Excel')
                    const tHeader = [this.$t('m.addNewInfo.address'), this.$t('m.addNewInfo.operat'), this.$t('m.addNewInfo.port'), this.$t('m.addNewInfo.account'), this.$t('m.addNewInfo.password')]
                    const filterVal = this.$t('m.addNewInfo.openExcel')
                    const data = [['xxx.xxx.xxx.xxx', 'LINUX', '8080', 'root', '123456']]
                    exportJson(tHeader, data, this.$t('m.addNewInfo.tableName'))
                })
            },
            /*
            ** 显示和隐藏添加云区域Agent框
            */
            addCloud () {
                if (this.curCloudProxyStatus.valid_count <= 0) {
                    return
                }
                let self = this
                // 当前proxy在编辑
                if (this.aProxy) {
                    this.$bkInfo({
                        title: this.$t('m.clickBtn.confirm'),
                        content: this.$t('m.message.proxy'),
                        confirmFn () {
                            self.toggleAgentEditor()
                        }
                    })
                } else {
                    this.aProxy = false
                    this.addAreaAgent = true
                    this.addShade = true
                    this.queryData.queryDisabled = {
                        set: true,
                        module: true,
                        cloud: true,
                        searchBtn: true,
                        searchInput: true
                    }
                }
            },
            toggleAgentEditor () {
                if (this.addAreaAgent) {
                    this.addAreaAgent = !this.addAreaAgent
                    this.aProxy = this.aProxy
                } else {
                    this.addAreaAgent = this.addAreaAgent
                    this.aProxy = !this.aProxy
                }
                this.addShade = false
                this.queryData.queryDisabled = {
                    set: false,
                    module: false,
                    cloud: false,
                    searchBtn: false,
                    searchInput: false
                }
            },
            addProxy () {
                if (this.curCloudProxyStatus.total >= 2) {
                    return
                }
                let self = this
                // 当前agent在编辑
                if (this.addAreaAgent) {
                    this.$bkInfo({
                        title: this.$t('m.clickBtn.confirm'),
                        content: this.$t('m.message.agent'),
                        confirmFn () {
                            self.toggleProxyEditor()
                        }
                    })
                } else {
                    this.aProxy = true
                    this.addAreaAgent = false
                    this.addShade = true
                    this.queryData.queryDisabled = {
                        set: true,
                        module: true,
                        cloud: true,
                        searchBtn: true,
                        searchInput: true
                    }
                }
            },
            toggleProxyEditor () {
                if (this.addAreaAgent) {
                    this.addAreaAgent = !this.addAreaAgent
                    this.aProxy = this.aProxy
                } else {
                    this.addAreaAgent = this.addAreaAgent
                    this.aProxy = !this.aProxy
                }
                this.addShade = false
                this.queryData.queryDisabled = {
                    set: false,
                    module: false,
                    cloud: false,
                    searchBtn: false,
                    searchInput: false
                }
            },
            /*
            ** 选择编辑类型
            */
            changeComplie (item, index) {
                if (this.compStatus) {
                    return
                }
                this.complieIndex.index = index
                this.complieIndex.windows = !!(item.title === 'WINDOWS')
                this.complieIndex.windowsCyg = !!(item.title === 'WINDOWSCYGWIN')
                this.complieIndex.linux = !!(item.title === 'LINUX')
                this.complieIndex.aix = !!(item.title === 'AIX')
                let arrWin = []
                let arrWinCyg = []
                let arrLin = []
                let arrAix = []
                for (let i = 0; i < this.areaCheckList.length; i++) {
                    if (this.complieIndex.windows && this.areaCheckList[i].os_type === 'WINDOWS' && !(this.areaCheckList[i].has_cygwin)) {
                        arrWin.push(this.areaCheckList[i].conn_ip)
                        this.compileInfo.connIp = arrWin.join(',')
                    } else if (this.complieIndex.windowsCyg && this.areaCheckList[i].os_type === 'WINDOWS' && this.areaCheckList[i].has_cygwin) {
                        arrWinCyg.push(this.areaCheckList[i].conn_ip)
                        this.compileInfo.connIp = arrWinCyg.join(',')
                    } else if (this.complieIndex.linux && this.areaCheckList[i].os_type === 'LINUX') {
                        arrLin.push(this.areaCheckList[i].conn_ip)
                        this.compileInfo.connIp = arrLin.join(',')
                    } else if (this.complieIndex.aix && this.areaCheckList[i].os_type === 'AIX') {
                        arrAix.push(this.areaCheckList[i].conn_ip)
                        this.compileInfo.connIp = arrAix.join(',')
                    }
                }
            },
            /*
            ** 导入CMDB
            */
            openAddCmdb () {
                if (this.aProxy) {
                    this.addCloud()
                    return
                }
                if (this.tabName === 'directArea') {
                    if (this.addAreaAgent) {
                        this.cmdbSettings.isShow = false
                    } else {
                        this.getAddCmdb()
                        this.cmdbSettings.isShow = true
                        this.cmdb = {
                            node: false,
                            continue: false,
                            add: true
                        }
                    }
                } else {
                    if (this.addAreaAgent || this.curCloudProxyStatus.valid_count <= 0) {
                        this.cmdbSettings.isShow = false
                    } else {
                        this.getAddCmdb()
                        this.cmdbSettings.isShow = true
                        this.cmdb = {
                            node: false,
                            continue: false,
                            add: true
                        }
                    }
                }
            },
            getAddCmdb () {
                let appId = this.appId
                if (!appId) {
                    this.isDataLoading = false
                    return
                }
                this.addCmdb = []
                this.$store.dispatch('stall/getCmdbInfo', {appId}).then((res) => {
                    this.addCmdb = res.data
                    for (let i = 0; i < this.addCmdb.length; i++) {
                        this.addCmdb[i].typeStatus = false
                        this.addCmdb[i].iconStatus = false
                        for (let j = 0; j < this.addCmdb[i].Children.length; j++) {
                            this.addCmdb[i].Children[j].childrenStatus = false
                        }
                    }
                    this.getAddCmdbInfo()
                }, res => {
                    if (this.appId === null) {
                        return
                    }
                    if (this.errorCode) {
                        this.errorCode = false
                        return
                    }
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            changTypeStatus (index, item) {
                this.addCmdb[index].iconStatus = !this.addCmdb[index].iconStatus
                this.addCmdb = JSON.parse(JSON.stringify(this.addCmdb))
            },
            // 导入cmdb总选状态
            changeCmdb (index, item) {
                this.addCmdb[index].typeStatus = !this.addCmdb[index].typeStatus
                for (let i = 0; i < this.addCmdb[index].Children.length; i++) {
                    this.addCmdb[index].Children[i].childrenStatus = !!this.addCmdb[index].typeStatus
                    this.addCmdb = JSON.parse(JSON.stringify(this.addCmdb))
                }
            },
            // 导入cmdb单选状态
            changeSmallStatus (index, innum, info) {
                this.addCmdb[index].Children[innum].childrenStatus = !this.addCmdb[index].Children[innum].childrenStatus
                for (let i = 0; i < this.addCmdb[index].Children.length; i++) {
                    if (!this.addCmdb[index].Children[i].childrenStatus) {
                        this.addCmdb[index].typeStatus = false
                        this.addCmdb = JSON.parse(JSON.stringify(this.addCmdb))
                        return
                    } else {
                        this.addCmdb[index].typeStatus = true
                        this.addCmdb = JSON.parse(JSON.stringify(this.addCmdb))
                    }
                }
            },
            // 查看导入node信息
            lookNodeInfo () {
                this.cmdb.continue = false
                this.cmdb.add = true
                this.cmdb.note = false
                this.cmdb.nodeInfo = []
                this.cmdb.wipeList = []
                this.cmdb.list = []
                for (let i = 0; i < this.addCmdb.length; i++) {
                    for (let j = 0; j < this.addCmdb[i].Children.length; j++) {
                        if (this.addCmdb[i].Children[j].childrenStatus) {
                            for (let t = 0; t < this.addCmdb[i].Children[j].HOSTS.length; t++) {
                                this.cmdb.list.push(this.addCmdb[i].Children[j].HOSTS[t])
                            }
                        }
                    }
                }
                if (this.cmdb.list.length === 0) {
                    this.$bkMessage({
                        message: this.$t('m.message.checkInfo'),
                        theme: 'error'
                    })
                    return
                }
                let params = {}
                params.bk_cloud_id = this.allIdNum
                params.hosts = this.cmdb.list
                let appId = this.appId
                this.$store.dispatch('stall/checkCmdbInfo', {appId, params}).then((res) => {
                    let listInfo = []
                    let str = {}
                    for (let i = 0; i < this.cmdb.list.length; i++) {
                        if (!str[this.cmdb.list[i]]) {
                            listInfo.push(this.cmdb.list[i])
                            str[this.cmdb.list[i]] = 1
                        }
                    }
                    this.cmdb.list = listInfo
                    this.continueNodeInfo()
                }, res => {
                    this.cmdb.continue = true
                    this.cmdb.add = false
                    this.cmdb.note = true
                    this.cmdb.nodeInfo = Object.values(res.data.messages[0])
                    this.cmdb.wipeList = Object.keys(res.data.messages[0])
                    let listInfo = []
                    for (let i = 0; i < this.cmdb.list.length; i++) {
                        if (this.cmdb.wipeList.indexOf(this.cmdb.list[i]) < 0) {
                            listInfo.push(this.cmdb.list[i])
                        }
                    }
                    this.cmdb.list = listInfo
                    this.showOne.length = this.cmdb.list.length
                    this.showOne.status = !(this.cmdb.list.length)
                })
            },
            continueNodeInfo () {
                if (this.showOne.status) {
                    return
                }
                this.cmdbSettings.isShow = false
                this.addAreaAgent = true
                this.addShade = true
                this.queryData.queryDisabled = {
                    set: true,
                    module: true,
                    cloud: true,
                    searchBtn: true,
                    searchInput: true
                }
            },
            goBackCmdb () {
                this.cmdb.continue = false
                this.cmdb.add = true
                this.cmdb.note = false
                this.cmdb.nodeInfo = []
                this.cmdb.wipeList = []
                this.cmdb.list = []
            },
            /*
            ** 详细安装步骤
            */
            openStallStep (item) {
                clearInterval(this.stepInterval)
                this.customSettings.title = this.$t('m.openSlider.stepInfo')
                this.customSettings.isShow = true
                let appId = this.appId
                let id = item.id
                this.logId = item.id

                this.$store.dispatch('stall/getStepInfo', {appId, id}).then((res) => {
                    this.stepInfo = res.data.logs
                }, res => {
                    this.stepInfo = res.data.msg
                })
                this.logSetInterval()
            },
            logSetInterval () {
                let appId = this.appId
                let id = this.logId
                this.stepInterval = setInterval(() => {
                    this.$store.dispatch('stall/getStepInfo', {appId, id}).then((res) => {
                        this.stepInfo = res.data.logs
                        document.getElementsByClassName('bk-sideslider-wrapper')[0].scrollTop = document.getElementsByClassName('bk-open-window')[0].offsetHeight
                        if (res.data.status === 'FAILED' || res.data.status === 'SUCCESS' || !this.customSettings.isShow) {
                            clearInterval(this.stepInterval)
                        }
                    }, res => {
                        clearInterval(this.stepInterval)
                    })
                }, 2000)
            },
            /*
            ** 编辑
            */
            openCompileInfo (value, item) {
                const complieIndexMap = {
                    'WINDOWS': 'windows',
                    'WINDOWSCYGWIN': 'windowsCyg',
                    'LINUX': 'linux',
                    'AIX': 'aix'
                }
                let osType = item.os_type
                if (item.os_type === 'WINDOWS' && item.has_cygwin) {
                    osType = 'WINDOWSCYGWIN'
                }
                for (let key in this.complieIndex) {
                    this.complieIndex[key] = !!(complieIndexMap[osType] === key)
                }
                for (let i = 0; i < this.complieList.length; i++) {
                    this.complieList[i].status = !!(item.os_type === this.complieList[i].title)
                }
                if (item.os_type === 'WINDOWS') {
                    this.complieList[0].status = !(item.has_cygwin)
                    this.complieList[1].status = !!(item.has_cygwin)
                }
                if (item.node_type === 'PROXY') {
                    this.compileInfo.cascade_ip = item.cascade_ip
                }

                if (value === 'SAVE') {
                    if (item.doObj.sava) {
                        return
                    }
                    this.customSettings.title = this.$t('m.operateStep.compile')
                    this.customSettings.isShow = true
                    this.compStatus = true
                } else {
                    this.customSettings.isShow = false
                    this.compStatus = false
                }

                this.compileInfo = {
                    tastId: item.id,
                    connIp: item.conn_ip,
                    cascade_ip: item.cascade_ip,
                    hasCygwin: !!(item.has_cygwin),
                    ssh: item.port,
                    account: item.account,
                    way: item.auth_type,
                    password: item.password,
                    agentWay: [
                        {
                            id: 'PASSWORD',
                            name: this.$t('m.addNode.password')
                        },
                        {
                            id: 'KEY',
                            name: this.$t('m.addNode.key')
                        }
                    ],
                    verify: {
                        ip: false,
                        cascade_ip: false,
                        port: false,
                        acc: false,
                        pass: false
                    },
                    doObj: {
                        reinstall: item.doObj.reinstall,
                        uninstall: item.doObj.uninstall,
                        remove: item.doObj.remove
                    },
                    bk_cloud_id: item.bk_cloud_id,
                    node_type: item.node_type,
                    os_type: item.os_type,
                    key: item.key,
                    id: item.job_result.job_id
                }
            },
            /*
            ** 编辑验证
            */
            compileAgent (type) {
                // 校验
                let reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
                let stal = /^\+?[1-9][0-9]*$/

                switch (type)
                {
                    case 'loginIp':
                        this.compileInfo.verify.loginIp = !reg.test(this.compileInfo.loginIp)
                        break
                    case 'ssh':
                        this.compileInfo.verify.port = !stal.test(this.compileInfo.ssh)
                        break
                    case 'account':
                        this.compileInfo.verify.acc = !this.compileInfo.account
                        break
                    case 'way':
                        if (this.compileInfo.way === 'PASSWORD') {
                            this.compileInfo.verify.pass = !this.compileInfo.password
                        }
                        break
                }
            },
            /*
            ** 编辑操作
            */
            compileAgentInfo (value, indentify, item) {
                if (indentify) {
                    if (this.compileInfo.verify.acc || this.compileInfo.account === '') {
                        this.compileInfo.verify.acc = true
                        return
                    }
                    if (this.compileInfo.verify.port || this.compileInfo.ssh === '') {
                        this.compileInfo.verify.port = true
                        return
                    }
                    if (value === 'REINSTALL' || value === 'SAVE') {
                        if (this.compileInfo.way === 'PASSWORD') {
                            if (this.compileInfo.verify.pass || this.compileInfo.password === '') {
                                this.compileInfo.verify.pass = true
                                return
                            }
                        } else if (this.compileInfo.way === 'KEY') {
                            if (this.compileInfo.key === '') {
                                this.$bkMessage({
                                    message: this.$t('m.addNode.upload'),
                                    theme: 'error'
                                })
                                return
                            }
                        }
                    }
                }

                let params = {}
                params.hosts = []
                let obj = {}
                let msg = this.$t('m.message.taskBegin')

                switch (value)
                {
                    case 'SAVE':
                        if (item && item.doObj.sava) {
                            return
                        }
                        params.op_type = 'SAVE'
                        msg = this.$t('m.message.task.saveTask')
                        break
                    case 'REINSTALL':
                        if (item && item.doObj.reinstall) {
                            return
                        }
                        params.op_type = 'REINSTALL'
                        msg = this.$t('m.message.task.reinstallTask')
                        break
                    case 'UNINSTALL':
                        if (item && item.doObj.uninstall) {
                            return
                        }
                        params.op_type = 'UNINSTALL'
                        msg = this.$t('m.message.task.uninstallTask')
                        break
                    case 'REMOVE':
                        if (item && item.doObj.remove) {
                            return
                        }
                        params.op_type = 'REMOVE'
                        msg = this.$t('m.message.task.removeTask')
                        break
                }

                params.bk_cloud_id = this.compileInfo.bk_cloud_id
                params.node_type = this.compileInfo.node_type

                if (indentify === 'indentify') {
                    obj.conn_ips = this.compileInfo.connIp
                    if (this.compileInfo.node_type === 'PROXY') {
                        obj.cascade_ip = this.compileInfo.cascade_ip
                    }
                    obj.port = this.compileInfo.ssh
                    obj.account = this.compileInfo.account
                    if (this.compileInfo.node_type === 'LINUX') {
                        obj.cascade_ip = this.compileInfo.loginIp
                    }
                    if (this.compileInfo.way === 'PASSWORD') {
                        obj.auth_type = 'PASSWORD'
                        obj.password = this.$encrypt(this.compileInfo.password)
                    } else if (this.compileInfo.way === 'KEY') {
                        obj.auth_type = 'KEY'
                        obj.key = this.compileInfo.key
                    }
                } else {
                    obj.conn_ips = this.compileInfo.connIp
                    params.op_type = this.termDelete.val
                }

                params.hosts.push(obj)
                let appId = this.appId

                for (let i = 0; i < this.cloudList.length; i++) {
                    if (this.compileInfo.id === this.cloudList[i].job_result.job_id) {
                        this.cloudList[i].checkedBox = false
                    }
                }
                for (let i = 0; i < this.areaCheckList.length; i++) {
                    if (this.compileInfo.id === this.areaCheckList[i].job_result.job_id) {
                        this.areaCheckList.splice(i, 1)
                    }
                }

                if (params.op_type === 'REINSTALL' || params.op_type === 'UNINSTALL') {
                    if (params.node_type !== 'PROXY' && params.bk_cloud_id !== '0') {
                        let valusPrxy = false
                        for (let i = 0; i < this.proxyList.length; i++) {
                            if (this.proxyList[i].job_result.status === 'SUCCESS') {
                                valusPrxy = true
                                break
                            }
                        }
                        if (!valusPrxy) {
                            this.$bkMessage({
                                message: '没有安装成功的PROXY，不能进行P-AGENT的重装卸载操作！',
                                theme: 'warning'
                            })
                            return
                        }
                    }
                }
                if (this.compileAgentStatus) {
                    return
                }
                this.compileAgentStatus = true

                this.$store.dispatch('stall/installAgent', {appId, params}).then((res) => {
                    if (res.result) {
                        this.$bkMessage({
                            message: msg,
                            theme: 'success'
                        })
                        this.getInfomation()
                        this.customSettings.isShow = false
                        this.compStatus = false
                        this.cloudStatus = false
                        this.closeAll()
                    }
                }, res => {
                    this.closeAll()
                    let errMsg = ''
                    if (this.termDelete.val === 'REINSTALL') {
                        this.customSettings.title = this.$t('m.operateStep.compile')
                        this.customSettings.isShow = true
                        this.compStatus = true
                        errMsg = res.data.msg
                        const complieIndexMap = {
                            'WINDOWS': 'windows',
                            'WINDOWSCYGWIN': 'windowsCyg',
                            'LINUX': 'linux',
                            'AIX': 'aix'
                        }
                        let osType = this.compileInfo.os_type
                        if (this.compileInfo.os_type === 'WINDOWS' && this.compileInfo.has_cygwin) {
                            osType = 'WINDOWSCYGWIN'
                        }
                        for (let key in this.complieIndex) {
                            this.complieIndex[key] = !!(complieIndexMap[osType] === key)
                        }
                        for (let i = 0; i < this.complieList.length; i++) {
                            this.complieList[i].status = !!(this.compileInfo.os_type === this.complieList[i].title)
                        }
                    } else {
                        this.customSettings.isShow = false
                        this.compStatus = false
                        errMsg = res.data.msg
                    }
                    this.$bkMessage({
                        message: errMsg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.clearData()
                    this.compileAgentStatus = false
                })
            },
            /*
            ** 单个终止任务
            */
            termTask () {
                if (this.operateStatus.tableInfo) { return }
                this.operateStatus.tableInfo = true
                let appId = this.appId
                let id = this.compileInfo.id
                this.$store.dispatch('stall/stopTask', {appId, id}).then((res) => {
                    this.$bkMessage({
                        message: this.$t('m.message.task.stopTask'),
                        theme: 'success'
                    })
                    this.closeAll()
                    this.getInfomation()
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                    this.closeAll()
                    this.getInfomation()
                }).finally(() => {
                    this.operateStatus.tableInfo = false
                    this.stopInfo.showthis = false
                })
            },
            openTerm (item, value) {
                let reinsMsg = value === 'REINSTALL' && item.doObj.reinstall
                let uninsMsg = value === 'UNINSTALL' && item.doObj.uninstall
                let removeMsg = value === 'REMOVE' && item.doObj.remove
                let stopMsg = value === 'STOP' && item.doObj.stop

                if (reinsMsg || uninsMsg || removeMsg || stopMsg) {
                    return
                }

                this.compileInfo = {
                    tastId: item.id,
                    connIp: item.conn_ip,
                    hasCygwin: false,
                    ssh: item.port,
                    account: item.account,
                    way: item.auth_type,
                    password: item.password,
                    agentWay: [
                        {
                            id: 'PASSWORD',
                            name: this.$t('m.addNode.password')
                        },
                        {
                            id: 'KEY',
                            name: this.$t('m.addNode.key')
                        }
                    ],
                    verify: {
                        ip: false,
                        cascade_ip: false,
                        port: false,
                        acc: false,
                        pass: false
                    },
                    doObj: {
                        reinstall: item.doObj.reinstall,
                        uninstall: item.doObj.uninstall,
                        remove: item.doObj.remove
                    },
                    bk_cloud_id: item.bk_cloud_id,
                    node_type: item.node_type,
                    os_type: item.os_type,
                    key: item.key,
                    id: item.job_result.job_id
                }
                this.termDelete = {
                    shade: !this.termDelete.shade,
                    deleteOpenTerm: !this.termDelete.deleteOpenTerm,
                    val: value
                }
                if (value === 'STOP') {
                    let appId = this.appId
                    let id = this.compileInfo.id
                    this.$store.dispatch('stall/getTasks', {appId, id}).then((res) => {
                        let listAgent = res.data.items
                        let arr = []
                        for (let i = 0; i < listAgent.length; i++) {
                            for (let j = 0; j < listAgent[i].hosts.length; j++) {
                                if (listAgent[i].hosts[j].status === 'RUNNING' || listAgent[i].hosts[j].status === 'QUEUE') {
                                    arr.push(listAgent[i])
                                }
                            }
                        }
                        this.stopInfo.showthis = arr.length > 1
                    }, res => {
                        this.stopInfo.showthis = false
                    })
                }
            },
            closeAll () {
                this.termDelete.shade = false
                this.termDelete.deleteOpenTerm = false
                this.stopInfo.showthis = false
            },
            /*
            ** 批量操作
            */
            batchOpear (value, status) {
                for (let key in this.installStatus) {
                    if (this.installStatus[key]) {
                        return
                    }
                }

                this.clearBatchInfo()

                let msg = this.$t('m.message.task.checkClash') + ' ' + this.$t('m.message.task.doNot')
                let checkPro = false
                let checkage = false
                for (let i = 0; i < this.areaCheckList.length; i++) {
                    let areaSta = this.areaCheckList[i]
                    if (areaSta.node_type === 'PROXY') {
                        checkPro = true
                    } else if (areaSta.node_type === 'PAGENT') {
                        checkage = true
                    }
                    if (areaSta.job_result.status === 'RUNNING' || areaSta.job_result.status === 'QUEUE') {
                        msg = this.$t('m.message.task.runClash')
                    }
                }
                if ((value === 'REMOVE' || value === 'UNINSTALL') && checkPro && this.agentList.length) {
                    this.$bkMessage({
                        message: this.$t('m.otherAdd.infoSta'),
                        theme: 'error'
                    })
                    return
                }
                if (checkPro && checkage) {
                    this.areaDoInfo = {
                        updata: true,
                        sava: true,
                        reinstall: true,
                        uninstall: true,
                        remove: true,
                        stop: false
                    }
                    msg = this.$t('m.message.task.proxyClash')
                }

                // if (value === 'UPGRADE' && this.areaDoInfo.updata === true) {
                //     this.$bkMessage({
                //         message: msg + ' ' + this.$t('m.message.batch.upgrade'),
                //         theme: 'error'
                //     })
                //     return
                // }
                if (value === 'SAVE' && this.areaDoInfo.sava === true) {
                    this.$bkMessage({
                        message: msg + ' ' + this.$t('m.message.batch.compile'),
                        theme: 'error'
                    })
                    return
                }
                if (value === 'REINSTALL' && this.areaDoInfo.reinstall === true) {
                    this.$bkMessage({
                        message: msg + ' ' + this.$t('m.message.batch.reinstall'),
                        theme: 'error'
                    })
                    return
                }
                if (value === 'UNINSTALL' && this.areaDoInfo.uninstall === true) {
                    this.$bkMessage({
                        message: msg + ' ' + this.$t('m.message.batch.uninstall'),
                        theme: 'error'
                    })
                    return
                }
                if (value === 'REMOVE' && this.areaDoInfo.remove === true) {
                    this.$bkMessage({
                        message: msg + ' ' + this.$t('m.message.batch.remove'),
                        theme: 'error'
                    })
                    return
                }
                if (value === 'STOP' && this.areaDoInfo.stop === true) {
                    this.$bkMessage({
                        message: msg + ' ' + this.$t('m.message.batch.stop'),
                        theme: 'error'
                    })
                    return
                }

                let params = {}
                params.hosts = []

                if (this.tabName === 'directArea') {
                    params.bk_cloud_id = this.allIdNum
                    params.node_type = 'AGENT'
                } else {
                    params.bk_cloud_id = this.allIdNum
                    for (let i = 0; i < this.areaCheckList.length; i++) {
                        params.node_type = this.areaCheckList[i].node_type
                    }
                }

                this.compileInfo.bk_cloud_id = this.allIdNum
                this.compileInfo.node_type = params.node_type

                let obj = {}
                obj.conn_ips = ''
                let arrIp = []
                if (value !== 'SAVE') {
                    for (let i = 0; i < this.areaCheckList.length; i++) {
                        arrIp.push(this.areaCheckList[i].conn_ip)
                    }
                    obj.conn_ips = arrIp.join(',')
                }

                params.hosts.push(obj)
                let appId = this.appId

                let valueInfo = false
                if (this.areaCheckList.length > 1) {
                    const valueType = this.areaCheckList[0].node_type
                    for (let i = 1; i < this.areaCheckList.length; i++) {
                        if (valueType !== this.areaCheckList[i].node_type) {
                            valueInfo = true
                        }
                    }
                }
                if (valueInfo) {
                    this.$bkMessage({
                        message: this.$t('m.addNewInfo.noAlong'),
                        theme: 'error'
                    })
                    return
                }

                if (this.operateStatus.checkStatus) { return }
                this.operateStatus.checkStatus = true

                switch (value)
                {
                    case 'STOP':
                        let str = ''
                        let arr = []
                        for (let i = 0; i < this.areaCheckList.length; i++) {
                            arr.push(this.areaCheckList[i].job_result.job_id)
                        }
                        str = arr.join(',')
                        this.$store.dispatch('stall/batchStopTask', {appId, str}).then((res) => {
                            this.$bkMessage({
                                message: this.$t('m.message.task.stopTask'),
                                theme: 'success'
                            })
                            this.cloudStatus = false
                            this.clearData()
                            this.getInfomation()
                        }, res => {
                            this.$bkMessage({
                                message: res.data.msg,
                                theme: 'error'
                            })
                            this.getInfomation()
                        }).finally(() => {
                            this.operateStatus.checkStatus = false
                        })
                        break
                    case 'SAVE':
                        params.op_type = 'SAVE'
                        this.customSettings.title = this.$t('m.operateStep.compile')
                        this.customSettings.isShow = true
                        this.compStatus = false

                        this.compileInfo.connIp = ''
                        this.complieIndex = {
                            windows: false,
                            windowsCyg: false,
                            linux: false,
                            aix: false
                        }
                        for (let i = 0; i < this.complieList.length; i++) {
                            this.complieList[i].status = false
                        }

                        let arrWin = []
                        let arrWinCyg = []
                        let arrLin = []
                        let arrAix = []

                        for (let i = 0; i < this.areaCheckList.length; i++) {
                            if (this.areaCheckList[i].os_type === 'WINDOWS' && !(this.areaCheckList[i].has_cygwin)) {
                                this.complieList[0].status = true
                                arrWin.push(this.areaCheckList[i].conn_ip)
                            } else if (this.areaCheckList[i].os_type === 'WINDOWS' && this.areaCheckList[i].has_cygwin) {
                                this.complieList[1].status = true
                                arrWinCyg.push(this.areaCheckList[i].conn_ip)
                            } else if (this.areaCheckList[i].os_type === 'LINUX') {
                                this.complieList[2].status = true
                                arrLin.push(this.areaCheckList[i].conn_ip)
                            } else if (this.areaCheckList[i].os_type === 'AIX') {
                                this.complieList[3].status = true
                                arrAix.push(this.areaCheckList[i].conn_ip)
                            }
                        }
                        this.operateStatus.checkStatus = false

                        if (this.complieList[0].status) {
                            this.complieIndex.windows = true
                            this.complieIndex.index = 0
                            this.compileInfo.connIp = arrWin.join(',')
                            obj.conn_ips = this.compileInfo.connIp
                            return
                        }
                        if (this.complieList[1].status) {
                            this.complieIndex.windowsCyg = true
                            this.complieIndex.index = 1
                            this.compileInfo.connIp = arrWinCyg.join(',')
                            obj.conn_ips = this.compileInfo.connIp
                            return
                        }
                        if (this.complieList[2].status) {
                            this.complieIndex.linux = true
                            this.complieIndex.index = 2
                            this.compileInfo.connIp = arrLin.join(',')
                            obj.conn_ips = this.compileInfo.connIp
                            return
                        }
                        if (this.complieList[3].status) {
                            this.complieIndex.aix = true
                            this.complieIndex.index = 3
                            this.compileInfo.connIp = arrAix.join(',')
                            obj.conn_ips = this.compileInfo.connIp
                        }
                        break
                    case 'UPGRADE':
                        params.op_type = 'UPGRADE'
                        this.cloudStatus = false
                        this.batchOpearAjax(params)
                        break
                    case 'REINSTALL':
                        params.op_type = 'REINSTALL'
                        this.cloudStatus = false
                        this.batchOpearAjax(params)
                        break
                    case 'UNINSTALL':
                        params.op_type = 'UNINSTALL'
                        this.cloudStatus = false
                        this.batchOpearAjax(params)
                        break
                    case 'REMOVE':
                        params.op_type = 'REMOVE'
                        this.batchOpearAjax(params)
                        this.cloudStatus = false
                        break
                }
            },
            clearBatchInfo () {
                this.compileInfo = {
                    tastId: '',
                    hasCygwin: false,
                    ssh: '',
                    account: '',
                    way: 'PASSWORD',
                    password: '',
                    agentWay: [
                        {
                            id: 'PASSWORD',
                            name: this.$t('m.addNode.password')
                        },
                        {
                            id: 'KEY',
                            name: this.$t('m.addNode.key')
                        }
                    ],
                    verify: {
                        ip: false,
                        cascade_ip: false,
                        port: false,
                        acc: false,
                        pass: false
                    },
                    doObj: {
                        reinstall: false,
                        uninstall: false,
                        remove: false
                    },
                    bk_cloud_id: '0',
                    node_type: 'PAGENT',
                    id: null,
                    os_type: '',
                    key: '',
                    connIp: ''
                }

                this.areaDoInfo = {
                    updata: false,
                    sava: false,
                    reinstall: false,
                    uninstall: false,
                    remove: false,
                    stop: false
                }
                for (let i = 0; i < this.areaCheckList.length; i++) {
                    if (this.areaCheckList[i].doObj.updata) {
                        this.areaDoInfo.updata = true
                    }
                    if (this.areaCheckList[i].doObj.sava) {
                        this.areaDoInfo.sava = true
                    }
                    if (this.areaCheckList[i].doObj.reinstall) {
                        this.areaDoInfo.reinstall = true
                    }
                    if (this.areaCheckList[i].doObj.uninstall) {
                        this.areaDoInfo.uninstall = true
                    }
                    if (this.areaCheckList[i].doObj.remove) {
                        this.areaDoInfo.remove = true
                    }
                    if (this.areaCheckList[i].doObj.stop) {
                        this.areaDoInfo.stop = true
                    }
                }
                if (this.allIdNum !== '0' && this.cloudStatus && this.agentList.length !== 0) {
                    this.areaDoInfo = {
                        updata: false,
                        sava: true,
                        reinstall: true,
                        uninstall: true,
                        remove: true,
                        stop: true
                    }
                }
            },
            batchOpearAjax (params) {
                console.log(params)
                if (params.op_type === 'REINSTALL' || params.op_type === 'UNINSTALL') {
                    if (params.node_type !== 'PROXY' && params.bk_cloud_id !== '0') {
                        let valusPrxy = false
                        for (let i = 0; i < this.proxyList.length; i++) {
                            if (this.proxyList[i].job_result.status === 'SUCCESS') {
                                valusPrxy = true
                                break
                            }
                        }
                        if (!valusPrxy) {
                            this.$bkMessage({
                                message: '没有安装成功的PROXY，不能进行P-AGENT的重装卸载操作！',
                                theme: 'warning'
                            })
                            return
                        }
                    }
                }
                let appId = this.appId
                this.$store.dispatch('stall/installAgent', {appId, params}).then((res) => {
                    if (res.result) {
                        this.$bkMessage({
                            message: this.$t('m.message.batchTask'),
                            theme: 'success'
                        })
                        this.clearData()
                        this.getInfomation()
                    }
                }, res => {
                    this.operateStatus.checkStatus = false
                    this.batchOpear('SAVE', 'status')
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.operateStatus.checkStatus = false
                })
            },
            /*
            ** 云区域管理
            */
            changeCloud (item) {
                item.changeSta = !item.changeSta
                this.cloudNameList = JSON.parse(JSON.stringify(this.cloudNameList))
            },
            // 修改云区域名称
            saveCloud (item, index) {
                if (!item.bk_cloud_name) {
                    this.$bkMessage({
                        message: this.$t('m.message.cloudName'),
                        theme: 'error'
                    })
                    this.cloudManage.saveStatus = true
                    return
                }
                if (item.bk_cloud_name === this.$t('m.tabControl.directArea') || item.bk_cloud_name === this.$t('m.tabControl.allArea')) {
                    this.$bkMessage({
                        message: this.$t('m.message.cloudClash'),
                        theme: 'error'
                    })
                    return
                }
                if (item.bk_cloud_name === this.$t('m.tabControl.cloudManag')) {
                    this.$bkMessage({
                        message: this.$t('m.message.cloudClash'),
                        theme: 'error'
                    })
                    return
                }
                for (let i = 0; i < this.cloudNameList.length; i++) {
                    if (item.bk_cloud_name === this.cloudNameList[i].bk_cloud_name && index !== i) {
                        this.$bkMessage({
                            message: this.$t('m.message.cloudExist'),
                            theme: 'error'
                        })
                        return
                    }
                }
                this.cloudManage.saveStatus = false

                let appId = this.appId
                let params = {
                    bk_cloud_name: item.bk_cloud_name
                }
                let id = item.id
                this.$store.dispatch('stall/reviseCloud', {appId, params, id}).then((res) => {
                    for (let i = 0; i < this.cloudNameList.length; i++) {
                        if (item.bk_cloud_id === this.cloudNameList[i].bk_cloud_id) {
                            this.cloudNameList[i].bk_cloud_name = item.bk_cloud_name
                            this.changeCloud(item)
                            this.$refs.childs.changeItems(item)
                            return
                        }
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                    this.changeCloud(item)
                })
            },
            // 改变云区域可视状态
            changeSee (item, valueStatus) {
                let appId = this.appId
                let id = item.id
                let params = {}
                if (valueStatus === 'eye') {
                    this.$store.dispatch('stall/closeCloudEye', {appId, id, params}).then((res) => {
                        for (let i = 0; i < this.cloudNameList.length; i++) {
                            if (item.bk_cloud_id === this.cloudNameList[i].bk_cloud_id) {
                                item.is_visible = false
                                this.cloudNameList = JSON.parse(JSON.stringify(this.cloudNameList))
                                this.$refs.childs.deleteItems(item)
                                for (let j = 0; j < this.queryData.searchCloud.length; j++) {
                                    if (item.bk_cloud_id === this.queryData.searchCloud[j].id) {
                                        this.queryData.searchCloud.splice(j, 1)
                                        return
                                    }
                                }
                            }
                        }
                    }, res => {
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    })
                } else if (valueStatus === 'slash') {
                    this.$store.dispatch('stall/seeCloudEye', {appId, id, params}).then((res) => {
                        for (let i = 0; i < this.cloudNameList.length; i++) {
                            if (item.bk_cloud_id === this.cloudNameList[i].bk_cloud_id) {
                                item.is_visible = true
                                this.cloudNameList = JSON.parse(JSON.stringify(this.cloudNameList))
                                this.$refs.childs.deleteItems(item)
                                this.queryData.searchCloud.push({
                                    id: item.bk_cloud_id,
                                    name: item.bk_cloud_name,
                                    tagName: item.name})
                                return
                            }
                        }
                    }, res => {
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    })
                }
            },
            deleteCloud (item) {
                item.delOpen = !item.delOpen
                this.cloudNameList = JSON.parse(JSON.stringify(this.cloudNameList))
            },
            cancelCloud (item) {
                item.changeDel = false
                item.delOpen = false
                this.cloudNameList = JSON.parse(JSON.stringify(this.cloudNameList))
            },
            // 删除云区域
            changeDelete (item) {
                if (this.operateStatus.tableInfo) { return }
                this.operateStatus.tableInfo = true
                let appId = this.appId
                let params = 'bk_cloud_id' + '=' + item.bk_cloud_id
                let id = item.id

                this.$store.dispatch('stall/getOneCloud', {appId, id}).then((res) => {
                    if (!res.data.enable_delete) {
                        item.changeDel = true
                        item.delOpen = !item.delOpen
                        this.cloudNameList = JSON.parse(JSON.stringify(this.cloudNameList))
                    } else {
                        this.$store.dispatch('stall/deleteCloud', {appId, id}).then((res) => {
                            this.$bkMessage({
                                message: this.$t('m.addCloud.deleteCloud'),
                                theme: 'success'
                            })
                            for (let i = 0; i < this.cloudNameList.length; i++) {
                                if (item.bk_cloud_id === this.cloudNameList[i].bk_cloud_id) {
                                    this.cloudNameList.splice(i, 1)
                                    this.$refs.childs.closeItems(item)
                                    break
                                }
                            }
                            for (let i = 0; i < this.queryData.searchCloud.length; i++) {
                                if (item.bk_cloud_id === this.queryData.searchCloud[i].bk_cloud_id) {
                                    this.queryData.searchCloud.splice(i, 1)
                                    break
                                }
                            }
                            item.delOpen = !item.delOpen
                        }, res => {
                            this.$bkMessage({
                                message: res.data.msg,
                                theme: 'error'
                            })
                            item.delOpen = !item.delOpen
                        })
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                    item.delOpen = !item.delOpen
                }).finally(() => {
                    this.operateStatus.tableInfo = false
                })
            },
            // 新增云区域切换
            cloudAddName () {
                this.cloudNameOpera.showAdd = !this.cloudNameOpera.showAdd
            },
            /*
            ** 读取文件信息
            */
            readFile ($event) {
                let fileInfo = $event.target.files[0]
                this.compileInfo.nameFile = fileInfo.name
                let reader = new FileReader()
                if (!reader) { return }
                reader.readAsText(fileInfo)
                reader.onload = (file) => {
                    this.compileInfo.key = file.target.result
                    this.$bkMessage({
                        message: this.$t('m.addSomeInfo.successInfo'),
                        theme: 'success'
                    })
                }
                this.a = ''
            },
            /*
            ** 清空批量操作数据
            */
            clearData () {
                this.areaCheckList = []
                this.installStatus = {
                    updata: true,
                    reset: true,
                    unload: true,
                    break: true,
                    remove: true,
                    compile: true
                }
            },
            //  页面轮循
            setItervalGetInfo () {
                clearInterval(this.$store.state.stall.timeOutCheck)
                this.$store.state.stall.timeOutCheck = setInterval(() => {
                    this.checkAgentInfo()
                }, 10000)
            }
        },
        computed: {
            showOpen () {
                return this.$store.state.open
            },
            openStatus () {
                return this.$store.state.openDoor
            },
            appId () {
                return this.$store.state.stall.appliId
            }
        },
        watch: {
            appId () {
                this.restoreData()
                this.tabName = 'directArea'
                this.allIdNum = '0'
                this.cloudShow = true
                this.getCloudInfo()
                this.getInfomation()
                this.getAddCmdb()
                this.allStop()
                // 关闭CMDB
                this.cmdbSettings.isShow = false
            },
            openStatus () {
                this.restoreData()
                this.tabName = 'directArea'
                this.allIdNum = '0'
                this.cloudShow = true
                this.getCloudInfo()
                this.getInfomation()
                this.getAddCmdb()
            },
            tabName () {
                this.aProxy = false
                // 关闭CMDB
                this.cmdbSettings.isShow = false
            }
        },
        async mounted () {
            this.getInfomation()
            this.getCloudInfo()
            this.getAddCmdb()
            this.setItervalGetInfo()
            this.allStop()
            this.showAreaCloud = window.is_cloud
        }
    }
</script>

<style lang="scss" scoped>
    @import './stallScss/stall.scss'
</style>
