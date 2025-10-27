<template>
  <v-navigation-drawer
    v-model="drawer"
    color="green-lighten-5"
    elevation="2"
    permanent
    :rail="rail"
  >
    <!-- Header -->
    <v-list-item
      class="mb-2"
      :prepend-avatar="rail ? undefined : '/logo.png'"
      :subtitle="rail ? undefined : 'Plant Assistant'"
      :title="rail ? undefined : 'Oasis'"
    >
      <template #prepend>
        <v-avatar color="green-darken-1" :size="rail ? 32 : 40">
          <v-icon color="white" :size="rail ? 16 : 24">mdi-leaf</v-icon>
        </v-avatar>
      </template>

      <template #append>
        <v-btn
          icon="mdi-chevron-left"
          variant="text"
          @click.stop="rail = !rail"
        />
      </template>
    </v-list-item>

    <v-divider class="mb-2" />

    <!-- Navigation Items -->
    <v-list density="compact" nav>
      <v-list-item
        v-for="item in navigationItems"
        :key="item.value"
        :active="currentView === item.value"
        color="green-darken-1"
        :prepend-icon="item.icon"
        :title="item.title"
        :value="item.value"
        @click="$emit('navigate', item.value)"
      >
        <template #prepend>
          <v-icon :color="currentView === item.value ? 'green-darken-1' : 'grey-darken-1'">
            {{ item.icon }}
          </v-icon>
        </template>
      </v-list-item>
    </v-list>

    <v-divider class="my-4" />

    <!-- User Section -->
    <v-list density="compact">
      <v-list-item
        prepend-icon="mdi-account-circle"
        :subtitle="rail ? undefined : 'Gardener'"
        :title="rail ? undefined : userName"
        @click="showUserDialog = true"
      >
        <template #prepend>
          <v-icon color="grey-darken-1">mdi-account-circle</v-icon>
        </template>
      </v-list-item>

      <v-list-item
        prepend-icon="mdi-cog"
        :title="rail ? undefined : 'Settings'"
        @click="showSettingsDialog = true"
      >
        <template #prepend>
          <v-icon color="grey-darken-1">mdi-cog</v-icon>
        </template>
      </v-list-item>
    </v-list>

    <!-- Footer -->
    <template #append>
      <div class="pa-2 text-center">
        <v-btn
          v-if="!rail"
          color="grey-darken-1"
          size="small"
          variant="text"
          @click="showAboutDialog = true"
        >
          About Oasis
        </v-btn>
        <v-btn
          v-else
          color="grey-darken-1"
          icon="mdi-information"
          size="small"
          variant="text"
          @click="showAboutDialog = true"
        />
      </div>
    </template>
  </v-navigation-drawer>

  <!-- User Profile Dialog -->
  <v-dialog v-model="showUserDialog" max-width="400">
    <v-card>
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-account-circle</v-icon>
        User Profile
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="tempUserName"
          hint="This name will be used in conversations"
          label="Your Name"
          persistent-hint
          prepend-icon="mdi-account"
          variant="outlined"
        />
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="showUserDialog = false">Cancel</v-btn>
        <v-btn color="green-darken-1" @click="saveUserName">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Settings Dialog -->
  <v-dialog v-model="showSettingsDialog" max-width="500">
    <v-card>
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-cog</v-icon>
        Settings
      </v-card-title>

      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-switch
              v-model="settings.darkMode"
              color="green-darken-1"
              hide-details
              label="Dark Mode"
            />
          </v-col>
          <v-col cols="12">
            <v-switch
              v-model="settings.notifications"
              color="green-darken-1"
              hide-details
              label="Enable Notifications"
            />
          </v-col>
          <v-col cols="12">
            <v-switch
              v-model="settings.autoSave"
              color="green-darken-1"
              hide-details
              label="Auto-save Conversations"
            />
          </v-col>
          <v-col cols="12">
            <v-select
              v-model="settings.language"
              :items="languages"
              label="Language"
              prepend-icon="mdi-translate"
              variant="outlined"
            />
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="showSettingsDialog = false">Cancel</v-btn>
        <v-btn color="green-darken-1" @click="saveSettings">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- About Dialog -->
  <v-dialog v-model="showAboutDialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5 text-center text-green-darken-1">
        <v-icon class="mr-2" size="32">mdi-leaf</v-icon>
        About Oasis
      </v-card-title>

      <v-card-text class="text-center">
        <v-avatar class="mb-4" color="green-lighten-2" size="80">
          <v-icon color="white" size="40">mdi-sprout</v-icon>
        </v-avatar>

        <h3 class="text-h6 font-weight-bold mb-2">Your Personal Plant Assistant</h3>

        <p class="text-body-1 mb-4">
          Oasis is an AI-powered gardening assistant designed to help you grow healthy plants
          and create thriving gardens. Whether you're a beginner or an experienced gardener,
          Oasis provides personalized advice and recommendations.
        </p>

        <v-row class="mb-4">
          <v-col cols="4">
            <v-icon class="mb-2" color="green-darken-1" size="32">mdi-chat</v-icon>
            <div class="text-caption font-weight-bold">Chat Support</div>
            <div class="text-caption text-grey-darken-1">24/7 plant advice</div>
          </v-col>
          <v-col cols="4">
            <v-icon class="mb-2" color="green-darken-1" size="32">mdi-calendar-check</v-icon>
            <div class="text-caption font-weight-bold">Crop Planning</div>
            <div class="text-caption text-grey-darken-1">Seasonal recommendations</div>
          </v-col>
          <v-col cols="4">
            <v-icon class="mb-2" color="green-darken-1" size="32">mdi-camera</v-icon>
            <div class="text-caption font-weight-bold">Plant Health</div>
            <div class="text-caption text-grey-darken-1">Image analysis</div>
          </v-col>
        </v-row>

        <v-divider class="my-4" />

        <div class="text-caption text-grey-darken-1">
          Version 1.0.0 • Built with Vue 3 & Vuetify • Powered by AI
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn color="green-darken-1" @click="showAboutDialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
  import { onMounted, reactive, ref } from 'vue'

  // Props
  interface Props {
    currentView: string
  }

  const props = defineProps<Props>()

  // Emits
  const emit = defineEmits<{
    navigate: [view: string]
  }>()

  // Reactive data
  const drawer = ref(true)
  const rail = ref(false)
  const showUserDialog = ref(false)
  const showSettingsDialog = ref(false)
  const showAboutDialog = ref(false)
  const userName = ref('Friend')
  const tempUserName = ref('')

  const settings = reactive({
    darkMode: false,
    notifications: true,
    autoSave: true,
    language: 'English',
  })

  // Navigation items
  const navigationItems = [
    {
      title: 'Chat',
      icon: 'mdi-chat',
      value: 'chat',
    },
    {
      title: 'Crop Planner',
      icon: 'mdi-sprout-outline',
      value: 'crop-planner',
    },
    {
      title: 'Plant Health',
      icon: 'mdi-medical-bag',
      value: 'plant-health',
    },
    {
      title: 'Garden Journal',
      icon: 'mdi-book-open-variant',
      value: 'journal',
    },
    {
      title: 'Plant Library',
      icon: 'mdi-library',
      value: 'library',
    },
  ]

  const languages = [
    'English',
    'Spanish',
    'French',
    'German',
    'Italian',
    'Portuguese',
  ]

  // Methods
  function saveUserName () {
    userName.value = tempUserName.value || 'Friend'
    localStorage.setItem('oasis-user-name', userName.value)
    showUserDialog.value = false
  }

  function saveSettings () {
    localStorage.setItem('oasis-settings', JSON.stringify(settings))
    showSettingsDialog.value = false

    // Apply dark mode if needed
    document.documentElement.classList.toggle('dark', settings.darkMode)
  }

  // Lifecycle
  onMounted(() => {
    // Load saved user name
    const savedName = localStorage.getItem('oasis-user-name')
    if (savedName) {
      userName.value = savedName
      tempUserName.value = savedName
    }

    // Load saved settings
    const savedSettings = localStorage.getItem('oasis-settings')
    if (savedSettings) {
      Object.assign(settings, JSON.parse(savedSettings))
    }
  })
</script>

<style scoped>
.v-navigation-drawer {
  border-right: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
