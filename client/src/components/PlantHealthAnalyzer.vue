<template>
  <v-container fluid class="plant-health pa-4">
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card color="green-darken-1" class="mb-4" rounded="lg">
          <v-card-text class="text-center py-6">
            <v-icon color="white" size="48" class="mb-2">mdi-medical-bag</v-icon>
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
        <v-card rounded="lg" elevation="2" min-height="400">
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-camera-plus</v-icon>
            Upload Plant Image
          </v-card-title>
          
          <v-card-text>
            <!-- Upload Area -->
            <div
              class="upload-area"
              :class="{ 'drag-over': isDragOver }"
              @drop="handleDrop"
              @dragover.prevent="isDragOver = true"
              @dragleave="isDragOver = false"
              @click="triggerFileInput"
            >
              <div v-if="!selectedImage" class="upload-content text-center">
                <v-icon color="green-darken-1" size="64" class="mb-4">mdi-cloud-upload</v-icon>
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
                  :src="selectedImage"
                  max-height="300"
                  class="rounded-lg"
                />
                <v-btn
                  icon="mdi-close"
                  color="red"
                  size="small"
                  class="remove-btn"
                  @click.stop="removeImage"
                />
              </div>
            </div>

            <!-- Upload Tips -->
            <v-alert
              type="info"
              variant="tonal"
              class="mt-4"
              icon="mdi-lightbulb"
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
              color="green-darken-1"
              size="large"
              block
              class="mt-4"
              :loading="analyzing"
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
        <v-card rounded="lg" elevation="2" min-height="400">
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-clipboard-text</v-icon>
            Analysis Results
          </v-card-title>
          
          <v-card-text>
            <!-- Loading State -->
            <div v-if="analyzing" class="text-center py-8">
              <v-progress-circular
                color="green-darken-1"
                indeterminate
                size="64"
                class="mb-4"
              />
              <p class="text-body-1">Analyzing your plant image...</p>
              <p class="text-body-2 text-grey-darken-1">This may take a few moments</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="!diagnosis" class="text-center py-8">
              <v-icon color="grey-lighten-1" size="64" class="mb-4">mdi-image-search</v-icon>
              <p class="text-body-1 text-grey-darken-1">
                Upload a plant image to get started with health analysis
              </p>
            </div>

            <!-- Results -->
            <div v-else>
              <!-- Health Status -->
              <v-card color="grey-lighten-5" class="mb-4" rounded="lg">
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon :color="getHealthColor()" size="24" class="mr-2">
                      {{ getHealthIcon() }}
                    </v-icon>
                    <span class="text-h6 font-weight-bold">Plant Health Status</span>
                  </div>
                  <v-chip
                    :color="getHealthColor()"
                    variant="tonal"
                    size="small"
                  >
                    {{ getHealthStatus() }}
                  </v-chip>
                </v-card-text>
              </v-card>

              <!-- Diagnosis Text -->
              <v-card color="white" class="mb-4" rounded="lg">
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
                    color="green-darken-1"
                    variant="outlined"
                    block
                    @click="saveAnalysis"
                  >
                    <v-icon class="mr-2">mdi-content-save</v-icon>
                    Save
                  </v-btn>
                </v-col>
                <v-col cols="6">
                  <v-btn
                    color="blue-darken-1"
                    variant="outlined"
                    block
                    @click="shareAnalysis"
                  >
                    <v-icon class="mr-2">mdi-share</v-icon>
                    Share
                  </v-btn>
                </v-col>
              </v-row>

              <!-- New Analysis Button -->
              <v-btn
                color="green-darken-1"
                variant="text"
                block
                class="mt-2"
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
        <v-card rounded="lg" elevation="2">
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
                sm="6"
                md="4"
              >
                <v-card
                  class="analysis-card"
                  rounded="lg"
                  elevation="1"
                  @click="viewAnalysis(analysis)"
                >
                  <v-img
                    :src="analysis.image"
                    height="120"
                    cover
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
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleFileSelect"
    />

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
import { ref, reactive, onMounted } from 'vue'

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
const fileInput = ref<HTMLInputElement>()
const recentAnalyses = ref<Analysis[]>([])

