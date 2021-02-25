<template>
	<div class="agent-node">
		<app-exception :type="'building'"></app-exception>
	</div>
</template>

<script>
    export default {
        data () {
            return {}
        },
        computed: {
            testStore () {
                return this.$store.state.health.test
            }
        }
    }
</script>
<style lang="scss" scoped>
    .agent-node {
        height: 500px;
    }
</style>