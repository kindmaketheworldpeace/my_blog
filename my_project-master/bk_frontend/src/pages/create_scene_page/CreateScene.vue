<template>
    <!--<div style="text-align: center">
        <div style="margin-bottom: 20px">
            <span>场景名称：</span>
            <el-input
                    style="width: 50%"
                    placeholder="请输入内容"
                    v-model="item.name"
                    clearable>
            </el-input>
        </div>
        <div style="margin-bottom: 20px">
            <span>所属标段：</span>
            <el-select style="width: 50%" v-model="item.service_privider" placeholder="请选择">
                <el-option
                        v-for="item in options"
                        :key="item.id"
                        :label="item.description"
                        :value="item.id">
                </el-option>
            </el-select>
        </div>
        <div style="margin-top: 20px">
            系统类型：
            <el-radio style="width: 23.5%" v-model="item.os_type" label="1">linux</el-radio>
            <el-radio style="width: 23.5%" v-model="item.os_type" label="2">windows</el-radio>
        </div>
        <div style="margin-top: 20px;">
            变更脚本：
            <el-radio style="width: 7%" v-model="item.script_type" label="1">shell</el-radio>
            <el-radio style="width: 7%" v-model="item.script_type" label="2">bat</el-radio>
            <el-radio style="width: 7%" v-model="item.script_type" label="2">perl</el-radio>
            <el-radio style="width: 7%" v-model="item.script_type" label="2">python</el-radio>
            <el-radio style="width: 7%" v-model="item.script_type" label="2">powershell</el-radio>
            <div style="margin-left: 30%;margin-right: 30%;text-align: left">
            <textarea ref="mycode" class="codesql" v-model="item.script_content"
                      style="height:200px;"></textarea>
            </div>
        </div>
        <div style="margin-top: 20px;">
            <div style="width: 100%" v-for="input in item.input_display_list" :key='input.displayname'>
                输入参数：
                <div class="block">
                    <el-form style="display: inline-block;vertical-align: middle" :inline="true" :model="input"
                             class="demo-form-inline">
                        <el-form-item label="显示名称">
                            <el-input style="width: 60%" v-model="input.displayname" placeholder="请输入显示名称"></el-input>
                        </el-form-item>
                        <el-form-item label="字符类型">
                            <el-select style="width: 60%" v-model="input.type" placeholder="请选择字符类型">
                                <el-option label="字符串" value="char"></el-option>
                                <el-option label="整型" value="int"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item style="width: 5%">
                            <el-checkbox v-model="input.checked">是否必填</el-checkbox>
                        </el-form-item>
                        <el-form-item style="width: 5%">
                            <el-button type="success" icon="el-icon-plus" @click="add_par()" circle></el-button>
                        </el-form-item>
                        <el-form-item style="width: 5%">
                            <el-button type="danger" icon="el-icon-minus" @click="del_par(input.id)" circle></el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </div>
        <div style="margin-bottom: 20px;">
            是否启用：
            <el-radio style="width: 23.5%" v-model="item.is_use" label="1">是</el-radio>
            <el-radio style="width: 23.5%" v-model="item.is_use" label="0">否</el-radio>
        </div>
    </div>-->
    <div style="margin-left: 10%;margin-right: 10%;margin-top: 1%">
        <el-form ref="form" :model="item" label-width="80px">
            <el-form-item label="场景名称">
                <el-input v-model="item.name"></el-input>
            </el-form-item>
            <el-form-item label="可见范围">
                <el-radio-group v-model="item.display_type">
                    <el-radio @change="change_show()" label="OPEN">公开</el-radio>
                    <el-radio @change="change_show()" label="CMDB">标段内</el-radio>
                </el-radio-group>
                <el-select v-show="show_service_privider" v-model="item.display_role" placeholder="请选择标段">
                    <el-option
                            v-for="(item,index) in options"
                            :key="index"
                            :label="item.description"
                            :value="item.name">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="系统类型">
                <el-radio-group v-model="item.os_type">
                    <el-radio label="LINUX">linux</el-radio>
                    <el-radio label="WINDOWS">windows</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="变更脚本">
                <div class="job_content">
                    <el-radio-group v-model="item.script_type">
                        <el-radio label="1">shell</el-radio>
                        <el-radio label="2">bat</el-radio>
                        <el-radio label="3">perl</el-radio>
                        <el-radio label="4">python</el-radio>
                        <el-radio label="5">powershell</el-radio>
                    </el-radio-group>
                    <textarea ref="mycode" class="codesql" :value="item.script_type"
                              style="height:200px;"></textarea>
                </div>
            </el-form-item>
            <el-form-item label="输入参数">
                <div style="width: 100%" v-for="input in item.input_display_list" :key='input.displayname'>
                    <el-form style="display: inline-block;vertical-align: middle" :inline="true" :model="input"
                             class="demo-form-inline">
                        <el-form-item label="显示名称">
                            <el-input v-model="input.displayname" placeholder="请输入显示名称"></el-input>
                        </el-form-item>
                        <el-form-item label="字符类型">
                            <el-select v-model="input.type" placeholder="请选择字符类型">
                                <el-option label="字符串" value="char"></el-option>
                                <el-option label="整型" value="int"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-checkbox v-model="input.checked">是否必填</el-checkbox>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="success" icon="el-icon-plus" @click="add_par()" circle></el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="danger" icon="el-icon-minus" @click="del_par(input.id)" circle></el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </el-form-item>
            <el-form-item label="是否启用">
                <el-radio-group v-model="item.is_use">
                    <el-radio label="1">是</el-radio>
                    <el-radio label="0">否</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="on_submit">立即创建</el-button>
                <el-button>取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script>
    import 'codemirror/theme/dracula.css';
    import 'codemirror/lib/codemirror.css';
    import 'codemirror/theme/blackboard.css';
    import 'codemirror/theme/solarized.css';
    import 'codemirror/addon/hint/show-hint.css';

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
        data() {
            return {
                code: '',
                item: {
                    name: '',
                    display_role: '',
                    display_type: 'OPEN',
                    os_type: 'LINUX',
                    script_type: '1',
                    script_content: '',
                    input_display_list: [{id: 1, displayname: '', type: '', checked: ''}],
                    is_use: '1',
                },
                script_content: 'echo test',
                cur_id: 1,
                options: [],
                show_service_privider: false
            }
        },
        created() {
            this.get_service_privider()
        },
        methods: {
            on_submit() {
                this.create_scene()
            },
            create_scene() {
                let params = {}
                params = {
                    name: this.item.name,
                    display_role: this.item.display_role,
                    display_type: this.item.display_type,
                    os_type: this.item.os_type,
                    script_type: this.item.script_type,
                    script_content: this.code.getValue(),
                    input_display_list: this.item.input_display_list,
                    is_use: this.item.is_use,
                }
                params.account = params.os_type == 'LINUX' ? 'root' : 'system'
                params.input_display_list = JSON.stringify(params.input_display_list)
                this.$store.dispatch('scene/createScene', params).then(res => {
                    console.log()
                })
            },
            get_service_privider() {
                let params = {}
                this.$store.dispatch('serviceprivider/getServicePrivider', params).then(res => {
                        for (let i = 0; i < res.data.items.length; i++) {
                            res.data.items[i].description = res.data.items[i].description + '(' + res.data.items[i].name + ')'
                        }
                        this.options = res.data.items
                    }
                )
            },
            add_par() {
                this.cur_id += 1
                this.item.input_display_list.push({id: this.cur_id, displayname: '', type: '', checked: ''})
            },
            del_par(id) {
                if (id == 1) {
                } else {
                    this.item.input_display_list.splice(-1, 1)
                }
            },
            change_show() {
                this.show_service_privider = !this.show_service_privider
                console.log('sss')
            }
        },
        mounted() {
            let mime = 'text/x-sh'
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
            })
            this.code.on('cursorActivity', function () {
                this.code.showHint()
            })
        }
    }
</script>
<style lang='scss'>
    .job_content {
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
    }

    .block {
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
        display: inline-block;
        vertical-align: middle;
    }

    .new {
        height: 100%;
        padding: 15px 20px 0 20px;
        background: #fff;
        #self_chart {
            width: 500px;
            height: 500px;
        }
    }
</style>
