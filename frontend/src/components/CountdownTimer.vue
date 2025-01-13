<template>
  <div class="font-mono text-sm text-red-500">
    <div v-if="timeLeft.total > 0" class="flex space-x-2">
      <span class="countdown-digit">{{ timeLeft.days }}d</span>
      <span class="countdown-digit">{{ ('0' + timeLeft.hours).slice(-2) }}h</span>
      <span class="countdown-digit">{{ ('0' + timeLeft.minutes).slice(-2) }}m</span>
      <span class="countdown-digit">{{ ('0' + timeLeft.seconds).slice(-2) }}s</span>
    </div>
    <div v-else class="text-gray-400">Already Left</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue'
import { parseISO } from 'date-fns'
import { zonedTimeToUtc, utcToZonedTime } from 'date-fns-tz'

const props = defineProps({
  date: {
    type: String,
    required: true
  }
})

const userTimezone = inject('userTimezone')
const timeLeft = ref({ days: 0, hours: 0, minutes: 0, seconds: 0, total: 0 })
let timer = null

const getTimeRemaining = (endtime) => {
  try {
    // Get current time in user's timezone
    const timezone = userTimezone?.value || Intl.DateTimeFormat().resolvedOptions().timeZone
    const nowUTC = new Date()
    
    // Parse target date string to UTC first
    const targetDate = parseISO(endtime)
    
    // Convert target date to user's timezone and set to next day midnight
    const targetInUserTZ = utcToZonedTime(targetDate, timezone)
    targetInUserTZ.setHours(0, 0, 0, 0)  // Set to midnight
    
    // Convert back to UTC for consistent calculations
    const targetUTC = zonedTimeToUtc(targetInUserTZ, timezone)
    
    // Calculate total milliseconds remaining
    const total = targetUTC.getTime() - nowUTC.getTime()
    
    // Calculate days first
    const days = Math.max(0, Math.floor(total / (1000 * 60 * 60 * 24)))
    
    // Calculate remaining time after removing full days
    const remainingTime = total - (days * 1000 * 60 * 60 * 24)
    
    // Calculate hours, minutes, seconds from remaining time
    const hours = Math.floor((remainingTime / (1000 * 60 * 60)) % 24)
    const minutes = Math.floor((remainingTime / (1000 * 60)) % 60)
    const seconds = Math.floor((remainingTime / 1000) % 60)

    return {
      total,
      days,
      hours,
      minutes,
      seconds
    }
  } catch (error) {
    console.error('Error in getTimeRemaining:', error)
    return { total: 0, days: 0, hours: 0, minutes: 0, seconds: 0 }
  }
}

const updateClock = () => {
  const t = getTimeRemaining(props.date)
  timeLeft.value = t
  
  if (t.total <= 0) {
    clearInterval(timer)
  }
}

onMounted(() => {
  updateClock() // Run once immediately
  timer = setInterval(updateClock, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>