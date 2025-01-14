<template>
  <div class="container-default">
    <h1 class="title-primary">
      Netflix Titles Leaving Soon
    </h1>
    <UserLocation v-model:userTimezone="userTimezone" />
    <div class="grid-layout">
      <LeavingTitle
        v-for="(titles, date) in leavingTitles"
        :key="date"
        :date="date"
        :titles="titles"
      />
    </div>
    <footer class="footer-reference">
      Reference: <a href="https://www.movieofthenight.com/catalog/netflix/th/leaving" class="tudum-link" target="_blank" rel="noopener noreferrer">Movie of the Night</a>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
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
</script>