<template>
  <v-container class="plant-health pa-4" fluid>
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card class="mb-4" color="green-darken-1" rounded="lg">
          <v-card-text class="text-center py-6">
            <v-icon class="mb-2" color="white" size="48">mdi-medical-bag</v-icon>
            <h2 class="text-h4 font-weight-bold text-white mb-2">Plant Health Analyzer</h2>
            <p class="text-green-lighten-4 text-body-1">
              Upload photos of your plants to get instant health analysis and treatment recommendations
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Upload Section -->
      <v-col cols="12" md="6">
        <v-card elevation="2" min-height="400" rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-camera-plus</v-icon>
            Upload Plant Image
          </v-card-title>

          <v-card-text>
            <!-- Upload Area -->
            <div
              class="upload-area"
              :class="{ 'drag-over': isDragOver }"
              @click="triggerFileInput"
              @dragleave="isDragOver = false"
              @dragover.prevent="isDragOver = true"
              @drop="handleDrop"
            >
              <div v-if="!selectedImage" class="upload-content text-center">
                <v-icon class="mb-4" color="green-darken-1" size="64">mdi-cloud-upload</v-icon>
                <h3 class="text-h6 font-weight-bold mb-2">Upload Plant Photo</h3>
                <p class="text-body-2 text-grey-darken-1 mb-4">
                  Drag and drop an image here, or click to select
                </p>
                <v-btn color="green-darken-1" variant="outlined">
                  <v-icon class="mr-2">mdi-camera</v-icon>
                  Choose Image
                </v-btn>
              </div>

              <div v-else class="image-preview">
                <v-img
                  class="rounded-lg"
                  max-height="300"
                  :src="selectedImage"
                />
                <v-btn
                  class="remove-btn"
                  color="red"
                  icon="mdi-close"
                  size="small"
                  @click.stop="removeImage"
                />
              </div>
            </div>

            <!-- Upload Tips -->
            <v-alert
              class="mt-4"
              icon="mdi-lightbulb"
              type="info"
              variant="tonal"
            >
              <div class="text-body-2">
                <strong>Tips for better analysis:</strong>
                <ul class="mt-2">
                  <li>Take photos in good lighting</li>
                  <li>Focus on affected areas</li>
                  <li>Include leaves, stems, or flowers</li>
                  <li>Avoid blurry or dark images</li>
                </ul>
              </div>
            </v-alert>

            <!-- Analyze Button -->
            <v-btn
              v-if="selectedImage"
              block
              class="mt-4"
              color="green-darken-1"
              :loading="analyzing"
              size="large"
              @click="analyzeImage"
            >
              <v-icon class="mr-2">mdi-magnify</v-icon>
              Analyze Plant Health
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Results Section -->
      <v-col cols="12" md="6">
        <v-card elevation="2" min-height="400" rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-clipboard-text</v-icon>
            Analysis Results
          </v-card-title>

          <v-card-text>
            <!-- Loading State -->
            <div v-if="analyzing" class="text-center py-8">
              <v-progress-circular
                class="mb-4"
                color="green-darken-1"
                indeterminate
                size="64"
              />
              <p class="text-body-1">Analyzing your plant image...</p>
              <p class="text-body-2 text-grey-darken-1">This may take a few moments</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="!diagnosis" class="text-center py-8">
              <v-icon class="mb-4" color="grey-lighten-1" size="64">mdi-image-search</v-icon>
              <p class="text-body-1 text-grey-darken-1">
                Upload a plant image to get started with health analysis
              </p>
            </div>

            <!-- Results -->
            <div v-else>
              <!-- Health Status -->
              <v-card class="mb-4" color="grey-lighten-5" rounded="lg">
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon class="mr-2" :color="getHealthColor()" size="24">
                      {{ getHealthIcon() }}
                    </v-icon>
                    <span class="text-h6 font-weight-bold">Plant Health Status</span>
                  </div>
                  <v-chip
                    :color="getHealthColor()"
                    size="small"
                    variant="tonal"
                  >
                    {{ getHealthStatus() }}
                  </v-chip>
                </v-card-text>
              </v-card>

              <!-- Diagnosis Text -->
              <v-card class="mb-4" color="white" rounded="lg">
                <v-card-title class="text-subtitle-1 font-weight-bold">
                  Detailed Analysis
                </v-card-title>
                <v-card-text>
                  <div class="text-body-2" style="white-space: pre-line;">
                    {{ diagnosis }}
                  </div>
                </v-card-text>
              </v-card>

              <!-- Action Buttons -->
              <v-row>
                <v-col cols="6">
                  <v-btn
                    block
                    color="green-darken-1"
                    variant="outlined"
                    @click="saveAnalysis"
                  >
                    <v-icon class="mr-2">mdi-content-save</v-icon>
                    Save
                  </v-btn>
                </v-col>
                <v-col cols="6">
                  <v-btn
                    block
                    color="blue-darken-1"
                    variant="outlined"
                    @click="shareAnalysis"
                  >
                    <v-icon class="mr-2">mdi-share</v-icon>
                    Share
                  </v-btn>
                </v-col>
              </v-row>

              <!-- New Analysis Button -->
              <v-btn
                block
                class="mt-2"
                color="green-darken-1"
                variant="text"
                @click="startNewAnalysis"
              >
                <v-icon class="mr-2">mdi-plus</v-icon>
                Analyze Another Image
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Analyses -->
    <v-row v-if="recentAnalyses.length > 0" class="mt-4">
      <v-col cols="12">
        <v-card elevation="2" rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-history</v-icon>
            Recent Analyses
          </v-card-title>

          <v-card-text>
            <v-row>
              <v-col
                v-for="(analysis, index) in recentAnalyses"
                :key="index"
                cols="12"
                md="4"
                sm="6"
              >
                <v-card
                  class="analysis-card"
                  elevation="1"
                  rounded="lg"
                  @click="viewAnalysis(analysis)"
                >
                  <v-img
                    cover
                    height="120"
                    :src="analysis.image"
                  />
                  <v-card-text class="pa-2">
                    <div class="text-caption text-grey-darken-1">
                      {{ formatDate(analysis.date) }}
                    </div>
                    <div class="text-body-2 font-weight-medium">
                      {{ analysis.summary }}
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Hidden File Input -->
    <input
      ref="fileInput"
      accept="image/*"
      style="display: none"
      type="file"
      @change="handleFileSelect"
    >

    <!-- Snackbar -->
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
  import { onMounted, reactive, ref } from 'vue'
  import { apiUrl } from '@/utils/api'

  interface Analysis {
    image: string
    diagnosis: string
    date: Date
    summary: string
  }

  // Reactive data
  const selectedImage = ref<string | null>(null)
  const selectedFile = ref<File | null>(null)
  const analyzing = ref(false)
  const diagnosis = ref<string | null>(null)
  const isDragOver = ref(false)
  const fileInput = ref<HTMLInputElement | null>(null)
  const recentAnalyses = ref<Analysis[]>([])

  const snackbar = reactive({
    show: false,
    message: '',
    color: 'success',
  })

  // Methods
  function triggerFileInput () {
    fileInput.value?.click()
  }

  function handleFileSelect (event: Event) {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0]
    if (file) {
      processFile(file)
    }
  }

  function handleDrop (event: DragEvent) {
    event.preventDefault()
    isDragOver.value = false

    const files = event.dataTransfer?.files
    if (files && files.length > 0) {
      processFile(files[0]!)
    }
  }

  function processFile (file: File) {
    if (!file.type.startsWith('image/')) {
      showSnackbar('Please select an image file', 'error')
      return
    }

    selectedFile.value = file
    const reader = new FileReader()
    reader.addEventListener('load', e => {
      selectedImage.value = e.target?.result as string
    })
    reader.readAsDataURL(file)
  }

  function removeImage () {
    selectedImage.value = null
    selectedFile.value = null
    diagnosis.value = null
  }

  async function analyzeImage () {
    if (!selectedFile.value) return

    analyzing.value = true

    try {
      const formData = new FormData()
      formData.append('file', selectedFile.value)

      const response = await fetch(apiUrl('plant-health'), {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to analyze image')
      }

      const data = await response.json()
      diagnosis.value = data.diagnosis

      // Save to recent analyses
      const analysis: Analysis = {
        image: selectedImage.value!,
        diagnosis: data.diagnosis,
        date: new Date(),
        summary: data.diagnosis.slice(0, 50) + '...',
      }

      recentAnalyses.value.unshift(analysis)
      if (recentAnalyses.value.length > 6) {
        recentAnalyses.value = recentAnalyses.value.slice(0, 6)
      }

      saveRecentAnalyses()
      showSnackbar('Analysis completed successfully!', 'success')
    } catch (error) {
      console.error('Error analyzing image:', error)
      showSnackbar('Failed to analyze image. Please try again.', 'error')
    } finally {
      analyzing.value = false
    }
  }

  function getHealthStatus () {
    if (!diagnosis.value) return 'Unknown'

    const text = diagnosis.value.toLowerCase()
    if (text.includes('healthy') || text.includes('good')) return 'Healthy'
    if (text.includes('disease') || text.includes('pest') || text.includes('problem')) return 'Needs Attention'
    if (text.includes('dying') || text.includes('severe')) return 'Critical'
    return 'Needs Assessment'
  }

  function getHealthColor () {
    const status = getHealthStatus()
    switch (status) {
      case 'Healthy': { return 'green'
      }
      case 'Needs Attention': { return 'orange'
      }
      case 'Critical': { return 'red'
      }
      default: { return 'grey'
      }
    }
  }

  function getHealthIcon () {
    const status = getHealthStatus()
    switch (status) {
      case 'Healthy': { return 'mdi-check-circle'
      }
      case 'Needs Attention': { return 'mdi-alert-circle'
      }
      case 'Critical': { return 'mdi-close-circle'
      }
      default: { return 'mdi-help-circle'
      }
    }
  }

  function saveAnalysis () {
    if (!diagnosis.value || !selectedImage.value) return

    const content = `OASIS PLANT HEALTH ANALYSIS\n\nDate: ${new Date().toLocaleDateString()}\n\nDiagnosis:\n${diagnosis.value}`

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `plant-analysis-${new Date().toISOString().split('T')[0]}.txt`
    document.body.append(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)

    showSnackbar('Analysis saved successfully!', 'success')
  }

  async function shareAnalysis () {
    if (!diagnosis.value) return

    const shareText = `Plant health analysis from Oasis 🌱\n\n${diagnosis.value.slice(0, 200)}...`

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Plant Health Analysis',
          text: shareText,
        })
        showSnackbar('Shared successfully!', 'success')
      } catch {
      // User cancelled sharing
      }
    } else {
      try {
        await navigator.clipboard.writeText(shareText)
        showSnackbar('Copied to clipboard!', 'success')
      } catch {
        showSnackbar('Unable to share. Please copy manually.', 'warning')
      }
    }
  }

  function startNewAnalysis () {
    removeImage()
  }

  function viewAnalysis (analysis: Analysis) {
    selectedImage.value = analysis.image
    diagnosis.value = analysis.diagnosis
  }

  function formatDate (date: Date) {
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
  }

  function showSnackbar (message: string, color: string) {
    snackbar.message = message
    snackbar.color = color
    snackbar.show = true
  }

  function saveRecentAnalyses () {
    const analysesToSave = recentAnalyses.value.map(analysis => ({
      ...analysis,
      date: analysis.date.toISOString(),
    }))
    localStorage.setItem('oasis-recent-analyses', JSON.stringify(analysesToSave))
  }

  function loadRecentAnalyses () {
    const saved = localStorage.getItem('oasis-recent-analyses')
    if (saved) {
      const parsed = JSON.parse(saved)
      recentAnalyses.value = parsed.map((analysis: any) => ({
        ...analysis,
        date: new Date(analysis.date),
      }))
    }
  }

  // Lifecycle
  onMounted(() => {
    loadRecentAnalyses()
  })
</script>

<style scoped>
.plant-health {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: #4caf50;
  background-color: #f8f9fa;
}

.upload-area.drag-over {
  border-color: #4caf50;
  background-color: #e8f5e8;
}

.image-preview {
  position: relative;
  width: 100%;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
}

.analysis-card {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.analysis-card:hover {
  transform: translateY(-2px);
}
</style>
