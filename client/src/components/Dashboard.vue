<template>
  <v-app>
    <!-- Navigation Drawer -->
    <NavigationDrawer
      :current-view="currentView"
      @navigate="handleNavigation"
    />

    <!-- Main Content -->
    <v-main>
      <v-container fluid class="pa-0">
        <!-- Chat Interface -->
        <div v-if="currentView === 'chat'">
          <ChatInterface />
        </div>

        <!-- Crop Planner -->
        <div v-else-if="currentView === 'crop-planner'">
          <CropPlanner />
        </div>

        <!-- Plant Health -->
        <div v-else-if="currentView === 'plant-health'">
          <PlantHealthAnalyzer />
        </div>

        <!-- Garden Journal -->
        <div v-else-if="currentView === 'journal'">
          <GardenJournal />
        </div>

        <!-- Plant Library -->
        <div v-else-if="currentView === 'library'">
          <PlantLibrary />
        </div>

        <!-- Default/Home View -->
        <div v-else>
          <HomeView @navigate="handleNavigation" />
        </div>
      </v-container>
    </v-main>

    <!-- Floating Action Button for Quick Chat -->
    <v-fab
      v-if="currentView !== 'chat'"
      icon="mdi-chat"
      color="green-darken-1"
      size="large"
      location="bottom end"
      app
      @click="handleNavigation('chat')"
    />
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NavigationDrawer from './NavigationDrawer.vue'
import ChatInterface from './ChatInterface.vue'
import CropPlanner from './CropPlanner.vue'
import PlantHealthAnalyzer from './PlantHealthAnalyzer.vue'
import GardenJournal from './GardenJournal.vue'
import PlantLibrary from './PlantLibrary.vue'
import HomeView from './HomeView.vue'

// Reactive data
const currentView = ref('home')

// Methods
const handleNavigation = (view: string) => {
  currentView.value = view
}
</script>

<style scoped>
.v-main {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}
</style>