webpackJsonp([9],{G4Hy:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});n("rgp1");var a=n("cMGX"),i=n("l0np"),l={components:{pagination:a.a,"new-edit":i.a},data:function(){return{totalNumber:0,currentPage:1,pageSize:10,tableData:[],activeIndex:"1",test:[{id:1,text:"标段一"},{id:2,text:"标段二"}]}},created:function(){this.get_service_privider(),this.get_rule()},methods:{get_service_privider:function(){var e=this;this.$store.dispatch("serviceprivider/getServicePrivider",{}).then(function(t){e.tableData=t.data.items})},pageSizeChange:function(e){this.currentPage=e.currentPage,this.pageSize=e.pageSize,this.get_rule({page:this.currentPage,page_size:this.pageSize})},create:function(){this.$router.replace("/create_rule")},get_rule:function(e){},detail_rule:function(){},modify_rule:function(e){},delete_rule:function(e){},get_rule_by_name:function(){},select_scene:function(){}}},r={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("el-menu",{staticClass:"el-menu-demo",attrs:{"default-active":e.activeIndex,mode:"horizontal"},on:{select:e.select_scene}},e._l(e.test,function(t){return n("el-menu-item",{key:t.id,attrs:{index:"2"}},[e._v(e._s(t.text))])})),e._v(" "),n("el-button",{attrs:{type:"text"},on:{click:function(t){e.create()}}},[e._v("新建规则")]),e._v(" "),n("el-button",{attrs:{type:"text"}},[e._v("优先级排序")]),e._v(" "),n("el-divider"),e._v(" "),n("div",{staticClass:"table"},[n("el-table",{staticStyle:{width:"100%"},attrs:{data:e.tableData,height:"100%",border:""}},[n("el-table-column",{attrs:{fixed:"",prop:"id",label:"编号",width:"150"}}),e._v(" "),n("el-table-column",{attrs:{prop:"name",label:"场景名称"}}),e._v(" "),n("el-table-column",{attrs:{prop:"os_type",label:"系统类型",width:"120"}}),e._v(" "),n("el-table-column",{attrs:{prop:"create_at",label:"创建时间",width:"300"}}),e._v(" "),n("el-table-column",{attrs:{fixed:"right",label:"操作",width:"100"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("el-button",{attrs:{type:"text",size:"small"},on:{click:function(n){e.detail_scene(t.row)}}},[e._v("详情")]),e._v(" "),n("el-button",{attrs:{type:"text",size:"small"},on:{click:function(n){e.modify_scene(t.row)}}},[e._v("编辑")]),e._v(" "),n("el-button",{attrs:{type:"text",size:"small"},on:{click:function(n){e.delete_scene(t.row)}}},[e._v("删除")])]}}])})],1)],1),e._v(" "),n("pagination",{attrs:{total:e.totalNumber},on:{"page-size-change":e.pageSizeChange}})],1)},staticRenderFns:[]};var c=n("VU/8")(l,r,!1,function(e){n("yf2G")},null,null);t.default=c.exports},yf2G:function(e,t){}});
//# sourceMappingURL=9.js.map