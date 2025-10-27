<template>
  <v-container class="crop-planner pa-4" fluid>
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card class="mb-4" color="green-darken-1" rounded="lg">
          <v-card-text class="text-center py-6">
            <v-icon class="mb-2" color="white" size="48">mdi-sprout-outline</v-icon>
            <h2 class="text-h4 font-weight-bold text-white mb-2">Crop Planner</h2>
            <p class="text-green-lighten-4 text-body-1">
              Get personalized crop recommendations based on your location, climate, and preferences
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Input Form -->
      <v-col cols="12" md="6">
        <v-card elevation="2" rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-form-select</v-icon>
            Tell us about your garden
          </v-card-title>

          <v-card-text>
            <v-form ref="form" v-model="valid">
              <!-- Location -->
              <v-text-field
                v-model="formData.location"
                class="mb-3"
                hint="e.g., San Francisco, CA or London, UK"
                label="Location (City, State/Country)"
                persistent-hint
                prepend-icon="mdi-map-marker"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Garden Size -->
              <v-select
                v-model="formData.gardenSize"
                class="mb-3"
                :items="gardenSizes"
                label="Garden Size"
                prepend-icon="mdi-resize"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Experience Level -->
              <v-select
                v-model="formData.experience"
                class="mb-3"
                :items="experienceLevels"
                label="Gardening Experience"
                prepend-icon="mdi-account-star"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Garden Type -->
              <v-select
                v-model="formData.gardenType"
                class="mb-3"
                :items="gardenTypes"
                label="Garden Type"
                prepend-icon="mdi-home-variant"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Soil Type -->
              <v-select
                v-model="formData.soilType"
                class="mb-3"
                hint="Leave blank if unsure"
                :items="soilTypes"
                label="Soil Type (if known)"
                persistent-hint
                prepend-icon="mdi-earth"
                variant="outlined"
              />

              <!-- Preferences -->
              <v-textarea
                v-model="formData.preferences"
                class="mb-3"
                hint="e.g., I want to grow vegetables for cooking, prefer low-maintenance plants, interested in herbs"
                label="Preferences & Goals"
                persistent-hint
                prepend-icon="mdi-heart"
                rows="3"
                variant="outlined"
              />

              <!-- Additional Info -->
              <v-textarea
                v-model="formData.additionalInfo"
                class="mb-4"
                hint="Any other details about your garden, climate, or specific requirements"
                label="Additional Information"
                persistent-hint
                prepend-icon="mdi-information"
                rows="2"
                variant="outlined"
              />

              <!-- Submit Button -->
              <v-btn
                block
                color="green-darken-1"
                :disabled="!valid"
                :loading="loading"
                size="large"
                @click="getCropRecommendations"
              >
                <v-icon class="mr-2">mdi-magic-staff</v-icon>
                Get My Crop Plan
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Results -->
      <v-col cols="12" md="6">
        <v-card elevation="2" min-height="400" rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-clipboard-list</v-icon>
            Your Personalized Crop Plan
          </v-card-title>

          <v-card-text>
            <!-- Loading State -->
            <div v-if="loading" class="text-center py-8">
              <v-progress-circular
                class="mb-4"
                color="green-darken-1"
                indeterminate
                size="64"
              />
              <p class="text-body-1">Creating your personalized crop plan...</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="!recommendations" class="text-center py-8">
              <v-icon class="mb-4" color="grey-lighten-1" size="64">mdi-sprout</v-icon>
              <p class="text-body-1 text-grey-darken-1">
                Fill out the form to get your personalized crop recommendations
              </p>
            </div>

            <!-- Results -->
            <div v-else>
              <!-- Summary Stats -->
              <v-row class="mb-4">
                <v-col cols="6">
                  <v-card class="text-center pa-3" color="green-lighten-5" rounded="lg">
                    <v-icon class="mb-1" color="green-darken-1" size="24">mdi-sprout</v-icon>
                    <div class="text-h6 font-weight-bold text-green-darken-1">
                      {{ recommendations.recommendations_list.length }}
                    </div>
                    <div class="text-caption text-green-darken-2">Recommendations</div>
                  </v-card>
                </v-col>
                <v-col cols="6">
                  <v-card class="text-center pa-3" color="blue-lighten-5" rounded="lg">
                    <v-icon class="mb-1" color="blue-darken-1" size="24">mdi-calendar</v-icon>
                    <div class="text-h6 font-weight-bold text-blue-darken-1">
                      {{ getCurrentSeason() }}
                    </div>
                    <div class="text-caption text-blue-darken-2">Current Season</div>
                  </v-card>
                </v-col>
              </v-row>

              <!-- Recommendations List -->
              <v-expansion-panels class="mb-4" variant="accordion">
                <v-expansion-panel
                  v-for="(recommendation, index) in recommendations.recommendations_list"
                  :key="index"
                  :title="`Recommendation ${index + 1}`"
                >
                  <v-expansion-panel-text>
                    <div class="text-body-2">{{ recommendation }}</div>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

              <!-- Full Text -->
              <v-card color="grey-lighten-5" rounded="lg">
                <v-card-title class="text-subtitle-1 font-weight-bold">
                  Complete Recommendations
                </v-card-title>
                <v-card-text>
                  <div class="text-body-2" style="white-space: pre-line;">
                    {{ recommendations.recommendations_text }}
                  </div>
                </v-card-text>
              </v-card>

              <!-- Action Buttons -->
              <v-row class="mt-4">
                <v-col cols="6">
                  <v-btn
                    block
                    color="green-darken-1"
                    variant="outlined"
                    @click="saveRecommendations"
                  >
                    <v-icon class="mr-2">mdi-download</v-icon>
                    Save Plan
                  </v-btn>
                </v-col>
                <v-col cols="6">
                  <v-btn
                    block
                    color="blue-darken-1"
                    variant="outlined"
                    @click="shareRecommendations"
                  >
                    <v-icon class="mr-2">mdi-share</v-icon>
                    Share
                  </v-btn>
                </v-col>
              </v-row>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.message }}
      <template #actions>
        <v-btn
          color="white"
          variant="text"
          @click="snackbar.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
  import { reactive, ref } from 'vue'
  import { apiUrl } from '@/utils/api'

  interface CropRecommendations {
    recommendations_text: string
    recommendations_list: string[]
  }

  // Reactive data
  const valid = ref(false)
  const loading = ref(false)
  const recommendations = ref<CropRecommendations | null>(null)
  const form = ref()

  const formData = reactive({
    location: '',
    gardenSize: '',
    experience: '',
    gardenType: '',
    soilType: '',
    preferences: '',
    additionalInfo: '',
  })

  const snackbar = reactive({
    show: false,
    message: '',
    color: 'success',
  })

  // Form options
  const gardenSizes = [
    'Small (balcony/windowsill)',
    'Medium (small yard/patio)',
    'Large (backyard garden)',
    'Very Large (farm/acreage)',
  ]

  const experienceLevels = [
    'Beginner (just starting)',
    'Intermediate (some experience)',
    'Advanced (experienced gardener)',
    'Expert (professional level)',
  ]

  const gardenTypes = [
    'Indoor (containers/houseplants)',
    'Outdoor containers/pots',
    'Raised beds',
    'In-ground garden',
    'Greenhouse',
    'Mixed (indoor and outdoor)',
  ]

  const soilTypes = [
    'Clay soil',
    'Sandy soil',
    'Loamy soil',
    'Silty soil',
    'Rocky soil',
    'Not sure',
  ]

  // Validation rules
  const rules = {
    required: (value: string) => !!value || 'This field is required',
  }

  // Methods
  async function getCropRecommendations () {
    if (!form.value?.validate()) return

    loading.value = true

    // Prepare user info string
    const userInfo = `
Location: ${formData.location}
Garden Size: ${formData.gardenSize}
Experience Level: ${formData.experience}
Garden Type: ${formData.gardenType}
Soil Type: ${formData.soilType || 'Unknown'}
Preferences: ${formData.preferences}
Additional Information: ${formData.additionalInfo}
  `.trim()

    try {
      const response = await fetch(apiUrl('crop-plan'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_info: userInfo,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get recommendations')
      }

      const data = await response.json()
      recommendations.value = data

      showSnackbar('Crop plan generated successfully!', 'success')
    } catch (error) {
      console.error('Error getting recommendations:', error)
      showSnackbar('Failed to generate crop plan. Please try again.', 'error')
    } finally {
      loading.value = false
    }
  }

  function saveRecommendations () {
    if (!recommendations.value) return

    const content = `OASIS CROP PLAN\n\nGenerated on: ${new Date().toLocaleDateString()}\n\nLocation: ${formData.location}\nGarden Size: ${formData.gardenSize}\nExperience: ${formData.experience}\n\n${recommendations.value.recommendations_text}`

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `oasis-crop-plan-${new Date().toISOString().split('T')[0]}.txt`
    document.body.append(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)

    showSnackbar('Crop plan saved successfully!', 'success')
  }

  async function shareRecommendations () {
    if (!recommendations.value) return

    const shareText = `Check out my personalized crop plan from Oasis! 🌱\n\n${recommendations.value.recommendations_text.slice(0, 200)}...`

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'My Oasis Crop Plan',
          text: shareText,
        })
        showSnackbar('Shared successfully!', 'success')
      } catch {
      // User cancelled sharing
      }
    } else {
      // Fallback: copy to clipboard
      try {
        await navigator.clipboard.writeText(shareText)
        showSnackbar('Copied to clipboard!', 'success')
      } catch {
        showSnackbar('Unable to share. Please copy manually.', 'warning')
      }
    }
  }

  function getCurrentSeason () {
    const month = new Date().getMonth()
    if (month >= 2 && month <= 4) return 'Spring'
    if (month >= 5 && month <= 7) return 'Summer'
    if (month >= 8 && month <= 10) return 'Fall'
    return 'Winter'
  }

  function showSnackbar (message: string, color: string) {
    snackbar.message = message
    snackbar.color = color
    snackbar.show = true
  }
</script>

<style scoped>
.crop-planner {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
</style>
