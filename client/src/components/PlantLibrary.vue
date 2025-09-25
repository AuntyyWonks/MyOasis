<template>
  <v-container fluid class="plant-library pa-4">
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card color="green-darken-1" class="mb-4" rounded="lg">
          <v-card-text class="text-center py-6">
            <v-icon color="white" size="48" class="mb-2">mdi-library</v-icon>
            <h2 class="text-h4 font-weight-bold text-white mb-2">Plant Library</h2>
            <p class="text-green-lighten-4 text-body-1">
              Discover and learn about different plants, their care requirements, and growing tips
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Search and Filters -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          label="Search plants..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          @input="searchPlants"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-row>
          <v-col cols="6">
            <v-select
              v-model="selectedCategory"
              label="Category"
              variant="outlined"
              :items="categories"
              clearable
              @update:model-value="filterPlants"
            />
          </v-col>
          <v-col cols="6">
            <v-select
              v-model="selectedDifficulty"
              label="Care Level"
              variant="outlined"
              :items="difficultyLevels"
              clearable
              @update:model-value="filterPlants"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- Quick Categories -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card rounded="lg" elevation="1">
          <v-card-text>
            <div class="text-subtitle-1 font-weight-bold mb-3">Popular Categories</div>
            <v-chip-group
              v-model="selectedCategoryChip"
              color="green-darken-1"
              @update:model-value="handleCategoryChip"
            >
              <v-chip
                v-for="category in popularCategories"
                :key="category.name"
                :prepend-icon="category.icon"
                variant="outlined"
              >
                {{ category.name }}
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <v-progress-circular
        color="green-darken-1"
        indeterminate
        size="64"
        class="mb-4"
      />
      <p class="text-body-1">Loading plant library...</p>
    </div>

    <!-- Plant Grid -->
    <v-row v-else>
      <v-col
        v-for="plant in filteredPlants"
        :key="plant.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card
          class="plant-card"
          rounded="lg"
          elevation="2"
          @click="viewPlantDetails(plant)"
        >
          <v-img
            :src="plant.image"
            height="200"
            cover
          >
            <template #placeholder>
              <div class="d-flex align-center justify-center fill-height">
                <v-icon color="grey-lighten-2" size="64">mdi-leaf</v-icon>
              </div>
            </template>
          </v-img>
          
          <v-card-title class="text-h6">{{ plant.name }}</v-card-title>
          <v-card-subtitle>{{ plant.scientificName }}</v-card-subtitle>
          
          <v-card-text>
            <div class="d-flex align-center mb-2">
              <v-icon :color="getDifficultyColor(plant.difficulty)" class="mr-2">
                {{ getDifficultyIcon(plant.difficulty) }}
              </v-icon>
              <span class="text-body-2">{{ plant.difficulty }}</span>
            </div>
            
            <div class="d-flex align-center mb-2">
              <v-icon color="blue" class="mr-2">mdi-water</v-icon>
              <span class="text-body-2">{{ plant.watering }}</span>
            </div>
            
            <div class="d-flex align-center">
              <v-icon color="orange" class="mr-2">mdi-white-balance-sunny</v-icon>
              <span class="text-body-2">{{ plant.light }}</span>
            </div>
          </v-card-text>
          
          <v-card-actions>
            <v-chip
              :color="getCategoryColor(plant.category)"
              variant="tonal"
              size="small"
            >
              {{ plant.category }}
            </v-chip>
            <v-spacer />
            <v-btn
              icon="mdi-heart-outline"
              variant="text"
              size="small"
              @click.stop="toggleFavorite(plant)"
            />
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <div v-if="!loading && filteredPlants.length === 0" class="text-center py-8">
      <v-icon color="grey-lighten-1" size="64" class="mb-4">mdi-magnify</v-icon>
      <p class="text-body-1 text-grey-darken-1">
        No plants found matching your criteria
      </p>
      <v-btn color="green-darken-1" variant="outlined" @click="clearFilters">
        Clear Filters
      </v-btn>
    </div>

    <!-- Plant Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="800" scrollable>
      <v-card v-if="selectedPlant">
        <v-img
          :src="selectedPlant.image"
          height="300"
          cover
        />
        
        <v-card-title class="text-h5">
          {{ selectedPlant.name }}
          <v-spacer />
          <v-btn
            icon="mdi-close"
            variant="text"
            @click="detailsDialog = false"
          />
        </v-card-title>
        
        <v-card-subtitle>{{ selectedPlant.scientificName }}</v-card-subtitle>
        
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <h3 class="text-h6 font-weight-bold mb-3">Care Information</h3>
              
              <div class="mb-3">
                <div class="d-flex align-center mb-1">
                  <v-icon :color="getDifficultyColor(selectedPlant.difficulty)" class="mr-2">
                    {{ getDifficultyIcon(selectedPlant.difficulty) }}
                  </v-icon>
                  <strong>Difficulty:</strong>
                </div>
                <p class="text-body-2 ml-8">{{ selectedPlant.difficulty }}</p>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center mb-1">
                  <v-icon color="blue" class="mr-2">mdi-water</v-icon>
                  <strong>Watering:</strong>
                </div>
                <p class="text-body-2 ml-8">{{ selectedPlant.watering }}</p>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center mb-1">
                  <v-icon color="orange" class="mr-2">mdi-white-balance-sunny</v-icon>
                  <strong>Light Requirements:</strong>
                </div>
                <p class="text-body-2 ml-8">{{ selectedPlant.light }}</p>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center mb-1">
                  <v-icon color="green" class="mr-2">mdi-thermometer</v-icon>
                  <strong>Temperature:</strong>
                </div>
                <p class="text-body-2 ml-8">{{ selectedPlant.temperature }}</p>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center mb-1">
                  <v-icon color="brown" class="mr-2">mdi-earth</v-icon>
                  <strong>Soil:</strong>
                </div>
                <p class="text-body-2 ml-8">{{ selectedPlant.soil }}</p>
              </div>
            </v-col>
            
            <v-col cols="12" md="6">
              <h3 class="text-h6 font-weight-bold mb-3">Description</h3>
              <p class="text-body-2 mb-4">{{ selectedPlant.description }}</p>
              
              <h3 class="text-h6 font-weight-bold mb-3">Care Tips</h3>
              <ul class="text-body-2">
                <li v-for="tip in selectedPlant.tips" :key="tip" class="mb-1">
                  {{ tip }}
                </li>
              </ul>
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-card-actions>
          <v-chip
            :color="getCategoryColor(selectedPlant.category)"
            variant="tonal"
          >
            {{ selectedPlant.category }}
          </v-chip>
          <v-spacer />
          <v-btn
            color="green-darken-1"
            variant="outlined"
            @click="addToMyPlants(selectedPlant)"
          >
            <v-icon class="mr-2">mdi-plus</v-icon>
            Add to My Plants
          </v-btn>
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

