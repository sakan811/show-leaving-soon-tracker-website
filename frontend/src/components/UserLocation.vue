<template>
  <div class="card mb-8">
    <div class="location-container">
      <div class="location-item">
        <svg class="location-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
        </svg>
        <span class="location-text">{{ location || 'Loading location...' }}</span>
      </div>
      <div class="location-item">
        <svg class="location-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span class="location-text">{{ userTimezone }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  userTimezone: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:userTimezone'])
const location = ref('')

onMounted(async () => {
  try {
    const response = await fetch('https://ipapi.co/json/')
    const data = await response.json()
    location.value = `${data.city}, ${data.country_name}`
    if (data.timezone) {
      emit('update:userTimezone', data.timezone)
    }
  } catch (error) {
    console.error('Error fetching location:', error)
    location.value = 'Location unavailable'
  }
})
</script> 