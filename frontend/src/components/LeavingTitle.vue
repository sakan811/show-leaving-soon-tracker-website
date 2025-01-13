<template>
  <div class="mb-8">
    <h3 class="section-title">{{ formatDate(date) }}</h3>
    <div class="grid-layout">
      <div 
        v-for="title in titles" 
        :key="title" 
        class="card"
      >
        <span class="text-netflix-black mr-4">{{ title }}</span>
        <CountdownTimer :date="getDateFromString(date)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import CountdownTimer from './CountdownTimer.vue'
import { format } from 'date-fns'

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

const getDateFromString = (dateStr) => {
  try {
    // Extract month and day from "Leaving Jan. 31"
    const parts = dateStr.split(' ')
    const monthStr = parts[1].replace('.', '') // Remove period from month abbreviation
    const day = parts[2].padStart(2, '0')
    
    // Map month abbreviation to number
    const months = {
      'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
      'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
      'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    
    const month = months[monthStr]
    if (!month) throw new Error('Invalid month')
    
    // Create ISO date string for 2025
    return `2025-${month}-${day}T00:00:00.000Z`
  } catch (error) {
    console.error('Error parsing date:', error, dateStr)
    return new Date().toISOString()
  }
}

const formatDate = (dateStr) => {
  try {
    const date = new Date(getDateFromString(dateStr))
    return format(date, 'dd MMMM yyyy')
  } catch (error) {
    return dateStr
  }
}
</script> 