interface Plant {
  id: number
  name: string
  scientificName: string
  category: string
  difficulty: string
  watering: string
  light: string
  temperature: string
  soil: string
  description: string
  tips: string[]
  image: string
  isFavorite?: boolean
}

// Reactive data
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedDifficulty = ref('')
const selectedCategoryChip = ref()
const detailsDialog = ref(false)
const selectedPlant = ref<Plant | null>(null)
const plants = ref<Plant[]>([])
const filteredPlants = ref<Plant[]>([])

const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

// Categories and filters
const categories = [
  'Houseplants',
  'Succulents',
  'Herbs',
  'Vegetables',
  'Flowers',
  'Trees',
  'Shrubs',
  'Ferns',
  'Cacti',
  'Vines'
]

const difficultyLevels = [
  'Easy',
  'Moderate',
  'Challenging',
  'Expert'
]

const popularCategories = [
  { name: 'Houseplants', icon: 'mdi-home-variant' },
  { name: 'Succulents', icon: 'mdi-cactus' },
  { name: 'Herbs', icon: 'mdi-leaf' },
  { name: 'Vegetables', icon: 'mdi-carrot' },
  { name: 'Flowers', icon: 'mdi-flower' }
]

// Sample plant data
const samplePlants: Plant[] = [
  {
    id: 1,
    name: 'Snake Plant',
    scientificName: 'Sansevieria trifasciata',
    category: 'Houseplants',
    difficulty: 'Easy',
    watering: 'Low - every 2-3 weeks',
    light: 'Low to bright indirect',
    temperature: '65-75°F (18-24°C)',
    soil: 'Well-draining potting mix',
    description: 'A hardy, low-maintenance plant perfect for beginners. Known for its air-purifying qualities and tolerance to neglect.',
    tips: [
      'Allow soil to dry completely between waterings',
      'Can tolerate low light conditions',
      'Avoid overwatering to prevent root rot',
      'Wipe leaves occasionally to remove dust'
    ],
    image: 'https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400'
  },
  {
    id: 2,
    name: 'Pothos',
    scientificName: 'Epipremnum aureum',
    category: 'Houseplants',
    difficulty: 'Easy',
    watering: 'Moderate - when top inch is dry',
    light: 'Bright indirect light',
    temperature: '65-85°F (18-29°C)',
    soil: 'Well-draining potting soil',
    description: 'A trailing vine that\'s perfect for hanging baskets or climbing. Very forgiving and grows quickly.',
    tips: [
      'Trim regularly to encourage bushier growth',
      'Can be propagated easily in water',
      'Tolerates various light conditions',
      'Toxic to pets if ingested'
    ],
    image: 'https://images.unsplash.com/photo-1586093248292-4e6f6c3b5e4e?w=400'
  },
  {
    id: 3,
    name: 'Basil',
    scientificName: 'Ocimum basilicum',
    category: 'Herbs',
    difficulty: 'Easy',
    watering: 'Regular - keep soil moist',
    light: 'Full sun (6+ hours)',
    temperature: '65-75°F (18-24°C)',
    soil: 'Rich, well-draining soil',
    description: 'A popular culinary herb with aromatic leaves. Perfect for cooking and easy to grow indoors or outdoors.',
    tips: [
      'Pinch flowers to encourage leaf growth',
      'Harvest regularly for best flavor',
      'Provide good air circulation',
      'Can be grown from seed or cuttings'
    ],
    image: 'https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=400'
  },
  {
    id: 4,
    name: 'Aloe Vera',
    scientificName: 'Aloe barbadensis',
    category: 'Succulents',
    difficulty: 'Easy',
    watering: 'Low - every 2-3 weeks',
    light: 'Bright indirect light',
    temperature: '60-75°F (15-24°C)',
    soil: 'Cactus/succulent mix',
    description: 'A medicinal succulent known for its healing gel. Very drought-tolerant and low-maintenance.',
    tips: [
      'Allow soil to dry completely between waterings',
      'Use gel from leaves for minor burns',
      'Repot when plant outgrows container',
      'Protect from frost'
    ],
    image: 'https://images.unsplash.com/photo-1509587584298-0f3b3a3a1797?w=400'
  },
  {
    id: 5,
    name: 'Tomato',
    scientificName: 'Solanum lycopersicum',
    category: 'Vegetables',
    difficulty: 'Moderate',
    watering: 'Regular - keep consistently moist',
    light: 'Full sun (6-8 hours)',
    temperature: '65-85°F (18-29°C)',
    soil: 'Rich, well-draining soil',
    description: 'A popular vegetable that produces delicious fruits. Requires regular care but very rewarding to grow.',
    tips: [
      'Provide support with stakes or cages',
      'Water at soil level to prevent disease',
      'Fertilize regularly during growing season',
      'Prune suckers for better fruit production'
    ],
    image: 'https://images.unsplash.com/photo-1592841200221-21e1c4e6e8e5?w=400'
  },
  {
    id: 6,
    name: 'Peace Lily',
    scientificName: 'Spathiphyllum wallisii',
    category: 'Houseplants',
    difficulty: 'Moderate',
    watering: 'Moderate - when top inch is dry',
    light: 'Low to medium indirect light',
    temperature: '65-80°F (18-27°C)',
    soil: 'Well-draining potting mix',
    description: 'An elegant flowering houseplant known for its white blooms and air-purifying qualities.',
    tips: [
      'Leaves will droop when thirsty',
      'Mist regularly for humidity',
      'Remove spent flowers',
      'Toxic to pets if ingested'
    ],
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400'
  }
]

