<template>
    <div :class="['bk-tab2', {'bk-tab2-small': size === 'small'}]">
        <div :class="['bk-tab2-head',{'is-fill': type === 'fill'}]">
            <div class="bk-tab-flo bk-ul-tab">
                <ul class="bk-tab2-nav" id="bk-tab2">
                    <li class="tab2-nav-item"
                        v-for="(item, index) in navList"
                        v-show="item.show"
                        :class="{'active': calcActiveName === item.name, 'bk-act-border': calcActiveName === item.name}"
                        @click="toggleTab(index)">
                        {{ item.title }} <span style="color: #dce3ea" v-show="item.id">[{{item.id}}]</span>
                        <span class="bk-li-active" v-if="calcActiveName === item.name"></span>
                    </li>
                </ul>
            </div>
            <div class="bk-tab-flo bk-tab-icon" id="bk-tab-icon">
                <div class="bk-tab2-over" v-show="showIcon">
                    <span>
                        <i class="bk-icon icon-angle-down" v-show="!showOver || !indexNum" @click="showClick"></i>
                        <i class="bk-icon icon-angle-up" style="color: #3c96ff" v-show="showOver && indexNum" @click="showOpen"></i>
                    </span>
                    <div class="bk-over-list" v-show="showOver && indexNum" :class="{'bk-border': calcActiveName === cla}">
                        <div @click="overToggleTab(addList.indexStatus)" class="bk-add-cloud">
                            <span>
                                <i class="bk-icon icon-plus"></i>{{$t('m.tabControl.cloudManag')}}
                            </span>
                        </div>
                        <div class="bk-ul-list">
                            <ul>
                                <li v-for="(item, index) in overList"
                                    v-show="item.show"
                                    :class="{'agentClick': calcActiveName === item.name}"
                                    @click="overToggleTab(index)">
                                    {{ item.title }}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bk-tab2-action" v-if="hasSetting">
                <div class="action-wrapper">
                    <slot name="setting"></slot>
                </div>
            </div>
        </div>
        <div class="bk-tab2-content">
            <slot></slot>
        </div>
    </div>
