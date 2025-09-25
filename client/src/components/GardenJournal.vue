<template>
  <v-container fluid class="garden-journal pa-4">
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card color="green-darken-1" class="mb-4" rounded="lg">
          <v-card-text class="text-center py-6">
            <v-icon color="white" size="48" class="mb-2">mdi-book-open-variant</v-icon>
            <h2 class="text-h4 font-weight-bold text-white mb-2">Garden Journal</h2>
            <p class="text-green-lighten-4 text-body-1">
              Track your gardening journey, record observations, and monitor plant progress
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Add Entry Form -->
      <v-col cols="12" md="4">
        <v-card rounded="lg" elevation="2" sticky>
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-plus-circle</v-icon>
            New Entry
          </v-card-title>
          
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <!-- Entry Type -->
              <v-select
                v-model="newEntry.type"
                label="Entry Type"
                prepend-icon="mdi-tag"
                variant="outlined"
                :items="entryTypes"
                :rules="[rules.required]"
                class="mb-3"
              />

              <!-- Plant Name -->
              <v-text-field
                v-model="newEntry.plantName"
                label="Plant Name"
                prepend-icon="mdi-leaf"
                variant="outlined"
                :rules="[rules.required]"
                class="mb-3"
              />

              <!-- Title -->
              <v-text-field
                v-model="newEntry.title"
                label="Entry Title"
                prepend-icon="mdi-format-title"
                variant="outlined"
                :rules="[rules.required]"
                class="mb-3"
              />

              <!-- Notes -->
              <v-textarea
                v-model="newEntry.notes"
                label="Notes & Observations"
                prepend-icon="mdi-note-text"
                variant="outlined"
                rows="4"
                :rules="[rules.required]"
                class="mb-3"
              />

              <!-- Weather -->
              <v-text-field
                v-model="newEntry.weather"
                label="Weather Conditions"
                prepend-icon="mdi-weather-partly-cloudy"
                variant="outlined"
                class="mb-3"
                hint="e.g., Sunny, 75°F, Light rain"
                persistent-hint
              />

              <!-- Photo Upload -->
              <v-file-input
                v-model="newEntry.photos"
                label="Add Photos"
                prepend-icon="mdi-camera"
                variant="outlined"
                multiple
                accept="image/*"
                class="mb-3"
                @change="handlePhotoUpload"
              />

              <!-- Photo Previews -->
              <div v-if="photoPreviews.length > 0" class="mb-3">
                <v-row>
                  <v-col
                    v-for="(preview, index) in photoPreviews"
                    :key="index"
                    cols="6"
                  >
                    <v-card rounded="lg">
                      <v-img
                        :src="preview"
                        height="80"
                        cover
                      />
                      <v-btn
                        icon="mdi-close"
                        color="red"
                        size="x-small"
                        class="remove-photo-btn"
                        @click="removePhoto(index)"
                      />
                    </v-card>
                  </v-col>
                </v-row>
              </div>

              <!-- Submit Button -->
              <v-btn
                color="green-darken-1"
                size="large"
                block
                :disabled="!valid"
                @click="addEntry"
              >
                <v-icon class="mr-2">mdi-content-save</v-icon>
                Save Entry
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Journal Entries -->
      <v-col cols="12" md="8">
        <v-card rounded="lg" elevation="2">
          <v-card-title class="d-flex align-center justify-space-between">
            <div class="text-h6 font-weight-bold text-green-darken-1">
              <v-icon class="mr-2">mdi-history</v-icon>
              Journal Entries ({{ filteredEntries.length }})
            </div>
            
            <!-- Filters -->
            <div class="d-flex align-center">
              <v-select
                v-model="filterType"
                label="Filter by type"
                variant="outlined"
                density="compact"
                :items="['All', ...entryTypes]"
                class="mr-2"
                style="max-width: 150px;"
              />
              <v-text-field
                v-model="searchQuery"
                label="Search"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                style="max-width: 200px;"
                clearable
              />
            </div>
          </v-card-title>
          
          <v-card-text>
            <!-- Empty State -->
            <div v-if="entries.length === 0" class="text-center py-8">
              <v-icon color="grey-lighten-1" size="64" class="mb-4">mdi-book-open-blank-variant</v-icon>
              <p class="text-body-1 text-grey-darken-1">
                Start your gardening journal by adding your first entry
              </p>
            </div>

            <!-- Timeline -->
            <v-timeline v-else side="end" align="start">
              <v-timeline-item
                v-for="(entry, index) in filteredEntries"
                :key="index"
                :dot-color="getEntryColor(entry.type)"
                size="small"
              >
                <template #icon>
                  <v-icon color="white" size="16">{{ getEntryIcon(entry.type) }}</v-icon>
                </template>

                <v-card rounded="lg" elevation="1" class="mb-4">
                  <v-card-title class="d-flex align-center justify-space-between">
                    <div>
                      <div class="text-h6 font-weight-bold">{{ entry.title }}</div>
                      <div class="text-subtitle-2 text-grey-darken-1">
                        {{ entry.plantName }} • {{ formatDate(entry.date) }}
                      </div>
                    </div>
                    
                    <div class="d-flex align-center">
                      <v-chip
                        :color="getEntryColor(entry.type)"
                        variant="tonal"
                        size="small"
                        class="mr-2"
                      >
                        {{ entry.type }}
                      </v-chip>
                      <v-menu>
                        <template #activator="{ props }">
                          <v-btn
                            icon="mdi-dots-vertical"
                            variant="text"
                            size="small"
                            v-bind="props"
                          />
                        </template>
                        <v-list>
                          <v-list-item @click="editEntry(entry)">
                            <v-list-item-title>
                              <v-icon class="mr-2">mdi-pencil</v-icon>
                              Edit
                            </v-list-item-title>
                          </v-list-item>
                          <v-list-item @click="deleteEntry(index)">
                            <v-list-item-title>
                              <v-icon class="mr-2">mdi-delete</v-icon>
                              Delete
                            </v-list-item-title>
                          </v-list-item>
                        </v-list>
                      </v-menu>
                    </div>
                  </v-card-title>
                  
                  <v-card-text>
                    <p class="text-body-2 mb-3">{{ entry.notes }}</p>
                    
                    <div v-if="entry.weather" class="d-flex align-center mb-3">
                      <v-icon color="blue" class="mr-2">mdi-weather-partly-cloudy</v-icon>
                      <span class="text-body-2">{{ entry.weather }}</span>
                    </div>

                    <!-- Photos -->
                    <div v-if="entry.photos && entry.photos.length > 0">
                      <v-row>
                        <v-col
                          v-for="(photo, photoIndex) in entry.photos"
                          :key="photoIndex"
                          cols="6"
                          sm="4"
                          md="3"
                        >
                          <v-card rounded="lg" @click="viewPhoto(photo)">
                            <v-img
                              :src="photo"
                              height="100"
                              cover
                              class="cursor-pointer"
                            />
                          </v-card>
                        </v-col>
                      </v-row>
                    </div>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Photo Viewer Dialog -->
    <v-dialog v-model="photoDialog" max-width="800">
      <v-card>
        <v-card-text class="pa-0">
          <v-img
            v-if="selectedPhoto"
            :src="selectedPhoto"
            max-height="600"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="green-darken-1" @click="photoDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
