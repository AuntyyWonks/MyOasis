<template>
  <v-container class="home-view pa-0" fluid>
    <!-- Hero Section -->
    <v-row no-gutters>
      <v-col cols="12">
        <v-card
          class="hero-card"
          color="green-darken-1"
          min-height="400"
          rounded="0"
        >
          <v-card-text class="text-center py-12">
            <v-avatar class="mb-6" color="white" size="120">
              <v-icon color="green-darken-1" size="60">mdi-leaf</v-icon>
            </v-avatar>

            <h1 class="text-h2 font-weight-bold text-white mb-4">
              Welcome to My Oasis
            </h1>

            <p class="text-h6 text-green-lighten-4 mb-6 mx-auto" style="max-width: 600px;">
              Your AI-powered gardening companion. Get personalized plant care advice,
              crop recommendations, and health analysis for your green friends.
            </p>

            <v-btn
              class="mr-4"
              color="white"
              size="large"
              @click="$emit('navigate', 'chat')"
            >
              <v-icon class="mr-2">mdi-chat</v-icon>
              Start Chatting
            </v-btn>

            <v-btn
              color="green-lighten-2"
              size="large"
              variant="outlined"
              @click="$emit('navigate', 'crop-planner')"
            >
              <v-icon class="mr-2">mdi-sprout</v-icon>
              Plan Your Garden
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Features Section -->
    <v-container class="py-12">
      <v-row>
        <v-col class="text-center mb-8" cols="12">
          <h2 class="text-h3 font-weight-bold text-green-darken-1 mb-4">
            Everything You Need for Gardening Success
          </h2>
          <p class="text-h6 text-grey-darken-1">
            Discover the tools and features that make Oasis your perfect gardening partner
          </p>
        </v-col>
      </v-row>

      <v-row>
        <v-col
          v-for="feature in features"
          :key="feature.title"
          cols="12"
          lg="3"
          md="6"
        >
          <v-card
            class="feature-card h-100"
            elevation="2"
            rounded="lg"
            @click="$emit('navigate', feature.route)"
          >
            <v-card-text class="text-center pa-6">
              <v-avatar
                class="mb-4"
                :color="feature.color"
                size="80"
              >
                <v-icon color="white" size="40">{{ feature.icon }}</v-icon>
              </v-avatar>

              <h3 class="text-h5 font-weight-bold mb-3">{{ feature.title }}</h3>
              <p class="text-body-1 text-grey-darken-1 mb-4">{{ feature.description }}</p>

              <v-btn
                :color="feature.color"
                variant="outlined"
                @click.stop="$emit('navigate', feature.route)"
              >
                {{ feature.buttonText }}
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Quick Stats -->
    <v-container class="py-8">
      <v-row>
        <v-col cols="12">
          <v-card color="grey-lighten-5" elevation="1" rounded="lg">
            <v-card-text class="py-8">
              <v-row>
                <v-col
                  v-for="stat in stats"
                  :key="stat.label"
                  class="text-center"
                  cols="6"
                  md="3"
                >
                  <div class="text-h3 font-weight-bold" :class="stat.color">
                    {{ stat.value }}
                  </div>
                  <div class="text-body-1 text-grey-darken-1">{{ stat.label }}</div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Getting Started -->
    <v-container class="py-12">
      <v-row>
        <v-col cols="12" md="6">
          <v-card class="h-100" elevation="2" rounded="lg">
            <v-card-title class="text-h5 font-weight-bold text-green-darken-1">
              <v-icon class="mr-2">mdi-rocket-launch</v-icon>
              Getting Started
            </v-card-title>

            <v-card-text>
              <v-timeline density="compact" side="end">
                <v-timeline-item
                  v-for="(step, index) in gettingStartedSteps"
                  :key="index"
                  :dot-color="step.color"
                  size="small"
                >
                  <template #icon>
                    <v-icon color="white" size="16">{{ step.icon }}</v-icon>
                  </template>

                  <div class="mb-4">
                    <h4 class="text-h6 font-weight-bold">{{ step.title }}</h4>
                    <p class="text-body-2 text-grey-darken-1 mb-2">{{ step.description }}</p>
                    <v-btn
                      :color="step.color"
                      size="small"
                      variant="text"
                      @click="$emit('navigate', step.route)"
                    >
                      {{ step.action }}
                      <v-icon class="ml-1">mdi-arrow-right</v-icon>
                    </v-btn>
                  </div>
                </v-timeline-item>
              </v-timeline>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card class="h-100" elevation="2" rounded="lg">
            <v-card-title class="text-h5 font-weight-bold text-green-darken-1">
              <v-icon class="mr-2">mdi-lightbulb</v-icon>
              Today's Garden Tip
            </v-card-title>

            <v-card-text>
              <v-card class="mb-4" color="green-lighten-5" rounded="lg">
                <v-card-text>
                  <div class="d-flex align-center mb-3">
                    <v-icon class="mr-3" color="green-darken-1" size="32">{{ todaysTip.icon }}</v-icon>
                    <h4 class="text-h6 font-weight-bold">{{ todaysTip.title }}</h4>
                  </div>
                  <p class="text-body-1">{{ todaysTip.content }}</p>
                </v-card-text>
              </v-card>

              <div class="text-center">
                <v-btn
                  color="green-darken-1"
                  variant="outlined"
                  @click="getNewTip"
                >
                  <v-icon class="mr-2">mdi-refresh</v-icon>
                  Get Another Tip
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Recent Activity -->
    <v-container v-if="recentActivity.length > 0" class="py-8">
      <v-row>
        <v-col cols="12">
          <v-card elevation="2" rounded="lg">
            <v-card-title class="text-h5 font-weight-bold text-green-darken-1">
              <v-icon class="mr-2">mdi-history</v-icon>
              Recent Activity
            </v-card-title>

            <v-card-text>
              <v-list>
                <v-list-item
                  v-for="(activity, index) in recentActivity"
                  :key="index"
                  :prepend-icon="activity.icon"
                  :subtitle="activity.subtitle"
                  :title="activity.title"
                >
                  <template #prepend>
                    <v-icon :color="activity.color">{{ activity.icon }}</v-icon>
                  </template>

                  <template #append>
                    <span class="text-caption text-grey-darken-1">{{ activity.time }}</span>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script setup lang="ts">
  import { onMounted, ref } from 'vue'

  // Emits
  const emit = defineEmits<{
    navigate: [view: string]
  }>()

  // Reactive data
  const todaysTip = ref({
    title: 'Watering Wisdom',
    content: 'Water your plants in the morning to give them time to absorb moisture before the heat of the day. This helps prevent fungal diseases and ensures optimal hydration.',
    icon: 'mdi-water',
  })

  const recentActivity = ref([
    {
      title: 'Plant health analysis completed',
      subtitle: 'Analyzed tomato plant leaves',
      icon: 'mdi-medical-bag',
      color: 'green',
      time: '2 hours ago',
    },
    {
      title: 'New journal entry added',
      subtitle: 'Watered herb garden',
      icon: 'mdi-book-open-variant',
      color: 'blue',
      time: '1 day ago',
    },
    {
      title: 'Crop plan generated',
      subtitle: 'Spring vegetable recommendations',
      icon: 'mdi-sprout',
      color: 'orange',
      time: '3 days ago',
    },
  ])

  // Static data
  const features = [
    {
      title: 'AI Chat Assistant',
      description: 'Get instant answers to all your gardening questions from our AI-powered plant expert.',
      icon: 'mdi-chat',
      color: 'green-darken-1',
      buttonText: 'Start Chatting',
      route: 'chat',
    },
    {
      title: 'Crop Planner',
      description: 'Receive personalized crop recommendations based on your location and preferences.',
      icon: 'mdi-sprout-outline',
      color: 'orange-darken-1',
      buttonText: 'Plan Garden',
      route: 'crop-planner',
    },
    {
      title: 'Plant Health Analysis',
      description: 'Upload photos of your plants to get instant health diagnosis and treatment advice.',
      icon: 'mdi-medical-bag',
      color: 'red-darken-1',
      buttonText: 'Analyze Plants',
      route: 'plant-health',
    },
    {
      title: 'Garden Journal',
      description: 'Track your gardening journey with detailed logs and progress photos.',
      icon: 'mdi-book-open-variant',
      color: 'blue-darken-1',
      buttonText: 'Start Journal',
      route: 'journal',
    },
  ]

  const stats = [
    { value: '10K+', label: 'Plants Analyzed', color: 'text-green-darken-1' },
    { value: '500+', label: 'Garden Plans', color: 'text-orange-darken-1' },
    { value: '1K+', label: 'Happy Gardeners', color: 'text-blue-darken-1' },
    { value: '24/7', label: 'AI Support', color: 'text-purple-darken-1' },
  ]

  const gettingStartedSteps = [
    {
      title: 'Ask Your First Question',
      description: 'Start by asking our AI assistant about any plant or gardening topic.',
      action: 'Open Chat',
      route: 'chat',
      icon: 'mdi-chat',
      color: 'green',
    },
    {
      title: 'Plan Your Garden',
      description: 'Get personalized crop recommendations for your specific location and goals.',
      action: 'Create Plan',
      route: 'crop-planner',
      icon: 'mdi-sprout',
      color: 'orange',
    },
    {
      title: 'Track Your Progress',
      description: 'Start a garden journal to document your plants\' growth and care.',
      action: 'Start Journal',
      route: 'journal',
      icon: 'mdi-book',
      color: 'blue',
    },
    {
      title: 'Explore Plant Library',
      description: 'Browse our extensive library to learn about different plants.',
      action: 'Browse Library',
      route: 'library',
      icon: 'mdi-library',
      color: 'purple',
    },
  ]

  const gardenTips = [
    {
      title: 'Watering Wisdom',
      content: 'Water your plants in the morning to give them time to absorb moisture before the heat of the day. This helps prevent fungal diseases and ensures optimal hydration.',
      icon: 'mdi-water',
    },
    {
      title: 'Soil Health',
      content: 'Healthy soil is the foundation of a thriving garden. Add compost regularly to improve soil structure, drainage, and nutrient content.',
      icon: 'mdi-earth',
    },
    {
      title: 'Companion Planting',
      content: 'Plant basil near tomatoes to improve their flavor and repel pests. Marigolds planted throughout the garden can help deter harmful insects.',
      icon: 'mdi-leaf',
    },
    {
      title: 'Pruning Tips',
      content: 'Regular pruning encourages healthy growth and better air circulation. Always use clean, sharp tools to prevent disease transmission.',
      icon: 'mdi-content-cut',
    },
    {
      title: 'Seasonal Care',
      content: 'Adjust your watering schedule with the seasons. Plants need less water in winter and more during hot summer months.',
      icon: 'mdi-calendar',
    },
  ]

  // Methods
  function getNewTip () {
    const index = Math.floor(Math.random() * gardenTips.length)
    const randomTip = gardenTips[index]!
    todaysTip.value = randomTip
  }

  // Lifecycle
  onMounted(() => {
    // Load recent activity from localStorage if available
    const savedActivity = localStorage.getItem('oasis-recent-activity')
    if (savedActivity) {
      recentActivity.value = JSON.parse(savedActivity)
    }
  })
</script>

<style scoped>
.home-view {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.hero-card {
  background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
}

.feature-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
</style>
