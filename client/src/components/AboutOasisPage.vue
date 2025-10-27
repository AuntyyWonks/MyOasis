<template>
  <div class="about-oasis-page pa-6">
    <v-container>
      <!-- Hero Section -->
      <v-row class="mb-8">
        <v-col class="text-center" cols="12">
          <v-avatar class="mb-6" color="olive-green" size="150">
            <v-icon color="white" size="80">mdi-leaf</v-icon>
          </v-avatar>
          <h1 class="text-h2 font-weight-bold text-olive-green mb-4">
            About My Oasis
          </h1>
          <p class="text-h5 text-grey-darken-1 mx-auto" style="max-width: 800px;">
            Your AI-powered companion for all things gardening. From plant care advice
            to health diagnosis, we're here to help your garden thrive.
          </p>
        </v-col>
      </v-row>

      <!-- Mission Section -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card color="grey-lighten-5" elevation="3" rounded="lg">
            <v-card-text class="pa-8">
              <h2 class="text-h4 font-weight-bold text-azure-blue mb-4 text-center">
                Our Mission
              </h2>
              <p class="text-h6 text-center text-grey-darken-1 mb-6">
                To make gardening accessible, enjoyable, and successful for everyone,
                regardless of their experience level.
              </p>
              <v-row>
                <v-col class="text-center" cols="12" md="4">
                  <v-icon class="mb-3" color="olive-green" size="64">mdi-lightbulb</v-icon>
                  <h3 class="text-h6 font-weight-bold mb-2">Expert Knowledge</h3>
                  <p class="text-body-1">
                    AI-powered insights backed by horticultural expertise
                  </p>
                </v-col>
                <v-col class="text-center" cols="12" md="4">
                  <v-icon class="mb-3" color="azure-blue" size="64">mdi-heart</v-icon>
                  <h3 class="text-h6 font-weight-bold mb-2">Personalized Care</h3>
                  <p class="text-body-1">
                    Tailored advice for your specific plants and environment
                  </p>
                </v-col>
                <v-col class="text-center" cols="12" md="4">
                  <v-icon class="mb-3" color="olive-green" size="64">mdi-earth</v-icon>
                  <h3 class="text-h6 font-weight-bold mb-2">Sustainable Growth</h3>
                  <p class="text-body-1">
                    Promoting eco-friendly gardening practices
                  </p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Features Section -->
      <v-row class="mb-8">
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold text-azure-blue mb-6 text-center">
            What We Offer
          </h2>
        </v-col>

        <v-col class="mb-4" cols="12" md="6">
          <v-card class="h-100" elevation="2" rounded="lg">
            <v-card-text class="pa-6">
              <div class="d-flex align-center mb-4">
                <v-avatar class="mr-4" color="azure-blue" size="60">
                  <v-icon color="white" size="30">mdi-chat</v-icon>
                </v-avatar>
                <h3 class="text-h5 font-weight-bold">Adviser</h3>
              </div>
              <p class="text-body-1 mb-4">
                Get personalized crop planning and gardening advice based on your location,
                climate, and experience level. Our AI adviser helps you choose the right
                plants for your garden.
              </p>
              <v-chip color="azure-blue" variant="tonal">Crop Planning</v-chip>
              <v-chip class="ml-2" color="azure-blue" variant="tonal">Location-based</v-chip>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col class="mb-4" cols="12" md="6">
          <v-card class="h-100" elevation="2" rounded="lg">
            <v-card-text class="pa-6">
              <div class="d-flex align-center mb-4">
                <v-avatar class="mr-4" color="olive-green" size="60">
                  <v-icon color="white" size="30">mdi-medical-bag</v-icon>
                </v-avatar>
                <h3 class="text-h5 font-weight-bold">Dr. Oasis</h3>
              </div>
              <p class="text-body-1 mb-4">
                Upload photos of your plants for instant health diagnosis. Dr. Oasis
                can identify diseases, pests, and nutrient deficiencies, providing
                cost efficient treatment recommendations.
              </p>
              <v-chip color="olive-green" variant="tonal">Plant Diagnosis</v-chip>
              <v-chip class="ml-2" color="olive-green" variant="tonal">Image Analysis</v-chip>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col class="mb-4" cols="12" md="6">
          <v-card class="h-100" elevation="2" rounded="lg">
            <v-card-text class="pa-6">
              <div class="d-flex align-center mb-4">
                <v-avatar class="mr-4" color="azure-blue" size="60">
                  <v-icon color="white" size="30">mdi-chat</v-icon>
                </v-avatar>
                <h3 class="text-h5 font-weight-bold">Welcome Chat</h3>
              </div>
              <p class="text-body-1 mb-4">
                Start your gardening journey with our friendly AI assistant. Ask any
                plant-related questions and get instant, helpful responses.
              </p>
              <v-chip color="azure-blue" variant="tonal">24/7 Support</v-chip>
              <v-chip class="ml-2" color="azure-blue" variant="tonal">General Advice</v-chip>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col class="mb-4" cols="12" md="6">
          <v-card class="h-100" elevation="2" rounded="lg">
            <v-card-text class="pa-6">
              <div class="d-flex align-center mb-4">
                <v-avatar class="mr-4" color="olive-green" size="60">
                  <v-icon color="white" size="30">mdi-book-open-variant</v-icon>
                </v-avatar>
                <h3 class="text-h5 font-weight-bold">Garden Journal</h3>
              </div>
              <p class="text-body-1 mb-4">
                Track your gardening progress with our digital journal. Record planting
                dates, care activities, and monitor your plants' growth over time.
              </p>
              <v-chip color="olive-green" variant="tonal">Progress Tracking</v-chip>
              <v-chip class="ml-2" color="olive-green" variant="tonal">Photo Logs</v-chip>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Technology Section -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card color="azure-blue" elevation="3" rounded="lg">
            <v-card-text class="pa-8 text-center">
              <h2 class="text-h4 font-weight-bold text-white mb-4">
                Powered by Advanced AI
              </h2>
              <p class="text-h6 text-blue-lighten-4 mb-6">
                My Oasis uses cutting-edge artificial intelligence to provide accurate,
                personalized gardening advice and plant health analysis.
              </p>
              <v-row>
                <v-col cols="12" md="4">
                  <v-icon class="mb-3" color="white" size="48">mdi-brain</v-icon>
                  <h4 class="text-h6 font-weight-bold text-white mb-2">Machine Learning</h4>
                  <p class="text-blue-lighten-4">
                    Continuously learning from plant data and user interactions
                  </p>
                </v-col>
                <v-col cols="12" md="4">
                  <v-icon class="mb-3" color="white" size="48">mdi-image-search</v-icon>
                  <h4 class="text-h6 font-weight-bold text-white mb-2">Image Recognition</h4>
                  <p class="text-blue-lighten-4">
                    Advanced computer vision for plant health diagnosis
                  </p>
                </v-col>
                <v-col cols="12" md="4">
                  <v-icon class="mb-3" color="white" size="48">mdi-database</v-icon>
                  <h4 class="text-h6 font-weight-bold text-white mb-2">Expert Knowledge</h4>
                  <p class="text-blue-lighten-4">
                    Vast database of horticultural expertise and best practices
                  </p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Contact Section -->
      <v-row>
        <v-col cols="12">
          <v-card color="grey-lighten-5" elevation="2" rounded="lg">
            <v-card-text class="pa-8 text-center">
              <h2 class="text-h4 font-weight-bold text-olive-green mb-4">
                Get in Touch
              </h2>
              <p class="text-h6 text-grey-darken-1 mb-6">
                Have questions or feedback? We'd love to hear from you!
              </p>
              <v-row justify="center">
                <v-col class="text-center" cols="12" md="4">
                  <v-icon class="mb-2" color="azure-blue" size="32">mdi-email</v-icon>
                  <h4 class="text-h6 font-weight-bold mb-2">Email</h4>
                  <p class="text-body-1">support@oasis-plants.com</p>
                </v-col>
                <v-col class="text-center" cols="12" md="4">
                  <v-icon class="mb-2" color="olive-green" size="32">mdi-web</v-icon>
                  <h4 class="text-h6 font-weight-bold mb-2">Website</h4>
                  <p class="text-body-1">www.oasis-plants.com</p>
                </v-col>
                <v-col class="text-center" cols="12" md="4">
                  <v-icon class="mb-2" color="azure-blue" size="32">mdi-account-group</v-icon>
                  <h4 class="text-h6 font-weight-bold mb-2">Community</h4>
                  <p class="text-body-1">Join our gardening community</p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
// No reactive data needed for this static page
</script>

<style scoped>
.about-oasis-page {
  height: 100%;
  overflow-y: auto;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
}

/* Custom color classes */
.text-azure-blue {
  color: #2196f3 !important;
}

.text-olive-green {
  color: #689f38 !important;
}

/* Scrollbar styling */
.about-oasis-page::-webkit-scrollbar {
  width: 8px;
}

.about-oasis-page::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.about-oasis-page::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.about-oasis-page::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