import { ref, reactive, computed, onMounted } from 'vue'

interface JournalEntry {
  type: string
  plantName: string
  title: string
  notes: string
  weather: string
  photos: string[]
  date: Date
}

// Reactive data
const valid = ref(false)
const form = ref()
const entries = ref<JournalEntry[]>([])
const photoPreviews = ref<string[]>([])
const filterType = ref('All')
const searchQuery = ref('')
const photoDialog = ref(false)
const selectedPhoto = ref<string | null>(null)

const newEntry = reactive({
  type: '',
  plantName: '',
  title: '',
  notes: '',
  weather: '',
  photos: [] as File[]
})

const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

// Entry types
const entryTypes = [
  'Planting',
  'Watering',
  'Fertilizing',
  'Pruning',
  'Observation',
  'Harvest',
  'Problem',
  'Treatment',
  'Progress',
  'Other'
]

// Validation rules
const rules = {
  required: (value: string) => !!value || 'This field is required'
}

// Computed
const filteredEntries = computed(() => {
  let filtered = entries.value

  if (filterType.value !== 'All') {
    filtered = filtered.filter(entry => entry.type === filterType.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(entry =>
      entry.title.toLowerCase().includes(query) ||
      entry.plantName.toLowerCase().includes(query) ||
      entry.notes.toLowerCase().includes(query)
    )
  }

  return filtered.sort((a, b) => b.date.getTime() - a.date.getTime())
})

// Methods
const handlePhotoUpload = () => {
  photoPreviews.value = []
  
  if (newEntry.photos) {
    newEntry.photos.forEach(file => {
      const reader = new FileReader()
      reader.onload = (e) => {
        photoPreviews.value.push(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    })
  }
}

const removePhoto = (index: number) => {
  photoPreviews.value.splice(index, 1)
  if (newEntry.photos) {
    newEntry.photos.splice(index, 1)
  }
}

const addEntry = () => {
  if (!form.value?.validate()) return

  const entry: JournalEntry = {
    type: newEntry.type,
    plantName: newEntry.plantName,
    title: newEntry.title,
    notes: newEntry.notes,
    weather: newEntry.weather,
    photos: [...photoPreviews.value],
    date: new Date()
  }

  entries.value.push(entry)
  saveEntries()
  resetForm()
  showSnackbar('Journal entry added successfully!', 'success')
}

const editEntry = (entry: JournalEntry) => {
  // Populate form with entry data for editing
  newEntry.type = entry.type
  newEntry.plantName = entry.plantName
  newEntry.title = entry.title
  newEntry.notes = entry.notes
  newEntry.weather = entry.weather
  photoPreviews.value = [...entry.photos]
}

const deleteEntry = (index: number) => {
  entries.value.splice(index, 1)
  saveEntries()
  showSnackbar('Entry deleted', 'info')
}

const resetForm = () => {
  newEntry.type = ''
  newEntry.plantName = ''
  newEntry.title = ''
  newEntry.notes = ''
  newEntry.weather = ''
  newEntry.photos = []
  photoPreviews.value = []
  form.value?.reset()
}

const viewPhoto = (photo: string) => {
  selectedPhoto.value = photo
  photoDialog.value = true
}

const getEntryColor = (type: string) => {
  const colors: Record<string, string> = {
    'Planting': 'green',
    'Watering': 'blue',
    'Fertilizing': 'orange',
    'Pruning': 'purple',
    'Observation': 'teal',
    'Harvest': 'amber',
    'Problem': 'red',
    'Treatment': 'pink',
    'Progress': 'indigo',
    'Other': 'grey'
  }
  return colors[type] || 'grey'
}

const getEntryIcon = (type: string) => {
  const icons: Record<string, string> = {
    'Planting': 'mdi-seed',
    'Watering': 'mdi-water',
    'Fertilizing': 'mdi-nutrition',
    'Pruning': 'mdi-content-cut',
    'Observation': 'mdi-eye',
    'Harvest': 'mdi-basket',
    'Problem': 'mdi-alert',
    'Treatment': 'mdi-medical-bag',
    'Progress': 'mdi-trending-up',
    'Other': 'mdi-note'
  }
  return icons[type] || 'mdi-note'
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString([], {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const showSnackbar = (message: string, color: string) => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

const saveEntries = () => {
  const entriesToSave = entries.value.map(entry => ({
    ...entry,
    date: entry.date.toISOString()
  }))
  localStorage.setItem('oasis-journal-entries', JSON.stringify(entriesToSave))
}

const loadEntries = () => {
  const saved = localStorage.getItem('oasis-journal-entries')
  if (saved) {
    const parsed = JSON.parse(saved)
    entries.value = parsed.map((entry: any) => ({
      ...entry,
      date: new Date(entry.date)
    }))
  }
}

// Lifecycle
onMounted(() => {
  loadEntries()
})
</script>

<style scoped>
.garden-journal {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.remove-photo-btn {
  position: absolute;
  top: 4px;
  right: 4px;
}

.cursor-pointer {
  cursor: pointer;
}
</style>