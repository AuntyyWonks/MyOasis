<template>
  <div class="adviser-page">
    <!-- Chat Messages Area -->
    <div class="chat-messages" ref="messagesContainer">
      <!-- Welcome Message -->
      <div v-if="messages.length === 0" class="welcome-section">
        <div class="text-center py-12">
          <v-avatar size="120" color="azure-blue" class="mb-6">
            <v-icon color="white" size="60">mdi-chat</v-icon>
          </v-avatar>
          <h2 class="text-h3 font-weight-bold text-azure-blue mb-4">
            Adviser - Crop Planning Expert 🌾
          </h2>
          <p class="text-h6 text-grey-darken-1 mb-6 mx-auto" style="max-width: 600px;">
            I'm your crop planning adviser. Tell me about your location, garden size, 
            and preferences to get personalized crop recommendations.
          </p>
          
          <!-- Quick Start Suggestions -->
          <div class="quick-suggestions">
            <h3 class="text-h6 font-weight-bold text-olive-green mb-4">
              Try asking me about:
            </h3>
            <v-row justify="center" class="mb-6">
              <v-col cols="auto">
                <v-chip
                  color="azure-blue"
                  variant="outlined"
                  size="large"
                  class="ma-2 suggestion-chip"
                  @click="sendQuickMessage('I live in California and have a medium backyard. What vegetables should I plant this spring?')"
                >
                  <v-icon start>mdi-map-marker</v-icon>
                  Location-based Planning
                </v-chip>
              </v-col>
              <v-col cols="auto">
                <v-chip
                  color="olive-green"
                  variant="outlined"
                  size="large"
                  class="ma-2 suggestion-chip"
                  @click="sendQuickMessage('I am a beginner gardener with a small balcony garden. What easy plants should I start with?')"
                >
                  <v-icon start>mdi-sprout</v-icon>
                  Beginner Friendly
                </v-chip>
              </v-col>
              <v-col cols="auto">
                <v-chip
                  color="azure-blue"
                  variant="outlined"
                  size="large"
                  class="ma-2 suggestion-chip"
                  @click="sendQuickMessage('I want to grow herbs and vegetables for cooking. I have good sunlight and live in a temperate climate.')"
                >
                  <v-icon start>mdi-chef-hat</v-icon>
                  Culinary Garden
                </v-chip>
              </v-col>
            </v-row>
          </div>
        </div>
      </div>

      <!-- Chat Messages -->
      <div class="messages-list pa-4">
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="message-wrapper mb-6"
        >
          <!-- User Message -->
          <div v-if="message.type === 'user'" class="user-message-container">
            <div class="d-flex justify-end">
              <v-card
                color="azure-blue"
                class="user-message pa-4"
                max-width="70%"
                rounded="xl"
                elevation="3"
              >
                <div class="text-white text-body-1">{{ message.content }}</div>
                <div class="text-blue-lighten-4 text-caption mt-2">
                  {{ formatTime(message.timestamp) }}
                </div>
              </v-card>
              <v-avatar size="40" color="azure-blue" class="ml-3 mt-1">
                <v-icon color="white" size="20">mdi-account</v-icon>
              </v-avatar>
            </div>
          </div>

          <!-- Bot Message -->
          <div v-else class="bot-message-container">
            <div class="d-flex justify-start">
              <v-avatar size="40" color="olive-green" class="mr-3 mt-1">
                <v-icon color="white" size="20">mdi-chat</v-icon>
              </v-avatar>
              <v-card
                color="grey-lighten-4"
                class="bot-message pa-4"
                max-width="70%"
                rounded="xl"
                elevation="2"
              >
                <div class="text-grey-darken-3 text-body-1" v-html="formatAndSanitizeMarkdown(message.content)"></div>
                <div class="text-grey text-caption mt-2">
                  {{ formatTime(message.timestamp) }}
                </div>
              </v-card>
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="typing-container mb-6">
          <div class="d-flex justify-start">
            <v-avatar size="40" color="olive-green" class="mr-3 mt-1">
              <v-icon color="white" size="20">mdi-chat</v-icon>
            </v-avatar>
            <v-card
              color="grey-lighten-4"
              class="pa-4"
              rounded="xl"
              elevation="2"
            >
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </v-card>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Input Area -->
    <div class="chat-input-area">
      <v-container class="pa-4">
        <v-card
          color="white"
          rounded="xl"
          elevation="4"
          class="input-card"
        >
          <v-card-text class="pa-3">
            <v-row no-gutters align="center">
              <!-- Text Input (75%) -->
              <v-col cols="9" class="pr-2">
                <v-text-field
                  v-model="newMessage"
                  placeholder="Tell me about your location, garden size, and what you'd like to grow..."
                  variant="plain"
                  hide-details
                  class="chat-input"
                  @keyup.enter="sendMessage"
                  :disabled="isTyping"
                >
                  <template #prepend-inner>
                    <v-icon color="azure-blue" class="mr-2">mdi-chat</v-icon>
                  </template>
                </v-text-field>
              </v-col>
              
              <!-- Send Button (25%) -->
              <v-col cols="3" class="d-flex justify-end">
                <v-btn
                  color="azure-blue"
                  size="large"
                  rounded="xl"
                  class="send-button"
                  :disabled="!newMessage.trim() || isTyping"
                  @click="sendMessage"
                >
                  <v-icon class="mr-2">mdi-send</v-icon>
                  Get Advice
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { formatAndSanitizeMarkdown } from '@/utils/markdown'
import { apiUrl } from '@/utils/api'

interface Message {
  type: 'user' | 'bot'
  content: string
  timestamp: Date
}

// Reactive data
const messages = ref<Message[]>([])
const newMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement>()

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
    const response = await fetch(apiUrl('crop-plan'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_info: messageToSend
      })
    })

    const data = await response.json()
    
    const botMessage: Message = {
      type: 'bot',
      content: data.recommendations_text || 'Sorry, I encountered an error. Please try again with more details about your location and garden.',
      timestamp: new Date()
    }

    messages.value.push(botMessage)
  } catch (error) {
    const errorMessage: Message = {
      type: 'bot',
      content: 'Sorry, I\'m having trouble connecting to the server. Please check if the backend is running and try again.',
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

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.adviser-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  scroll-behavior: smooth;
  background: transparent;
}

.welcome-section {
  background: linear-gradient(135deg, #e3f2fd 0%, #f1f8e9 100%);
  border-radius: 20px;
  margin: 20px;
  border: 2px solid #e0e0e0;
}

.suggestion-chip {
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.suggestion-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.messages-list {
  min-height: 200px;
}

.user-message {
  border-bottom-right-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.bot-message {
  border-bottom-left-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-input-area {
  background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
  border-top: 2px solid #e0e0e0;
}

.input-card {
  border: 2px solid #e3f2fd;
  transition: all 0.3s ease;
}

.input-card:hover {
  border-color: #2196f3;
  box-shadow: 0 4px 20px rgba(33, 150, 243, 0.2);
}

.chat-input {
  font-size: 16px;
}

.send-button {
  min-width: 120px;
  font-weight: 600;
  text-transform: none;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.send-button:hover {
  box-shadow: 0 6px 16px rgba(33, 150, 243, 0.4);
  transform: translateY(-1px);
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 0;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #689f38;
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
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Custom color classes */
.text-azure-blue {
  color: #2196f3 !important;
}

.text-olive-green {
  color: #689f38 !important;
}
</style>