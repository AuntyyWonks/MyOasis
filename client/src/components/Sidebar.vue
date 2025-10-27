<template>
  <div class="sidebar bg-gray-900 text-white w-64 flex flex-col p-4">
    <div class="logo mb-8 text-center">
      <img alt="My Oasis" class="h-16 mx-auto" src="/logo.png">
    </div>

    <NuxtLink v-for="page in pages" :key="page.name" class="btn mb-4 py-2 px-4 rounded hover:bg-gray-700" :to="page.route">
      {{ page.name }}
    </NuxtLink>
  </div>
</template>

<script setup>
  const pages = [
    { name: 'Welcome', route: '/' },
    { name: 'Dr Oasis', route: '/dr-oasis' },
    { name: 'Advisor', route: '/advisor' },
    { name: 'About Me', route: '/about-me' },
    { name: 'Page 5', route: '/page5' },
  ]
</script>

<style scoped>
.sidebar { min-width: 16rem; }
.btn { display: block; text-align: center; font-weight: bold; }
</style>
