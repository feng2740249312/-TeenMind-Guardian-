<template>
  <div ref="root" class="chart">情绪趋势图占位</div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const root = ref(null)
onMounted(()=>{/* 可集成 echarts */})
</script>
<style scoped>
.chart{height:300px;border:1px dashed #ddd;display:flex;align-items:center;justify-content:center}
</style>
