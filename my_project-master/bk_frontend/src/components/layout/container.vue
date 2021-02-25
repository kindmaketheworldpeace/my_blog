<template>
    <div class="container" :style="isCollapse ? 'width: calc(100% - 50px)' : 'width: calc(100% - 230px)'">
        <breadcrumb :to="$route.meta.bread"></breadcrumb>
        <div class="container-content">
            <router-view/>
        </div>
        <app-footer></app-footer>
    </div>
</template>

<script>
    import Breadcrumb from '@/components/Breadcrumb'
    import Footer from '@/components/layout/Footer'
    import { mapGetters } from 'vuex'

    export default {
        name: 'container',
        mounted() {
        },
        components: {
            'app-footer': Footer,
            'breadcrumb': Breadcrumb
        },
        computed: {
            ...mapGetters('main', ['isCollapse'])
        },
    }
</script>