// Methods
const searchPlants = () => {
  filterPlants()
}

const filterPlants = () => {
  let filtered = [...plants.value]

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(plant =>
      plant.name.toLowerCase().includes(query) ||
      plant.scientificName.toLowerCase().includes(query) ||
      plant.category.toLowerCase().includes(query)
    )
  }

  if (selectedCategory.value) {
    filtered = filtered.filter(plant => plant.category === selectedCategory.value)
  }

  if (selectedDifficulty.value) {
    filtered = filtered.filter(plant => plant.difficulty === selectedDifficulty.value)
  }

  filteredPlants.value = filtered
}

const handleCategoryChip = (index: number | undefined) => {
  if (index !== undefined) {
    selectedCategory.value = popularCategories[index].name
  } else {
    selectedCategory.value = ''
  }
  filterPlants()
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedDifficulty.value = ''
  selectedCategoryChip.value = undefined
  filterPlants()
}

const viewPlantDetails = (plant: Plant) => {
  selectedPlant.value = plant
  detailsDialog.value = true
}

const toggleFavorite = (plant: Plant) => {
  plant.isFavorite = !plant.isFavorite
  showSnackbar(
    plant.isFavorite ? 'Added to favorites' : 'Removed from favorites',
    'success'
  )
}

const addToMyPlants = (plant: Plant) => {
  // This would typically save to a user's plant collection
  showSnackbar(`${plant.name} added to your plant collection!`, 'success')
  detailsDialog.value = false
}

const getDifficultyColor = (difficulty: string) => {
  const colors: Record<string, string> = {
    'Easy': 'green',
    'Moderate': 'orange',
    'Challenging': 'red',
    'Expert': 'purple'
  }
  return colors[difficulty] || 'grey'
}

const getDifficultyIcon = (difficulty: string) => {
  const icons: Record<string, string> = {
    'Easy': 'mdi-star',
    'Moderate': 'mdi-star-half-full',
    'Challenging': 'mdi-star-outline',
    'Expert': 'mdi-star-circle'
  }
  return icons[difficulty] || 'mdi-star'
}

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    'Houseplants': 'green',
    'Succulents': 'teal',
    'Herbs': 'light-green',
    'Vegetables': 'orange',
    'Flowers': 'pink',
    'Trees': 'brown',
    'Shrubs': 'green-darken-2',
    'Ferns': 'green-lighten-2',
    'Cacti': 'yellow-darken-2',
    'Vines': 'purple'
  }
  return colors[category] || 'grey'
}

const showSnackbar = (message: string, color: string) => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

// Lifecycle
onMounted(() => {
  // Simulate loading
  setTimeout(() => {
    plants.value = samplePlants
    filteredPlants.value = [...plants.value]
    loading.value = false
  }, 1000)
})
</script>

<style scoped>
.plant-library {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.plant-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.plant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
</style>