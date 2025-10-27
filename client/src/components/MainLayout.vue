<template>
  <v-app>
    <!-- Static Sidebar -->
    <v-navigation-drawer
      class="sidebar"
      color="grey-lighten-5"
      elevation="3"
      permanent
      width="280"
    >
      <!-- Logo Section -->
      <div class="logo-section pa-6 text-center">
        <v-avatar class="mb-3" color="olive-green" size="200">
          <img alt="Logo" src="@/assets/LogoOasis.png">
        </v-avatar>
        <h2 class="text-h5 font-weight-bold text-olive-green">My Oasis</h2>
        <p class="text-body-2 text-grey-darken-1">Plant Assistant</p>
      </div>

      <v-divider class="mx-4 mb-4" />

      <!-- Navigation Buttons -->
      <v-list class="px-4" nav>
        <v-list-item
          v-for="item in navigationItems"
          :key="item.id"
          :active="currentPage === item.id"
          class="nav-item mb-2"
          color="azure-blue"
          rounded="lg"
          :value="item.id"
          @click="navigateTo(item.id)"
        >
          <template #prepend>
            <v-icon :color="currentPage === item.id ? 'azure-blue' : 'grey-darken-1'">
              {{ item.icon }}
            </v-icon>
          </template>
          <v-list-item-title class="font-weight-medium">
            {{ item.title }}
          </v-list-item-title>
        </v-list-item>
      </v-list>

      <!-- Sidebar Footer -->
      <template #append>
        <div class="pa-4 text-center">
          <v-divider class="mb-3" />
          <p class="text-caption text-grey-darken-1">
            Version 1.0.0
          </p>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Main Content Area -->
    <v-main class="main-content">
      <!-- Header -->
      <v-app-bar
        class="header-bar"
        color="white"
        elevation="2"
        height="70"
      >
        <v-app-bar-title class="text-center">
          <h1 class="text-h4 font-weight-bold text-azure-blue">
            {{ currentPageTitle }}
          </h1>
        </v-app-bar-title>

        <!-- Profile Menu -->
        <template #append>
          <v-menu offset-y>
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                class="mr-4"
                color="azure-blue"
                icon
                size="large"
              >
                <v-avatar color="azure-blue" size="40">
                  <v-icon color="white">mdi-account</v-icon>
                </v-avatar>
              </v-btn>
            </template>

            <v-list min-width="200">
              <v-list-item
                v-for="menuItem in profileMenuItems"
                :key="menuItem.title"
                @click="handleProfileAction(menuItem.action)"
              >
                <template #prepend>
                  <v-icon :color="menuItem.color || 'grey-darken-1'">
                    {{ menuItem.icon }}
                  </v-icon>
                </template>
                <v-list-item-title>{{ menuItem.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-app-bar>

      <!-- Page Content -->
      <v-container class="page-container pa-0" fluid>
        <!-- Welcome Page with Chat Interface -->
        <div v-if="currentPage === 'welcome'" class="welcome-page">
          <WelcomeChatInterface />
        </div>

        <!-- Adviser Page -->
        <div v-else-if="currentPage === 'adviser'" class="welcome-page">
          <AdviserPage />
        </div>

        <!-- Dr. Oasis Page -->
        <div v-else-if="currentPage === 'dr-oasis'" class="welcome-page">
          <DrOasisPage />
        </div>

        <!-- About Oasis Page -->
        <div v-else-if="currentPage === 'about'" class="other-page">
          <AboutOasisPage />
        </div>

        <!-- Other Pages (Placeholder for now) -->
        <div v-else class="other-page pa-6">
          <v-card class="pa-8 text-center" elevation="2" rounded="lg">
            <v-icon class="mb-4" color="olive-green" size="64">
              {{ getCurrentPageIcon() }}
            </v-icon>
            <h2 class="text-h4 font-weight-bold text-olive-green mb-4">
              {{ currentPageTitle }}
            </h2>
            <p class="text-body-1 text-grey-darken-1">
              This page is under development. Please check back soon!
            </p>
          </v-card>
        </div>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer
      class="footer pa-2"
      color="grey-darken-3"
      height="60"
    >
      <v-container class="pa-2">
        <v-row align="center" no-gutters>
          <v-col cols="12" md="8">
            <div class="text-white d-flex align-center">
              <span class="text-body-2 font-weight-bold mr-4">LogoOasis</span>
              <span class="text-caption mr-4">© 2024 Oasis Technologies. All rights reserved.</span>
              <span class="text-caption">Contact: support@oasis-plants.com</span>
            </div>
          </v-col>
          <v-col class="text-md-right" cols="12" md="4">
            <div class="d-flex justify-md-end justify-start align-center">
              <v-btn
                class="mr-1"
                color="white"
                icon
                size="x-small"
                variant="text"
              >
                <v-icon size="16">mdi-facebook</v-icon>
              </v-btn>
              <v-btn
                class="mr-1"
                color="white"
                icon
                size="x-small"
                variant="text"
              >
                <v-icon size="16">mdi-twitter</v-icon>
              </v-btn>
              <v-btn
                color="white"
                icon
                size="x-small"
                variant="text"
              >
                <v-icon size="16">mdi-instagram</v-icon>
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>

    <!-- Settings Dialog -->
    <v-dialog v-model="settingsDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h6 font-weight-bold text-azure-blue">
          <v-icon class="mr-2">mdi-cog</v-icon>
          Settings
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <v-switch
                v-model="settings.notifications"
                color="azure-blue"
                hide-details
                label="Enable Notifications"
              />
            </v-col>
            <v-col cols="12">
              <v-switch
                v-model="settings.darkMode"
                color="azure-blue"
                hide-details
                label="Dark Mode"
              />
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="settings.language"
                color="azure-blue"
                :items="languages"
                label="Language"
                variant="outlined"
              />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="settingsDialog = false">Cancel</v-btn>
          <v-btn color="azure-blue" @click="saveSettings">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Help Dialog -->
    <v-dialog v-model="helpDialog" max-width="600">
      <v-card>
        <v-card-title class="text-h6 font-weight-bold text-azure-blue">
          <v-icon class="mr-2">mdi-help-circle</v-icon>
          Help & Support
        </v-card-title>
        <v-card-text>
          <h3 class="text-h6 font-weight-bold mb-3">How to use Oasis:</h3>
          <v-list>
            <v-list-item>
              <template #prepend>
                <v-icon color="olive-green">mdi-chat</v-icon>
              </template>
              <v-list-item-title>Chat with our AI assistant for plant advice</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template #prepend>
                <v-icon color="olive-green">mdi-camera</v-icon>
              </template>
              <v-list-item-title>Upload plant photos for health analysis</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template #prepend>
                <v-icon color="olive-green">mdi-book</v-icon>
              </template>
              <v-list-item-title>Browse our plant care library</v-list-item-title>
            </v-list-item>
          </v-list>
          <v-divider class="my-4" />
          <p class="text-body-2">
            For additional support, contact us at support@oasis-plants.com
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="azure-blue" @click="helpDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup lang="ts">
  import { computed, reactive, ref } from 'vue'
  import AboutOasisPage from './AboutOasisPage.vue'
  import AdviserPage from './AdviserPage.vue'
  import DrOasisPage from './DrOasisPage.vue'
  import WelcomeChatInterface from './WelcomeChatInterface.vue'

  // Reactive data
  const currentPage = ref('welcome')
  const settingsDialog = ref(false)
  const helpDialog = ref(false)

  const settings = reactive({
    notifications: true,
    darkMode: false,
    language: 'English',
  })

  // Navigation items
  const navigationItems = [
    {
      id: 'welcome',
      title: 'Welcome',
      icon: 'mdi-home',
    },
    {
      id: 'adviser',
      title: 'Adviser',
      icon: 'mdi-chat',
    },
    {
      id: 'dr-oasis',
      title: 'Dr. Oasis',
      icon: 'mdi-medical-bag',
    },
    {
      id: 'about',
      title: 'About Oasis',
      icon: 'mdi-information',
    },
    {
      id: 'journal',
      title: 'Garden Journal',
      icon: 'mdi-book-open-variant',
    },
  ]

  // Profile menu items
  const profileMenuItems = [
    {
      title: 'Settings',
      icon: 'mdi-cog',
      action: 'settings',
    },
    {
      title: 'Help',
      icon: 'mdi-help-circle',
      action: 'help',
    },
    {
      title: 'Sign Out',
      icon: 'mdi-logout',
      action: 'signout',
      color: 'red',
    },
  ]

  const languages = ['English', 'Spanish', 'French', 'German']

  // Computed properties
  const currentPageTitle = computed(() => {
    const pageMap: Record<string, string> = {
      'welcome': 'MY OASIS',
      'adviser': 'ADVISER',
      'dr-oasis': 'DR. OASIS',
      'about': 'ABOUT OASIS',
      'journal': 'GARDEN JOURNAL',
    }
    return pageMap[currentPage.value] || 'OASIS'
  })

  // Methods
  function navigateTo (pageId: string) {
    currentPage.value = pageId
  }

  function handleProfileAction (action: string) {
    switch (action) {
      case 'settings': {
        settingsDialog.value = true
        break
      }
      case 'help': {
        helpDialog.value = true
        break
      }
      case 'signout': {
        // Handle sign out logic
        console.log('Sign out clicked')
        break
      }
    }
  }

  function saveSettings () {
    // Save settings logic
    localStorage.setItem('oasis-settings', JSON.stringify(settings))
    settingsDialog.value = false
  }

  function getCurrentPageIcon () {
    const item = navigationItems.find(item => item.id === currentPage.value)
    return item?.icon || 'mdi-home'
  }
</script>

<style scoped>
.sidebar {
  border-right: 2px solid #e0e0e0;
}

.logo-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 0 0 20px 20px;
  margin: 0 16px 16px 16px;
}

.nav-item {
  transition: all 0.3s ease;
}

.nav-item:hover {
  transform: translateX(4px);
}

.header-bar {
  border-bottom: 2px solid #e3f2fd;
}

.main-content {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.page-container {
  min-height: calc(100vh - 130px);
}

.welcome-page {
  height: calc(100vh - 130px);
}

.other-page {
  height: calc(100vh - 130px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer {
  border-top: 2px solid #424242;
}

/* Custom color classes */
.text-azure-blue {
  color: #2196f3 !important;
}

.text-olive-green {
  color: #689f38 !important;
}

.bg-azure-blue {
  background-color: #2196f3 !important;
}

.bg-olive-green {
  background-color: #689f38 !important;
}
</style>
