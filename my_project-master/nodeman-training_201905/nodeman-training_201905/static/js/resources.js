/**
 * @module: resources.js
 * @author: 蓝鲸智云
 * @create: 2018-05-10 11:39:19
 */

var BaseRestAPI = function (method, url, data, options) {
    var defaultOptions = {
        type: method,
        url: window.site + url,
        dataType: 'json',
    }
    if (method === 'GET') {
        defaultOptions.data = data
    } else {
        defaultOptions.data = data
        defaultOptions.contentType = 'application/json'
    }
    return $.ajax(Object.assign(defaultOptions, options))
}

/*
  列表类型的API
 */
var RestListAPI = function(method, url) {
    return function (data, options) {
        return BaseRestAPI(method, url, data, options)
    }
}


/*
  详情类型的API，需要替换掉URL字符串模版中的"{pk}"，以生成合法的URL
 */
var RestDetailAPI = function(method, url) {
    return function (id, data, options) {
        var requestURL = url.replace("{pk}", id)
        return BaseRestAPI(method, requestURL, data, options)
    }
}

/* Model API */
var Model = {
    
    job: {
        
        /**
         * 
         * @api { DELETE } ^{bk_biz_id}/tasks/bulk/ BulkDestroy
         * @apiName BulkDestroy  
         * @apiGroup job  
         */
        bulkDestroy: RestListAPI("DELETE", "{bk_biz_id}/tasks/bulk/"),
        
        /**
         * 
         * @api { POST } ^{bk_biz_id}/tasks/ Create
         * @apiName Create  
         * @apiGroup job  
         */
        create: RestListAPI("POST", "{bk_biz_id}/tasks/"),
        
        /**
         * 
         * @api { DELETE } ^{bk_biz_id}/tasks/{pk}/ Destroy
         * @apiName Destroy  
         * @apiGroup job  
         */
        destroy: RestDetailAPI("DELETE", "{bk_biz_id}/tasks/{pk}/"),
        
        /**
         * 
         * @api { GET } ^{bk_biz_id}/tasks/ List
         * @apiName List  
         * @apiGroup job  
         */
        list: RestListAPI("GET", "{bk_biz_id}/tasks/"),
        
        /**
         * 
         * @api { PATCH } ^{bk_biz_id}/tasks/{pk}/ PartialUpdate
         * @apiName PartialUpdate  
         * @apiGroup job  
         */
        partialUpdate: RestDetailAPI("PATCH", "{bk_biz_id}/tasks/{pk}/"),
        
        /**
         * 
         * @api { GET } ^{bk_biz_id}/tasks/{pk}/ Retrieve
         * @apiName Retrieve  
         * @apiGroup job  
         */
        retrieve: RestDetailAPI("GET", "{bk_biz_id}/tasks/{pk}/"),
        
        /**
         * 
         * @api { PUT } ^{bk_biz_id}/tasks/{pk}/ Update
         * @apiName Update  
         * @apiGroup job  
         */
        update: RestDetailAPI("PUT", "{bk_biz_id}/tasks/{pk}/"),
        
    },
    
    model: {
        
        /**
         * 
         * @api { POST }  Create
         * @apiName Create  
         * @apiGroup model  
         */
        create: RestListAPI("POST", ""),
        
        /**
         * 
         * @api { DELETE }  Destroy
         * @apiName Destroy  
         * @apiGroup model  
         */
        destroy: RestDetailAPI("DELETE", ""),
        
        /**
         * 
         * @api { GET }  List
         * @apiName List  
         * @apiGroup model  
         */
        list: RestListAPI("GET", ""),
        
        /**
         * 
         * @api { PATCH }  PartialUpdate
         * @apiName PartialUpdate  
         * @apiGroup model  
         */
        partialUpdate: RestDetailAPI("PATCH", ""),
        
        /**
         * 
         * @api { GET }  Retrieve
         * @apiName Retrieve  
         * @apiGroup model  
         */
        retrieve: RestDetailAPI("GET", ""),
        
        /**
         * 
         * @api { PUT }  Update
         * @apiName Update  
         * @apiGroup model  
         */
        update: RestDetailAPI("PUT", ""),
        
    },
    
    cloud: {
        
        /**
         * 
         * @api { POST } ^{bk_biz_id}/clouds/ Create
         * @apiName Create  
         * @apiGroup cloud  
         */
        create: RestListAPI("POST", "{bk_biz_id}/clouds/"),
        
        /**
         * 
         * @api { DELETE } ^{bk_biz_id}/clouds/{pk}/ Destroy
         * @apiName Destroy  
         * @apiGroup cloud  
         */
        destroy: RestDetailAPI("DELETE", "{bk_biz_id}/clouds/{pk}/"),
        
        /**
         * 
         * @api { POST } ^{bk_biz_id}/clouds/{pk}/disvisible/ Disvisible
         * @apiName Disvisible  
         * @apiGroup cloud  
         */
        disvisible: RestDetailAPI("POST", "{bk_biz_id}/clouds/{pk}/disvisible/"),
        
        /**
         * 
         * @api { POST } ^{bk_biz_id}/clouds/{pk}/envisible/ Envisible
         * @apiName Envisible  
         * @apiGroup cloud  
         */
        envisible: RestDetailAPI("POST", "{bk_biz_id}/clouds/{pk}/envisible/"),
        
        /**
         * 
         * @api { GET } ^{bk_biz_id}/clouds/ List
         * @apiName List  
         * @apiGroup cloud  
         */
        list: RestListAPI("GET", "{bk_biz_id}/clouds/"),
        
        /**
         * 
         * @api { PATCH } ^{bk_biz_id}/clouds/{pk}/ PartialUpdate
         * @apiName PartialUpdate  
         * @apiGroup cloud  
         */
        partialUpdate: RestDetailAPI("PATCH", "{bk_biz_id}/clouds/{pk}/"),
        
        /**
         * 
         * @api { POST } ^{bk_biz_id}/clouds/{pk}/rename/ Rename
         * @apiName Rename  
         * @apiGroup cloud  
         */
        rename: RestDetailAPI("POST", "{bk_biz_id}/clouds/{pk}/rename/"),
        
        /**
         * 
         * @api { GET } ^{bk_biz_id}/clouds/{pk}/ Retrieve
         * @apiName Retrieve  
         * @apiGroup cloud  
         */
        retrieve: RestDetailAPI("GET", "{bk_biz_id}/clouds/{pk}/"),
        
        /**
         * 
         * @api { PUT } ^{bk_biz_id}/clouds/{pk}/ Update
         * @apiName Update  
         * @apiGroup cloud  
         */
        update: RestDetailAPI("PUT", "{bk_biz_id}/clouds/{pk}/"),
        
    },
    
    cmdb: {
        
        /**
         * @apiDescription 查询用户有权限的业务列表
         * @api { GET } ^cmdb/applications/ Applications
         * @apiName Applications  
         * @apiGroup cmdb  
         */
        applications: RestListAPI("GET", "cmdb/applications/"),
        
        /**
         * @apiDescription 查询所有云区域信息
         * @api { GET }  GetAllPlat
         * @apiName GetAllPlat  
         * @apiGroup cmdb  
         */
        getAllPlat: RestListAPI("GET", ""),
        
        /**
         * @apiDescription 查询业务下主机列表信息
         * @api { GET } ^cmdb/{bk_biz_id}/get_app_host_list/ GetAppHostList
         * @apiName GetAppHostList  
         * @apiGroup cmdb  
         */
        getAppHostList: RestDetailAPI("GET", "cmdb/{bk_biz_id}/get_app_host_list/"),
        
        /**
         * @apiDescription 查询业务下的大区和模块列表信息
         * @api { GET } ^cmdb/{bk_biz_id}/topo/ Topo
         * @apiName Topo  
         * @apiGroup cmdb  
         */
        topo: RestDetailAPI("GET", "cmdb/{bk_biz_id}/topo/"),
        
    },
    
    hostStatus: {
        
        /**
         * 
         * @api { POST }  Create
         * @apiName Create  
         * @apiGroup hostStatus  
         */
        create: RestListAPI("POST", ""),
        
        /**
         * 
         * @api { DELETE }  Destroy
         * @apiName Destroy  
         * @apiGroup hostStatus  
         */
        destroy: RestDetailAPI("DELETE", ""),
        
        /**
         * 
         * @api { GET }  List
         * @apiName List  
         * @apiGroup hostStatus  
         */
        list: RestListAPI("GET", ""),
        
        /**
         * 
         * @api { PATCH }  PartialUpdate
         * @apiName PartialUpdate  
         * @apiGroup hostStatus  
         */
        partialUpdate: RestDetailAPI("PATCH", ""),
        
        /**
         * 
         * @api { GET }  Retrieve
         * @apiName Retrieve  
         * @apiGroup hostStatus  
         */
        retrieve: RestDetailAPI("GET", ""),
        
        /**
         * 
         * @api { PUT }  Update
         * @apiName Update  
         * @apiGroup hostStatus  
         */
        update: RestDetailAPI("PUT", ""),
        
    },
    
    host: {
        
        /**
         * 
         * @api { POST }  CheckHostsValid
         * @apiName CheckHostsValid  
         * @apiGroup host  
         */
        checkHostsValid: RestListAPI("POST", ""),
        
        /**
         * 
         * @api { POST }  CheckProxyExisted
         * @apiName CheckProxyExisted  
         * @apiGroup host  
         */
        checkProxyExisted: RestListAPI("POST", ""),
        
        /**
         * 
         * @api { POST } ^{bk_biz_id}/hosts/ Create
         * @apiName Create  
         * @apiGroup host  
         */
        create: RestListAPI("POST", "{bk_biz_id}/hosts/"),
        
        /**
         * 
         * @api { DELETE } ^{bk_biz_id}/hosts/{pk}/ Destroy
         * @apiName Destroy  
         * @apiGroup host  
         */
        destroy: RestDetailAPI("DELETE", "{bk_biz_id}/hosts/{pk}/"),
        
        /**
         * 
         * @api { GET } ^{bk_biz_id}/hosts/ List
         * @apiName List  
         * @apiGroup host  
         */
        list: RestListAPI("GET", "{bk_biz_id}/hosts/"),
        
        /**
         * 
         * @api { PATCH } ^{bk_biz_id}/hosts/{pk}/ PartialUpdate
         * @apiName PartialUpdate  
         * @apiGroup host  
         */
        partialUpdate: RestDetailAPI("PATCH", "{bk_biz_id}/hosts/{pk}/"),
        
        /**
         * 
         * @api { GET } ^{bk_biz_id}/hosts/{pk}/ Retrieve
         * @apiName Retrieve  
         * @apiGroup host  
         */
        retrieve: RestDetailAPI("GET", "{bk_biz_id}/hosts/{pk}/"),
        
        /**
         * 
         * @api { PUT } ^{bk_biz_id}/hosts/{pk}/ Update
         * @apiName Update  
         * @apiGroup host  
         */
        update: RestDetailAPI("PUT", "{bk_biz_id}/hosts/{pk}/"),
        
    },
    
    generic: {
        
    },
    
    hostLog: {
        
        /**
         * 
         * @api { POST }  Create
         * @apiName Create  
         * @apiGroup hostLog  
         */
        create: RestListAPI("POST", ""),
        
        /**
         * 
         * @api { DELETE }  Destroy
         * @apiName Destroy  
         * @apiGroup hostLog  
         */
        destroy: RestDetailAPI("DELETE", ""),
        
        /**
         * 
         * @api { GET }  List
         * @apiName List  
         * @apiGroup hostLog  
         */
        list: RestListAPI("GET", ""),
        
        /**
         * 
         * @api { PATCH }  PartialUpdate
         * @apiName PartialUpdate  
         * @apiGroup hostLog  
         */
        partialUpdate: RestDetailAPI("PATCH", ""),
        
        /**
         * 
         * @api { GET }  Retrieve
         * @apiName Retrieve  
         * @apiGroup hostLog  
         */
        retrieve: RestDetailAPI("GET", ""),
        
        /**
         * 
         * @api { PUT }  Update
         * @apiName Update  
         * @apiGroup hostLog  
         */
        update: RestDetailAPI("PUT", ""),
        
    },
    
    test: {
        
        /**
         * @apiDescription celery中应用esbclient测试
         * @api { GET }  TestCeleryEsbClient
         * @apiName TestCeleryEsbClient  
         * @apiGroup test  
         */
        testCeleryEsbClient: RestListAPI("GET", ""),
        
        /**
         * 
         * @api { GET }  TestGetTaskLog
         * @apiName TestGetTaskLog  
         * @apiGroup test  
         */
        testGetTaskLog: RestListAPI("GET", ""),
        
        /**
         * @apiDescription 安装pagent测试
         * @api { GET }  TestInstallPagent
         * @apiName TestInstallPagent  
         * @apiGroup test  
         */
        testInstallPagent: RestListAPI("GET", ""),
        
        /**
         * @apiDescription 安装proxy测试
        http://dev.paas-dev.bking.com:8000/tests/test_install_proxy/?cloud=1&ip=&node_type=PROXY
         * @api { GET }  TestInstallProxy
         * @apiName TestInstallProxy  
         * @apiGroup test  
         */
        testInstallProxy: RestListAPI("GET", ""),
        
        /**
         * @apiDescription 卸载agent测试
         * @api { GET }  TestUninstallAgent
         * @apiName TestUninstallAgent  
         * @apiGroup test  
         */
        testUninstallAgent: RestListAPI("GET", ""),
        
    },
    
    kv: {
        
        /**
         * 
         * @api { POST }  Create
         * @apiName Create  
         * @apiGroup kv  
         */
        create: RestListAPI("POST", ""),
        
        /**
         * 
         * @api { DELETE }  Destroy
         * @apiName Destroy  
         * @apiGroup kv  
         */
        destroy: RestDetailAPI("DELETE", ""),
        
        /**
         * 
         * @api { GET }  List
         * @apiName List  
         * @apiGroup kv  
         */
        list: RestListAPI("GET", ""),
        
        /**
         * 
         * @api { GET }  Nginx
         * @apiName Nginx  
         * @apiGroup kv  
         */
        nginx: RestListAPI("GET", ""),
        
        /**
         * 
         * @api { PATCH }  PartialUpdate
         * @apiName PartialUpdate  
         * @apiGroup kv  
         */
        partialUpdate: RestDetailAPI("PATCH", ""),
        
        /**
         * 
         * @api { GET }  Retrieve
         * @apiName Retrieve  
         * @apiGroup kv  
         */
        retrieve: RestDetailAPI("GET", ""),
        
        /**
         * 
         * @api { PUT }  Update
         * @apiName Update  
         * @apiGroup kv  
         */
        update: RestDetailAPI("PUT", ""),
        
    },
    
}
