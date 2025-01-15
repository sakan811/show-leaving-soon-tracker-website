<template>
  <div v-if="hasUpcomingTitles" class="mb-8">
    <h3 class="section-title">{{ formatDate(date) }}</h3>
    <div class="grid-layout">
      <div 
        v-for="title in uniqueTitles" 
        :key="`${title}-${date}`"
        class="card"
      >
        <span class="text-netflix-black mr-4">{{ title }}</span>
        <CountdownTimer :date="date" />
      </div>
    </div>
  </div>
</template>

<script setup>
import CountdownTimer from './CountdownTimer.vue'
import { format } from 'date-fns'
import { computed } from 'vue'

const props = defineProps({
  date: {
    type: String,
    required: true
  },
  titles: {
    type: Array,
    required: true
  }
})

const formatDate = (dateStr) => {
  try {
    const date = new Date(dateStr)
    return format(date, 'dd MMMM yyyy')
  } catch (error) {
    return dateStr
  }
}

const hasUpcomingTitles = computed(() => {
  const targetDate = new Date(props.date)
  return targetDate > new Date()
})

// Computed property to filter out duplicate titles
const uniqueTitles = computed(() => {
  return [...new Set(props.titles)]
})
</script> 