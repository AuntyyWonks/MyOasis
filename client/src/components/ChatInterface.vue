<template>
  <v-container fluid class="chat-container pa-0">
    <!-- Chat Header -->
    <v-app-bar
      color="green-darken-1"
      density="compact"
      elevation="2"
    >
      <template #prepend>
        <v-avatar size="40" class="ml-2">
          <v-icon color="white" size="24">mdi-leaf</v-icon>
        </v-avatar>
      </template>
      
      <v-app-bar-title class="text-white font-weight-bold">
        Oasis - Your Plant Assistant
      </v-app-bar-title>
      
      <template #append>
        <v-btn
          icon="mdi-information-outline"
          variant="text"
          color="white"
          @click="showInfo = !showInfo"
        />
      </template>
    </v-app-bar>

    <!-- Info Panel -->
    <v-expand-transition>
      <v-card v-show="showInfo" color="green-lighten-5" class="mx-2 mt-2" rounded="lg">
        <v-card-text class="text-center">
          <v-icon color="green-darken-1" size="32" class="mb-2">mdi-sprout</v-icon>
          <div class="text-body-1 font-weight-medium mb-1">Welcome to Oasis!</div>
          <div class="text-body-2 text-grey-darken-1">
            I'm here to help with all your gardening needs. Ask me about plant care, 
            crop planning, or upload images for plant health analysis.
          </div>
        </v-card-text>
      </v-card>
    </v-expand-transition>

    <!-- Chat Messages Area -->
    <v-card
      class="chat-messages mx-2 mt-2"
      :height="chatHeight"
      rounded="lg"
      elevation="2"
    >
      <v-card-text class="pa-0 h-100">
        <div
          ref="messagesContainer"
          class="messages-scroll pa-4"
          style="height: 100%; overflow-y: auto;"
        >
          <!-- Welcome Message -->
          <div v-if="messages.length === 0" class="text-center py-8">
            <v-avatar size="80" color="green-lighten-2" class="mb-4">
              <v-icon color="white" size="40">mdi-leaf</v-icon>
            </v-avatar>
            <h3 class="text-h5 font-weight-bold text-green-darken-1 mb-2">
              Hello {{ userName }}! 🌱
            </h3>
            <p class="text-body-1 text-grey-darken-1 mb-4">
              I'm Oasis, your personal plant assistant. How can I help you today?
            </p>
            <v-row justify="center" class="mt-4">
              <v-col cols="auto">
                <v-chip
                  color="green-lighten-4"
                  text-color="green-darken-2"
                  class="ma-1"
                  @click="sendQuickMessage('How do I care for indoor plants?')"
                >
                  <v-icon start>mdi-home-variant</v-icon>
                  Indoor Plants
                </v-chip>
              </v-col>
              <v-col cols="auto">
                <v-chip
                  color="green-lighten-4"
                  text-color="green-darken-2"
                  class="ma-1"
                  @click="sendQuickMessage('What vegetables should I plant this season?')"
                >
                  <v-icon start>mdi-carrot</v-icon>
                  Seasonal Crops
                </v-chip>
              </v-col>
              <v-col cols="auto">
                <v-chip
                  color="green-lighten-4"
                  text-color="green-darken-2"
                  class="ma-1"
                  @click="sendQuickMessage('My plant leaves are turning yellow, what should I do?')"
                >
                  <v-icon start>mdi-medical-bag</v-icon>
                  Plant Health
                </v-chip>
              </v-col>
            </v-row>
          </div>

          <!-- Chat Messages -->
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message-wrapper mb-4"
          >
            <!-- User Message -->
            <div v-if="message.type === 'user'" class="d-flex justify-end">
              <v-card
                color="blue-darken-1"
                class="user-message pa-3"
                max-width="70%"
                rounded="xl"
                elevation="2"
              >
                <div class="text-white">{{ message.content }}</div>
                <div class="text-blue-lighten-4 text-caption mt-1">
                  {{ formatTime(message.timestamp) }}
                </div>
              </v-card>
            </div>

            <!-- Bot Message -->
            <div v-else class="d-flex justify-start">
              <v-avatar size="32" color="green-darken-1" class="mr-2 mt-1">
                <v-icon color="white" size="16">mdi-leaf</v-icon>
              </v-avatar>
              <v-card
                color="grey-lighten-4"
                class="bot-message pa-3"
                max-width="70%"
                rounded="xl"
                elevation="1"
              >
                <div class="text-grey-darken-3">{{ message.content }}</div>
                <div class="text-grey text-caption mt-1">
                  {{ formatTime(message.timestamp) }}
                </div>
              </v-card>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="d-flex justify-start mb-4">
            <v-avatar size="32" color="green-darken-1" class="mr-2 mt-1">
              <v-icon color="white" size="16">mdi-leaf</v-icon>
            </v-avatar>
            <v-card
              color="grey-lighten-4"
              class="pa-3"
              rounded="xl"
              elevation="1"
            >
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </v-card>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Input Area -->
    <v-card class="mx-2 mt-2 mb-2" rounded="lg" elevation="2">
      <v-card-text class="pa-2">
        <v-row no-gutters align="center">
          <v-col>
            <v-text-field
              v-model="newMessage"
              placeholder="Ask me about plants, gardening, or upload an image..."
              variant="outlined"
              density="compact"
              hide-details
              @keyup.enter="sendMessage"
              :disabled="isTyping"
            >
              <template #prepend-inner>
                <v-icon color="green-darken-1">mdi-message-text</v-icon>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="auto" class="ml-2">
            <v-btn
              icon="mdi-image-plus"
              color="green-darken-1"
              variant="tonal"
              @click="triggerImageUpload"
              :disabled="isTyping"
            />
          </v-col>
          <v-col cols="auto" class="ml-2">
            <v-btn
              icon="mdi-send"
              color="green-darken-1"
              :disabled="!newMessage.trim() || isTyping"
              @click="sendMessage"
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Hidden File Input -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleImageUpload"
    />

    <!-- Image Preview Dialog -->
    <v-dialog v-model="imageDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h6">
          Plant Health Analysis
        </v-card-title>
        <v-card-text>
          <v-img
            v-if="selectedImage"
            :src="selectedImage"
            max-height="300"
            class="mb-4"
          />
          <p>Upload this image for plant health analysis?</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="imageDialog = false">Cancel</v-btn>
          <v-btn color="green-darken-1" @click="uploadImage">Analyze</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'

