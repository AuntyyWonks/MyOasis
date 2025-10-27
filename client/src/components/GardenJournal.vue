<template>
  <v-container class="garden-journal pa-4" fluid>
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card class="mb-4" color="green-darken-1" rounded="lg">
          <v-card-text class="text-center py-6">
            <v-icon class="mb-2" color="white" size="48">mdi-book-open-variant</v-icon>
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
        <v-card elevation="2" rounded="lg" sticky>
          <v-card-title class="text-h6 font-weight-bold text-green-darken-1">
            <v-icon class="mr-2">mdi-plus-circle</v-icon>
            New Entry
          </v-card-title>

          <v-card-text>
            <v-form ref="form" v-model="valid">
              <!-- Entry Type -->
              <v-select
                v-model="newEntry.type"
                class="mb-3"
                :items="entryTypes"
                label="Entry Type"
                prepend-icon="mdi-tag"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Plant Name -->
              <v-text-field
                v-model="newEntry.plantName"
                class="mb-3"
                label="Plant Name"
                prepend-icon="mdi-leaf"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Title -->
              <v-text-field
                v-model="newEntry.title"
                class="mb-3"
                label="Entry Title"
                prepend-icon="mdi-format-title"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Notes -->
              <v-textarea
                v-model="newEntry.notes"
                class="mb-3"
                label="Notes & Observations"
                prepend-icon="mdi-note-text"
                rows="4"
                :rules="[rules.required]"
                variant="outlined"
              />

              <!-- Weather -->
              <v-text-field
                v-model="newEntry.weather"
                class="mb-3"
                hint="e.g., Sunny, 75°F, Light rain"
                label="Weather Conditions"
                persistent-hint
                prepend-icon="mdi-weather-partly-cloudy"
                variant="outlined"
              />

              <!-- Photo Upload -->
              <v-file-input
                v-model="newEntry.photos"
                accept="image/*"
                class="mb-3"
                label="Add Photos"
                multiple
                prepend-icon="mdi-camera"
                variant="outlined"
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
                        cover
                        height="80"
                        :src="preview"
                      />
                      <v-btn
                        class="remove-photo-btn"
                        color="red"
                        icon="mdi-close"
                        size="x-small"
                        @click="removePhoto(index)"
                      />
                    </v-card>
                  </v-col>
                </v-row>
              </div>

              <!-- Submit Button -->
              <v-btn
                block
                color="green-darken-1"
                :disabled="!valid"
                size="large"
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
        <v-card elevation="2" rounded="lg">
          <v-card-title class="d-flex align-center justify-space-between">
            <div class="text-h6 font-weight-bold text-green-darken-1">
              <v-icon class="mr-2">mdi-history</v-icon>
              Journal Entries ({{ filteredEntries.length }})
            </div>

            <!-- Filters -->
            <div class="d-flex align-center">
              <v-select
                v-model="filterType"
                class="mr-2"
                density="compact"
                :items="['All', ...entryTypes]"
                label="Filter by type"
                style="max-width: 150px;"
                variant="outlined"
              />
              <v-text-field
                v-model="searchQuery"
                clearable
                density="compact"
                label="Search"
                prepend-inner-icon="mdi-magnify"
                style="max-width: 200px;"
                variant="outlined"
              />
            </div>
          </v-card-title>

          <v-card-text>
            <!-- Empty State -->
            <div v-if="entries.length === 0" class="text-center py-8">
              <v-icon class="mb-4" color="grey-lighten-1" size="64">mdi-book-open-blank-variant</v-icon>
              <p class="text-body-1 text-grey-darken-1">
                Start your gardening journal by adding your first entry
              </p>
            </div>

            <!-- Timeline -->
            <v-timeline v-else align="start" side="end">
              <v-timeline-item
                v-for="(entry, index) in filteredEntries"
                :key="index"
                :dot-color="getEntryColor(entry.type)"
                size="small"
              >
                <template #icon>
                  <v-icon color="white" size="16">{{ getEntryIcon(entry.type) }}</v-icon>
                </template>

                <v-card class="mb-4" elevation="1" rounded="lg">
                  <v-card-title class="d-flex align-center justify-space-between">
                    <div>
                      <div class="text-h6 font-weight-bold">{{ entry.title }}</div>
                      <div class="text-subtitle-2 text-grey-darken-1">
                        {{ entry.plantName }} • {{ formatDate(entry.date) }}
                      </div>
                    </div>

                    <div class="d-flex align-center">
                      <v-chip
                        class="mr-2"
                        :color="getEntryColor(entry.type)"
                        size="small"
                        variant="tonal"
                      >
                        {{ entry.type }}
                      </v-chip>
                      <v-menu>
                        <template #activator="{ props }">
                          <v-btn
                            icon="mdi-dots-vertical"
                            size="small"
                            variant="text"
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
                      <v-icon class="mr-2" color="blue">mdi-weather-partly-cloudy</v-icon>
                      <span class="text-body-2">{{ entry.weather }}</span>
                    </div>

                    <!-- Photos -->
                    <div v-if="entry.photos && entry.photos.length > 0">
                      <v-row>
                        <v-col
                          v-for="(photo, photoIndex) in entry.photos"
                          :key="photoIndex"
                          cols="6"
                          md="3"
                          sm="4"
                        >
                          <v-card rounded="lg" @click="viewPhoto(photo)">
                            <v-img
                              class="cursor-pointer"
                              cover
                              height="100"
                              :src="photo"
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
            max-height="600"
            :src="selectedPhoto"
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
  import { computed, onMounted, reactive, ref } from 'vue'

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
    photos: [] as File[],
  })

  const snackbar = reactive({
    show: false,
    message: '',
    color: 'success',
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
    'Other',
  ]

  // Validation rules
  const rules = {
    required: (value: string) => !!value || 'This field is required',
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
        entry.title.toLowerCase().includes(query)
        || entry.plantName.toLowerCase().includes(query)
        || entry.notes.toLowerCase().includes(query),
      )
    }

    // Use non-mutating toSorted per lint rule
    return filtered.toSorted((a, b) => b.date.getTime() - a.date.getTime())
  })

  // Methods
  function handlePhotoUpload () {
    photoPreviews.value = []

    if (newEntry.photos) {
      for (const file of newEntry.photos) {
        const reader = new FileReader()
        reader.addEventListener('load', e => {
          photoPreviews.value.push(e.target?.result as string)
        })
        reader.readAsDataURL(file)
      }
    }
  }

  function removePhoto (index: number) {
    photoPreviews.value.splice(index, 1)
    if (newEntry.photos) {
      newEntry.photos.splice(index, 1)
    }
  }

  function addEntry () {
    if (!form.value?.validate()) return

    const entry: JournalEntry = {
      type: newEntry.type,
      plantName: newEntry.plantName,
      title: newEntry.title,
      notes: newEntry.notes,
      weather: newEntry.weather,
      photos: [...photoPreviews.value],
      date: new Date(),
    }

    entries.value.push(entry)
    saveEntries()
    resetForm()
    showSnackbar('Journal entry added successfully!', 'success')
  }

  function editEntry (entry: JournalEntry) {
    // Populate form with entry data for editing
    newEntry.type = entry.type
    newEntry.plantName = entry.plantName
    newEntry.title = entry.title
    newEntry.notes = entry.notes
    newEntry.weather = entry.weather
    photoPreviews.value = [...entry.photos]
  }

  function deleteEntry (index: number) {
    entries.value.splice(index, 1)
    saveEntries()
    showSnackbar('Entry deleted', 'info')
  }

  function resetForm () {
    newEntry.type = ''
    newEntry.plantName = ''
    newEntry.title = ''
    newEntry.notes = ''
    newEntry.weather = ''
    newEntry.photos = []
    photoPreviews.value = []
    form.value?.reset()
  }

  function viewPhoto (photo: string) {
    selectedPhoto.value = photo
    photoDialog.value = true
  }

  function getEntryColor (type: string) {
    const colors: Record<string, string> = {
      Planting: 'green',
      Watering: 'blue',
      Fertilizing: 'orange',
      Pruning: 'purple',
      Observation: 'teal',
      Harvest: 'amber',
      Problem: 'red',
      Treatment: 'pink',
      Progress: 'indigo',
      Other: 'grey',
    }
    return colors[type] || 'grey'
  }

  function getEntryIcon (type: string) {
    const icons: Record<string, string> = {
      Planting: 'mdi-seed',
      Watering: 'mdi-water',
      Fertilizing: 'mdi-nutrition',
      Pruning: 'mdi-content-cut',
      Observation: 'mdi-eye',
      Harvest: 'mdi-basket',
      Problem: 'mdi-alert',
      Treatment: 'mdi-medical-bag',
      Progress: 'mdi-trending-up',
      Other: 'mdi-note',
    }
    return icons[type] || 'mdi-note'
  }

  function formatDate (date: Date) {
    return date.toLocaleDateString([], {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  function showSnackbar (message: string, color: string) {
    snackbar.message = message
    snackbar.color = color
    snackbar.show = true
  }

  function saveEntries () {
    const entriesToSave = entries.value.map(entry => ({
      ...entry,
      date: entry.date.toISOString(),
    }))
    localStorage.setItem('oasis-journal-entries', JSON.stringify(entriesToSave))
  }

  function loadEntries () {
    const saved = localStorage.getItem('oasis-journal-entries')
    if (saved) {
      const parsed = JSON.parse(saved)
      entries.value = parsed.map((entry: any) => ({
        ...entry,
        date: new Date(entry.date),
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
