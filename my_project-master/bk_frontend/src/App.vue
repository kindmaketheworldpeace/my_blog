<template>
    <div class="app">
        <bk-header></bk-header>
        <div class="app-content">
            <left-menu></left-menu>
            <container></container>
        </div>
    </div>
</template>

<script>
    import header from '@/components/layout/header'
    import leftMenu from '@/components/layout/leftMenu'
    import container from '@/components/layout/container'

    export default {
        name: 'App',
        components: {
            'bk-header': header,
            'left-menu': leftMenu,
            'container': container
        },
    }
</script>
<style lang="scss">
.app {
    // overflow: hidden;
    // .flex_content {
    //     height: 100%;
    //     display: flex;
    //     #main-container {
    //         flex-grow: 1;
    //     }
    // }
}
</style>
