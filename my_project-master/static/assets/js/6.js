webpackJsonp([6],{eoEM:function(e,a,n){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var l={render:function(){var e=this,a=e.$createElement,n=e._self._c||a;return n("div",{staticClass:"editChange"},[e._v("\n    任务名称：\n    "),n("el-input",{attrs:{placeholder:"请输入任务名称"},model:{value:e.changeName,callback:function(a){e.changeName=a},expression:"changeName"}}),e._v("\n    所属标段：\n    "),n("el-select",{attrs:{placeholder:"请选择"},model:{value:e.tender,callback:function(a){e.tender=a},expression:"tender"}},e._l(e.options,function(e){return n("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),e._v("\n    变更类型：\n    "),n("el-radio",{attrs:{label:"1"},model:{value:e.changeType,callback:function(a){e.changeType=a},expression:"changeType"}},[e._v("常规变更")]),e._v(" "),n("el-radio",{attrs:{label:"2"},model:{value:e.changeType,callback:function(a){e.changeType=a},expression:"changeType"}},[e._v("自定义变更")]),e._v("\n    系统类型：\n    "),n("el-radio",{attrs:{label:"3"},model:{value:e.systemType,callback:function(a){e.systemType=a},expression:"systemType"}},[e._v("windows")]),e._v(" "),n("el-radio",{attrs:{label:"4"},model:{value:e.systemType,callback:function(a){e.systemType=a},expression:"systemType"}},[e._v("linux")]),e._v(" "),n("div",{attrs:{id:"changeDetail"}},[e._v("\n        变更场景：\n        "),n("el-select",{attrs:{placeholder:"请选择"},model:{value:e.changeScene,callback:function(a){e.changeScene=a},expression:"changeScene"}},e._l(e.options,function(e){return n("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})}))],1)],1)},staticRenderFns:[]};var t=n("VU/8")({name:"editChange",data:function(){return{changeName:"",changeScene:"",changeType:"1",systemType:"2",tender:"",options:[{value:"选项1",label:"标段一--嘉为"},{value:"选项2",label:"标段二--灵通"},{value:"选项3",label:"标段三--康拓扑"}]}}},l,!1,function(e){n("jxpd")},"data-v-c81350f8",null);a.default=t.exports},jxpd:function(e,a){}});
//# sourceMappingURL=6.js.map