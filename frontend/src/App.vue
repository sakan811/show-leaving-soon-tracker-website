<template>
  <div class="container-default">
    <h1 v-if="selectedService === 'hbo'" class="title-primary">
      HBO Shows Leaving Soon
    </h1>
    <h1 v-else class="title-primary">
      Netflix Shows Leaving Soon
    </h1>
    <UserLocation v-model:userTimezone="userTimezone" />
    
    <div class="dropdown-container">
      <select v-model="selectedCountry" class="dropdown-select">
        <option value="th">Thailand</option>
        <option value="us">United States</option>
      </select>
      <select v-model="selectedService" class="dropdown-select">
        <option value="netflix">Netflix</option>
        <option value="hbo">HBO</option>
      </select>
    </div>

    <div v-if="Object.keys(leavingTitles).length === 0" class="no-data-message">
      No leaving shows at the moment
    </div>
    <div v-else class="grid-layout">
      <LeavingTitle
        v-for="(titles, date) in sortedLeavingTitles"
        :key="date"
        :date="date"
        :titles="titles"
      />
    </div>
    <footer class="footer-reference">
      Reference: <a href="https://docs.movieofthenight.com" class="ref-link" target="_blank" rel="noopener noreferrer">Streaming Availability API</a>
    </footer>
  </div>
</template>

<script setup>
import { ref, provide, computed, watch, onMounted } from 'vue'
import LeavingTitle from './components/LeavingTitle.vue'
import UserLocation from './components/UserLocation.vue'

const leavingTitles = ref({})
const userTimezone = ref(Intl.DateTimeFormat().resolvedOptions().timeZone)
const selectedCountry = ref('th')
const selectedService = ref('netflix')

// Provide timezone at App level
provide('userTimezone', userTimezone)

const fetchLeavingTitles = async () => {
  try {
    const response = await fetch(`/data/leaving_titles_${selectedCountry.value}_${selectedService.value}.json`)
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    leavingTitles.value = await response.json()
  } catch (error) {
    console.error('Error loading leaving titles:', error)
    leavingTitles.value = {} // Reset titles on error
  }
}

// Watch for changes in selectedCountry and selectedService to fetch titles automatically
watch([selectedCountry, selectedService], () => {
  fetchLeavingTitles()
})

// Fetch titles on component mount
onMounted(() => {
  fetchLeavingTitles()
})

// Computed property to sort leaving titles by date
const sortedLeavingTitles = computed(() => {
  const now = new Date(); // Current date and time
  return Object.keys(leavingTitles.value)
    .filter(date => new Date(date) > now) // Keep only future dates
    .sort() // Sort the dates
    .reduce((acc, date) => {
      acc[date] = leavingTitles.value[date]; // Ensure this is an array
      return acc;
    }, {});
});
</script>