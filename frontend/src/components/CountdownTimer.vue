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
    const timezone = userTimezone?.value || Intl.DateTimeFormat().resolvedOptions().timeZone
    const now = new Date()
    
    // Parse target date and create Date object
    const targetDate = parseISO(endtime)
    
    // Create formatter for target timezone
    const formatter = new Intl.DateTimeFormat('en-US', {
      timeZone: timezone,
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    })

    // Format target date in user's timezone
    const parts = formatter.formatToParts(targetDate)
    const dateObj = {}
    parts.forEach(part => {
      if (part.type !== 'literal') {
        dateObj[part.type] = part.value
      }
    })

    // Create new date at midnight in user's timezone
    const targetInTZ = new Date(
      `${dateObj.year}-${dateObj.month}-${dateObj.day}T00:00:00.000${getTimezoneOffset(timezone)}`
    )
    
    // Calculate total milliseconds remaining
    const total = targetInTZ.getTime() - now.getTime()
    
    // Calculate time components
    const days = Math.max(0, Math.floor(total / (1000 * 60 * 60 * 24)))
    const remainingTime = total - (days * 1000 * 60 * 60 * 24)
    const hours = Math.floor((remainingTime / (1000 * 60 * 60)) % 24)
    const minutes = Math.floor((remainingTime / (1000 * 60)) % 60)
    const seconds = Math.floor((remainingTime / 1000) % 60)

    return { total, days, hours, minutes, seconds }
  } catch (error) {
    console.error('Error in getTimeRemaining:', error)
    return { total: 0, days: 0, hours: 0, minutes: 0, seconds: 0 }
  }
}

const getTimezoneOffset = (timezone) => {
  const date = new Date()
  const utcDate = new Date(date.toLocaleString('en-US', { timeZone: 'UTC' }))
  const tzDate = new Date(date.toLocaleString('en-US', { timeZone: timezone }))
  const offset = (tzDate - utcDate) / 60000
  const hours = Math.floor(Math.abs(offset) / 60)
  const minutes = Math.abs(offset) % 60
  return `${offset >= 0 ? '+' : '-'}${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
}

const updateClock = () => {
  const t = getTimeRemaining(props.date)
  timeLeft.value = t
  
  if (t.total <= 0) {
    clearInterval(timer)
  }
}

onMounted(() => {
  updateClock()
  timer = setInterval(updateClock, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>