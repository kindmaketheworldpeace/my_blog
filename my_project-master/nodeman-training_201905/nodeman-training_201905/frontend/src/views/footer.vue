<template>
    <div class="agent-footer">
        <div class="bk-foot-info">
            <p>
                {{$t('m.footerInfo.consult')}} (800802001) | <a href="http://bbs.bk.tencent.com/forum.php">{{$t('m.footerInfo.bbs')}}</a> | <a href="http://bk.tencent.com/">{{$t('m.footerInfo.website')}}</a> | <a href="/">{{$t('m.footerInfo.web')}}</a>
            </p>
            <p>
                Copyright © 2012-2019 Tencent BlueKing All Rights Reserved
            </p>
        </div>
    </div>
</template>

<script>

export default {
    data () {
        return {
            hrefInfo: ''
        }
    },
    methods: {
        gethref () {
            this.hrefInfo = window.hostname + '/console'
        }
    },
    mounted () {
        this.gethref()
    }
}
</script>

<style lang="scss" scoped>
    .agent-footer {
        font-size: 20px;
        background: #313b4c;
        position: fixed;
        bottom: 0;
        left: 0;
        z-index: 10;
        width: 100%;
        padding: 10px 0;
        
    }

    .bk-foot-info {
        text-align: center;
        color: #fff;
        line-height: 20px;
        font-size: 14px;
        a {
            color: #fff!important;
        }
    }
</style>




