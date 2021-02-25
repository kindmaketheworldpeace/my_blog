<template>
    <div class="editChange">
        <div style="margin-left: 20px;margin-top: 10px;">
          <span>任务名称:</span><el-input v-model="changeName" placeholder="请输入任务名称" style="display: inline-block;width: 150px;margin-left: 15px"></el-input>
        </div>
      <div style="margin-left: 20px;margin-top: 10px;">
        <span>所属标段:</span>
        <el-select v-model="tender" placeholder="请选择">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
      </el-select>
      </div>
      <div style="margin-left: 20px;margin-top: 10px;">
        <span>变更类型:</span>
        <el-radio v-model="changeType" label="1">常规变更</el-radio>
        <el-radio v-model="changeType" label="2">自定义变更</el-radio>
      </div>
        <div v-if="changeType==1">
            <div style="margin-left: 20px;margin-top: 10px;">
        <span>系统类型:</span>
        <el-radio v-model="systemType" label="3">windows</el-radio>
        <el-radio v-model="systemType" label="4">linux</el-radio>
      </div>

        <div id="changeDetail">
          <div style="margin-left: 20px;margin-top: 10px;">
            <span>变更场景:</span>
            <el-select v-model="changeScene" placeholder="请选择">
    <el-option
      v-for="item in sceneoptions"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
      </el-select>
          </div>
        </div>
        </div>
        <div v-if="changeType==2">
            <el-form ref="form" :model="item" label-width="80px">
                <el-form-item label="变更脚本">
                <div class="job_content">
                    <el-radio-group v-model="item.script_type">
                        <el-radio label="1">shell</el-radio>
                        <el-radio label="2">bat</el-radio>
                        <el-radio label="3">perl</el-radio>
                        <el-radio label="4">python</el-radio>
                        <el-radio label="5">powershell</el-radio>
                    </el-radio-group>
                </div>
                    <div><textarea ref="mycode" class="codesql" :value="item.script_type"
                              style="height:200px;"></textarea></div>
            </el-form-item>
            </el-form>
        </div>
      <div style="margin-left: 20px;margin-top: 10px;">
        <span>变更对象:</span> <el-button type="primary" style="margin-left: 15px" @click="choose_server">选择服务器</el-button>
      </div>
      <NewEdit ref="newEdit" title="选择服务器" @handle-success="handlesuccess" width="width">
          <div slot="dialog-content">
              <div style="margin-top: 8px">
              <el-radio v-model="serverSource" label="1">通过IP选择服务器</el-radio>
                <el-radio v-model="serverSource" label="2">配置平台</el-radio>
              </div>
              <el-divider></el-divider>
              <el-input v-model="searchserver" placeholder="请输入IP,多个请用空格隔开" style="width: 40%"></el-input>
              <el-checkbox v-model="is_accurate" style="margin-left: 10px">精确匹配</el-checkbox>
              <el-button type="primary" style="float: right">立即查找</el-button>
              <el-table ref="multipleTable" :data="tableData" tooltip-effect="dark" style="width: 100%" @selection-change="handleSelectionChange">
                <el-table-column
                  type="selection"
                  width="55">
                </el-table-column>
                <el-table-column
                  prop="region"
                  label="区域名称"
                  width="77">
                </el-table-column>
                <el-table-column
                  prop="ipaddr"
                  label="IP地址"
                  show-overflow-tooltip>
                </el-table-column>
                  <el-table-column
                  prop="os"
                  label="操作系统"
                  show-overflow-tooltip>
                </el-table-column>
              </el-table>
          </div>
      </NewEdit>
        <div style="margin-left: 20px;margin-top: 10px;">
            <el-button type="primary">保存</el-button>
            <el-button type="primary">发起变更</el-button>
            <el-button type="primary">取消</el-button>
        </div>
    </div>
</template>

<script>
    import 'codemirror/theme/dracula.css';
    import 'codemirror/lib/codemirror.css';
    import 'codemirror/theme/blackboard.css';
    import 'codemirror/theme/solarized.css';
    import 'codemirror/addon/hint/show-hint.css';
    import NewEdit from '@/components/NewEdit'

    let CodeMirror = require('codemirror/lib/codemirror');
    require('codemirror/addon/edit/matchbrackets');
    require('codemirror/addon/selection/active-line');
    require('codemirror/mode/sql/sql');
    require('codemirror/mode/shell/shell');
    require('codemirror/mode/python/python');
    require('codemirror/mode/perl/perl');
    require('codemirror/mode/powershell/powershell');
    require('codemirror/addon/hint/show-hint');
    require('codemirror/addon/hint/sql-hint');

    export default {
        name: 'editChange',
        components: {
            'NewEdit': NewEdit
        },
        data() {
            return {
                item: {
                    script_type: '',
                    script_content: ''
                },
                tableData: [{
                    region: '深圳',
                    ipaddr: '10.5.172.220',
                    os: 'linux'
                }],
                is_accurate: false,
                searchserver: '',
                width: '30%',
                serverSource: '',
                changeName: '',
                changeScene: '',
                changeType: '1',
                systemType: '2',
                tender: '',
                options: [{
                    value: '选项1',
                    label: '标段一--嘉为'
                }, {
                    value: '选项2',
                    label: '标段二--灵通'
                }, {
                    value: '选项3',
                    label: '标段三--康拓扑'
                }],
                sceneoptions: [{
                    value: '选项1',
                    label: '关机'
                }, {
                    value: '选项2',
                    label: '重启'
                }, {
                    value: '选项3',
                    label: '密码修改'
                }, {
                    value: '选项4',
                    label: '账号创建'
                }],
            }
        },
        methods: {
          choose_server() {
              this.$refs['newEdit'].open();
              console.log('111')
          },
          handlesuccess() {
              console.log('222');
        }
        },
        mounted() {
            let mime = 'text/x-sh';
            this.code = CodeMirror.fromTextArea(this.$refs.mycode, {
                theme: 'blackboard',
                mode: mime, //选择对应代码编辑器的语言，我这边选的是数据库，根据个人情况自行设置即可
                indentWithTabs: true,
                smartIndent: true,
                lineNumbers: true,
                matchBrackets: true,
                //theme: theme,
                // autofocus: true,
                extraKeys: {'Ctrl': 'autocomplete'}, //自定义快捷键
                hintOptions: { //自定义提示选项
                    tables: {
                        users: ['name', 'score', 'birthDate'],
                        countries: ['name', 'population', 'size']
                    }
                }
            });
            this.code.on('cursorActivity', function () {
                this.code.showHint()
            })
        }
    }
</script>

<style scoped>
 #changeDetail{
     border: 2px solid white;
     width: 400px;
     height: 200px;
     background-color: #ADB5BD;
     margin-left: 20px;
     margin-top: 10px;
 }
 .editChange{
    position:absolute;
    left:20%;
    top:10%;
 }
</style>