const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

// Methods
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    processFile(file)
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = false
  
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    processFile(files[0])
  }
}

const processFile = (file: File) => {
  if (!file.type.startsWith('image/')) {
    showSnackbar('Please select an image file', 'error')
    return
  }

  selectedFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    selectedImage.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const removeImage = () => {
  selectedImage.value = null
  selectedFile.value = null
  diagnosis.value = null
}

const analyzeImage = async () => {
  if (!selectedFile.value) return

  analyzing.value = true

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await fetch('http://127.0.0.1:5000/plant-health', {
      method: 'POST',
      body: formData
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
      summary: data.diagnosis.substring(0, 50) + '...'
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

const getHealthStatus = () => {
  if (!diagnosis.value) return 'Unknown'
  
  const text = diagnosis.value.toLowerCase()
  if (text.includes('healthy') || text.includes('good')) return 'Healthy'
  if (text.includes('disease') || text.includes('pest') || text.includes('problem')) return 'Needs Attention'
  if (text.includes('dying') || text.includes('severe')) return 'Critical'
  return 'Needs Assessment'
}

const getHealthColor = () => {
  const status = getHealthStatus()
  switch (status) {
    case 'Healthy': return 'green'
    case 'Needs Attention': return 'orange'
    case 'Critical': return 'red'
    default: return 'grey'
  }
}

const getHealthIcon = () => {
  const status = getHealthStatus()
  switch (status) {
    case 'Healthy': return 'mdi-check-circle'
    case 'Needs Attention': return 'mdi-alert-circle'
    case 'Critical': return 'mdi-close-circle'
    default: return 'mdi-help-circle'
  }
}

const saveAnalysis = () => {
  if (!diagnosis.value || !selectedImage.value) return

  const content = `OASIS PLANT HEALTH ANALYSIS\n\nDate: ${new Date().toLocaleDateString()}\n\nDiagnosis:\n${diagnosis.value}`
  
  const blob = new Blob([content], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `plant-analysis-${new Date().toISOString().split('T')[0]}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  showSnackbar('Analysis saved successfully!', 'success')
}

const shareAnalysis = async () => {
  if (!diagnosis.value) return

  const shareText = `Plant health analysis from Oasis 🌱\n\n${diagnosis.value.substring(0, 200)}...`
  
  if (navigator.share) {
    try {
      await navigator.share({
        title: 'Plant Health Analysis',
        text: shareText
      })
      showSnackbar('Shared successfully!', 'success')
    } catch (error) {
      // User cancelled sharing
    }
  } else {
    try {
      await navigator.clipboard.writeText(shareText)
      showSnackbar('Copied to clipboard!', 'success')
    } catch (error) {
      showSnackbar('Unable to share. Please copy manually.', 'warning')
    }
  }
}

const startNewAnalysis = () => {
  removeImage()
}

const viewAnalysis = (analysis: Analysis) => {
  selectedImage.value = analysis.image
  diagnosis.value = analysis.diagnosis
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
}

const showSnackbar = (message: string, color: string) => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

const saveRecentAnalyses = () => {
  const analysesToSave = recentAnalyses.value.map(analysis => ({
    ...analysis,
    date: analysis.date.toISOString()
  }))
  localStorage.setItem('oasis-recent-analyses', JSON.stringify(analysesToSave))
}

const loadRecentAnalyses = () => {
  const saved = localStorage.getItem('oasis-recent-analyses')
  if (saved) {
    const parsed = JSON.parse(saved)
    recentAnalyses.value = parsed.map((analysis: any) => ({
      ...analysis,
      date: new Date(analysis.date)
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