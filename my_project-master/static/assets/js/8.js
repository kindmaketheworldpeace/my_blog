webpackJsonp([8],{RLKS:function(e,t){},yVmr:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n={name:"selfChange",data:function(){return{changeName:"",tender:"",serverList:[{value:"选项1",label:"标段一（嘉为）"},{value:"选项2",label:"标段二（灵通）"},{value:"选项3",label:"标段三（康拓扑）"}]}},created:function(){this.inntCharts()},methods:{inntCharts:function(){this.$echarts.init(document.getElementById("self_chart")).setOption({title:{text:"ECharts 入门示例"},tooltip:{},legend:{data:["销量"]},xAxis:{data:["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]},yAxis:{},series:[{name:"销量",type:"bar",data:[5,20,36,10,10,20]}]})}}},l={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"selfChange"},[a("div",[a("span",[e._v("任务名称:")]),a("el-input",{staticStyle:{"margin-left":"5px",width:"180px"},attrs:{placeholder:"请输入内容"},model:{value:e.changeName,callback:function(t){e.changeName=t},expression:"changeName"}})],1),e._v(" "),a("div",{staticStyle:{"margin-top":"10px"}},[a("span",[e._v("所属标段")]),e._v(" "),a("el-select",{staticStyle:{"margin-left":"5px"},attrs:{placeholder:"请选择服务商"},model:{value:e.tender,callback:function(t){e.tender=t},expression:"tender"}},e._l(e.serverList,function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})}))],1)])},staticRenderFns:[]};var r=a("VU/8")(n,l,!1,function(e){a("RLKS")},null,null);t.default=r.exports}});
//# sourceMappingURL=8.js.map