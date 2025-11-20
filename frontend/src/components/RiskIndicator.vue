<template>
  <div class="risk">风险指示器：<strong>{{ level }}</strong></div>
</template>
<script setup>
const props = defineProps({ level: { type: String, default: '🟢 低风险' } })
</script>
<style scoped>
.risk{padding:10px;border:1px solid #eee}
</style>
