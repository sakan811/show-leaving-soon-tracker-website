<template>
  <div class="container-default">
    <h1 class="title-primary">
      Netflix Titles Leaving Soon
    </h1>
    <UserLocation v-model:userTimezone="userTimezone" />
    <div class="grid-layout">
      <LeavingTitle
        v-for="(titles, date) in sortedLeavingTitles"
        :key="date"
        :date="date"
        :titles="titles"
      />
    </div>
    <footer class="footer-reference">
      Reference: <a href="https://docs.movieofthenight.com" class="tudum-link" target="_blank" rel="noopener noreferrer">Streaming Availability API</a>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, provide, computed } from 'vue'
import LeavingTitle from './components/LeavingTitle.vue'
import UserLocation from './components/UserLocation.vue'

const leavingTitles = ref({})
const userTimezone = ref(Intl.DateTimeFormat().resolvedOptions().timeZone)

// Provide timezone at App level
provide('userTimezone', userTimezone)

onMounted(async () => {
  try {
    const response = await fetch('/data/leaving_titles_jan_2025.json')
    leavingTitles.value = await response.json()
  } catch (error) {
    console.error('Error loading leaving titles:', error)
  }
})

// Computed property to sort leaving titles by date
const sortedLeavingTitles = computed(() => {
  return Object.keys(leavingTitles.value)
    .sort() // Sort the dates
    .reduce((acc, date) => {
      acc[date] = leavingTitles.value[date]
      return acc
    }, {})
})
</script>