interface Message {
  type: 'user' | 'bot'
  content: string
  timestamp: Date
}

// Reactive data
const messages = ref<Message[]>([])
const newMessage = ref('')
const isTyping = ref(false)
const showInfo = ref(false)
const userName = ref('Friend')
const messagesContainer = ref<HTMLElement>()
const fileInput = ref<HTMLInputElement>()
const imageDialog = ref(false)
const selectedImage = ref<string | null>(null)
const selectedFile = ref<File | null>(null)

// Computed properties
const chatHeight = computed(() => {
  return window.innerHeight - 200 // Adjust based on header and input heights
})

// Methods
const sendMessage = async () => {
  if (!newMessage.value.trim()) return

  const userMessage: Message = {
    type: 'user',
    content: newMessage.value,
    timestamp: new Date()
  }

  messages.value.push(userMessage)
  const messageToSend = newMessage.value
  newMessage.value = ''
  
  await scrollToBottom()
  
  // Show typing indicator
  isTyping.value = true
  
  try {
    const response = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: messageToSend,
        name: userName.value
      })
    })

    const data = await response.json()
    
    const botMessage: Message = {
      type: 'bot',
      content: data.reply || 'Sorry, I encountered an error. Please try again.',
      timestamp: new Date()
    }

    messages.value.push(botMessage)
  } catch (error) {
    const errorMessage: Message = {
      type: 'bot',
      content: 'Sorry, I\'m having trouble connecting. Please check if the server is running.',
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isTyping.value = false
    await scrollToBottom()
  }
}

const sendQuickMessage = (message: string) => {
  newMessage.value = message
  sendMessage()
}

const triggerImageUpload = () => {
  fileInput.value?.click()
}

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file) {
    selectedFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      selectedImage.value = e.target?.result as string
      imageDialog.value = true
    }
    reader.readAsDataURL(file)
  }
}

const uploadImage = async () => {
  if (!selectedFile.value) return

  imageDialog.value = false
  
  // Add user message showing image upload
  const userMessage: Message = {
    type: 'user',
    content: '📷 Uploaded image for plant health analysis',
    timestamp: new Date()
  }
  messages.value.push(userMessage)
  
  await scrollToBottom()
  isTyping.value = true

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await fetch('http://127.0.0.1:5000/plant-health', {
      method: 'POST',
      body: formData
    })

    const data = await response.json()
    
    const botMessage: Message = {
      type: 'bot',
      content: data.diagnosis || 'Sorry, I couldn\'t analyze the image. Please try again.',
      timestamp: new Date()
    }

    messages.value.push(botMessage)
  } catch (error) {
    const errorMessage: Message = {
      type: 'bot',
      content: 'Sorry, I\'m having trouble analyzing the image. Please check if the server is running.',
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isTyping.value = false
    selectedImage.value = null
    selectedFile.value = null
    await scrollToBottom()
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Lifecycle
onMounted(() => {
  // Get user's name (you could make this configurable)
  const savedName = localStorage.getItem('oasis-user-name')
  if (savedName) {
    userName.value = savedName
  }
})
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow: hidden;
}

.messages-scroll {
  scroll-behavior: smooth;
}

.user-message {
  border-bottom-right-radius: 4px !important;
}

.bot-message {
  border-bottom-left-radius: 4px !important;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #666;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Scrollbar styling */
.messages-scroll::-webkit-scrollbar {
  width: 6px;
}

.messages-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.messages-scroll::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-scroll::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>