</template>
<script>
    export default {
        name: 'bk-tab',
        props: {
            activeName: {
                type: String,
                default: ''
            },
            type: {
                type: String,
                default: ''
            },
            size: {
                type: String,
                default: ''
            }
        },
        watch: {
            activeName (val) {
                this.calcActiveName = val
            }
        },
        mounted () {
            if (!this.activeName) {
                this.calcActiveName = this.navList[0].name
            }
            window.setTime = setInterval(() => {
                this.testNav()
            }, 1000)
        },
        data () {
            return {
                navList: [],
                overList: [],
                addList: {},
                indexNum: 0,
                showIcon: true,
                calcActiveName: this.activeName,
                hasSetting: this.$slots.setting,
                showOver: false,
                shareing: false,
                cla: '',
                listNum: 2
            }
        },
        methods: {
            /**
             *  切换tab
             */
            testNav () {
                let bkUl = document.getElementById('bk-tab2')
                if (!bkUl) {
                    return
                }
                let ulOffsetWidth = bkUl.offsetWidth
                let liWidth = 0
                let t = Math.floor(ulOffsetWidth / 120)
                let sum = 0
                for (let i = 0; i < this.navList.length; i++) {
                    if (this.navList[i].show) {
                        sum += 1
                    }
                }
                if (t >= sum) {
                    this.showIcon = false
                } else {
                    this.showIcon = true
                }
            },
            toggleTab (index) {
                this.calcActiveName = this.navList[index].name
                this.$emit('tab-changed', this.calcActiveName, index)
            },
            overToggleTab (index) {
                let num = index + this.indexNum

                if (index === this.addList.indexStatus) {
                    this.calcActiveName = this.navList[num].name
                    this.$emit('tab-changed', this.calcActiveName, num)
                    this.showOver = false
                } else {
                    let obj = this.navList[num]
                    this.navList.splice(num, 1)
                    this.navList.splice(this.listNum, 0, obj)

                    this.calcActiveName = this.navList[this.listNum].name
                    this.$emit('tab-changed', this.calcActiveName, this.listNum)
                    this.showOver = false
                }
            },
            addNavItem (item) {
                for (let i = this.navList.length - 1; i >= 0; i--) {
                    if (item.title === this.navList[i].title) {
                        return this.navList.length - 1
                    }
                }
                this.navList.push(item)
                return this.navList.length - 1
            },
            addNewItem (item) {
                let newName = 'cloudName' + (this.navList.length + 1)
                for (let i = this.navList.length - 1; i >= 0; i--) {
                    if (item.bk_cloud_name === this.navList[i].title) {
                        this.navList[i].id = item.bk_cloud_id
                        let obj = this.navList[i]
                        this.navList.splice(this.listNum, 0, obj)
                        break
                    } else if (i === 0) {
                        let obj = {
                            name: newName,
                            show: true,
                            title: item.bk_cloud_name,
                            id: item.bk_cloud_id
                        }
                        this.navList.splice(this.listNum, 0, obj)
                    }
                }
                this.showOver = false
                this.calcActiveName = this.navList[this.listNum].name
                this.$emit('tab-changed', this.calcActiveName, this.listNum)
            },
            deleteItems (item) {
                for (let i = this.navList.length - 1; i >= 0; i--) {
                    if (item.bk_cloud_name === this.navList[i].title) {
                        this.navList[i].show = !this.navList[i].show
                        break
                    }
                }
            },
            closeItems (item) {
                for (let i = this.navList.length - 1; i >= 0; i--) {
                    if (item.bk_cloud_name === this.navList[i].title) {
                        this.navList.splice(i, 1)
                        break
                    }
                }
            },
            changeItems (item) {
                for (let i = this.navList.length - 1; i >= 0; i--) {
                    if (item.name === this.navList[i].name) {
                        this.navList[i].title = item.bk_cloud_name
                        break
                    }
                }
            },
            showOpen () {
                this.showOver = !this.showOver
            },
            closeOpen () {
                this.showOver = false
            },
            showClick () {
                this.indexNum = 0
                this.cla = this.navList[this.navList.length - 1].name
                this.addList = this.navList[this.navList.length - 1]
                this.showOver = true
                let bkUl = document.getElementById('bk-tab2')
                let ulOffsetWidth = bkUl.offsetWidth
                let liWidth = 0
                this.overList = []
                for (let i = 0; i < bkUl.childNodes.length; i++) {
                    liWidth += bkUl.childNodes[i].offsetWidth
                    if (liWidth > ulOffsetWidth) {
                        this.indexNum = i
                        for (let j = i; j < this.navList.length; j++) {
                            this.overList.push(this.navList[j])
                        }
                        this.addList.indexStatus = this.overList.length - 1
                        if (this.overList[this.overList.length - 1].title === this.$t('m.tabControl.cloudManag')) {
                            this.overList.splice(this.overList.length - 1, 1)
                        }
                        return
                    }
                }
            },
            /**
             *  子组件更新时调用
             *  @param index - 子组件的索引值
             *  @param data - 更新的内容
             */
            updateList (index, data) {
                // let list = this.navList
                // let item = list[index]

                // for (let key in item) {
                //     item[key] = data[key]
                // }
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import '../../scss/mixins/scroller.scss';
    .bk-tab2-nav {
        overflow: hidden;
        width: 100%;
        height: 45px;
        > li {
            height: 45px!important;
            width: 120px;
            padding: 0 10px!important;
            text-align: center;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
    }
    .active {
        border-bottom: none;
    }
    .bk-tab2-over {
        position: absolute;
        top: 0;
        right: 0;
        width: 30px;
        height: 44px;
        background-color: #fff;
        line-height: 44px;
        text-align: center;
        cursor: pointer;
        z-index: 20;
        > span {
            > i {
                color: #e1e6eb;
            }
        }
        .bk-over-list {
            position: absolute;
            top: 44px;
            right: 0px;
            width: 250px;
            height: 210px;
            background-color: #fff;
            border: 1px solid #dde4eb;
            .bk-ul-list {
                overflow: auto;
                @include scroller;
                width: 250px;
                height: 160px;
                padding: 10px 0px;
                border-right: 2px solid #dde4eb;
                ul {
                    width: 100%;
                    li {
                        line-height: 40px;
                        padding: 0 15px;
                        text-align: left;
                        font-size: 12px;
                        color: #737987;
                        &.agentClick {
                            background-color: #ebf4ff;
                            color: #3c96ff;
                        }
                    }
                }
            }
            .bk-add-cloud {
                width: 245px;
                position: absolute;
                bottom: 0;
                left: 0;
                height: 40px;
                line-height: 40px;
                z-index: 5;
                background-color: #fff;
                font-size: 12px;
                text-align: left;
                color: #737987;
                padding: 0 15px;
                border-top: 1px solid #dde4eb;
            }
            &.bk-border {
                border-right: 1px solid #dde4eb;
            }
        }
    }
    .bk-tab2 .bk-tab2-head.is-fill .bk-tab2-nav>li {
        border: none;
    }
    .bk-act-border {
        border-bottom: 1px solid #3c96ff!important;
    }
    .bk-mar60 {
        margin-right: 60px;
    }
    .bk-tab-flo {
        float: left;
        position: relative;
    }
    .bk-ul-tab {
        width: 95%;
    }
    .bk-tab-icon {
        width: 5%;
    }
    .bk-tab2-head {
        border: none;
    }
    .bk-tab2 .bk-tab2-head {
        background-color: #fff;
    }
</style>
