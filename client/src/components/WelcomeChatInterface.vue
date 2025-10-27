<template>
  <div class="chat-interface">
    <!-- Chat Messages Area -->
    <div ref="messagesContainer" class="chat-messages">
      <!-- Welcome Message -->
      <div v-if="messages.length === 0" class="welcome-section">
        <div class="text-center py-12">
          <v-avatar class="mb-6" color="olive-green" size="120">
            <v-icon color="white" size="60">mdi-leaf</v-icon>
          </v-avatar>
          <h2 class="text-h3 font-weight-bold text-olive-green mb-4">
            Welcome to Oasis! 🌱
          </h2>
          <p class="text-h6 text-grey-darken-1 mb-6 mx-auto" style="max-width: 600px;">
            I'm your AI-powered plant assistant. Ask me anything about plant care,
            gardening tips, or upload photos for plant health analysis.
          </p>

          <!-- Quick Start Suggestions -->
          <div class="quick-suggestions">
            <h3 class="text-h6 font-weight-bold text-azure-blue mb-4">
              Try asking me about:
            </h3>
            <v-row class="mb-6" justify="center">
              <v-col cols="auto">
                <v-chip
                  class="ma-2 suggestion-chip"
                  color="azure-blue"
                  size="large"
                  variant="outlined"
                  @click="sendQuickMessage('How do I care for indoor plants?')"
                >
                  <v-icon start>mdi-home-variant</v-icon>
                  Indoor Plant Care
                </v-chip>
              </v-col>
              <v-col cols="auto">
                <v-chip
                  class="ma-2 suggestion-chip"
                  color="olive-green"
                  size="large"
                  variant="outlined"
                  @click="sendQuickMessage('What vegetables should I plant this season?')"
                >
                  <v-icon start>mdi-carrot</v-icon>
                  Seasonal Planting
                </v-chip>
              </v-col>
              <v-col cols="auto">
                <v-chip
                  class="ma-2 suggestion-chip"
                  color="azure-blue"
                  size="large"
                  variant="outlined"
                  @click="sendQuickMessage('My plant leaves are turning yellow, what should I do?')"
                >
                  <v-icon start>mdi-medical-bag</v-icon>
                  Plant Problems
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
                class="user-message pa-4"
                color="azure-blue"
                elevation="3"
                max-width="70%"
                rounded="xl"
              >
                <div class="text-white text-body-1">{{ message.content }}</div>
                <div class="text-blue-lighten-4 text-caption mt-2">
                  {{ formatTime(message.timestamp) }}
                </div>
              </v-card>
              <v-avatar class="ml-3 mt-1" color="azure-blue" size="40">
                <v-icon color="white" size="20">mdi-account</v-icon>
              </v-avatar>
            </div>
          </div>

          <!-- Bot Message -->
          <div v-else class="bot-message-container">
            <div class="d-flex justify-start">
              <v-avatar class="mr-3 mt-1" color="olive-green" size="40">
                <v-icon color="white" size="20">mdi-leaf</v-icon>
              </v-avatar>
              <v-card
                class="bot-message pa-4"
                color="grey-lighten-4"
                elevation="2"
                max-width="70%"
                rounded="xl"
              >
                <div class="text-grey-darken-3 text-body-1" v-html="formatAndSanitizeMarkdown(message.content)" />
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
            <v-avatar class="mr-3 mt-1" color="olive-green" size="40">
              <v-icon color="white" size="20">mdi-leaf</v-icon>
            </v-avatar>
            <v-card
              class="pa-4"
              color="grey-lighten-4"
              elevation="2"
              rounded="xl"
            >
              <div class="typing-indicator">
                <span />
                <span />
                <span />
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
          class="input-card"
          color="white"
          elevation="4"
          rounded="xl"
        >
          <v-card-text class="pa-3">
            <v-row align="center" no-gutters>
              <!-- Text Input (75%) -->
              <v-col class="pr-2" cols="9">
                <v-text-field
                  v-model="newMessage"
                  class="chat-input"
                  :disabled="isTyping"
                  hide-details
                  placeholder="Ask me about plants, gardening, or upload an image..."
                  variant="plain"
                  @keyup.enter="sendMessage"
                >
                  <template #prepend-inner>
                    <v-icon class="mr-2" color="olive-green">mdi-message-text</v-icon>
                  </template>
                </v-text-field>
              </v-col>

              <!-- Send Button (25%) -->
              <v-col class="d-flex justify-end" cols="3">
                <v-btn
                  class="send-button"
                  color="azure-blue"
                  :disabled="!newMessage.trim() || isTyping"
                  rounded="xl"
                  size="large"
                  @click="sendMessage"
                >
                  <v-icon class="mr-2">mdi-send</v-icon>
                  Send
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
  import { nextTick, ref } from 'vue'
  import { apiUrl } from '@/utils/api'
  import { formatAndSanitizeMarkdown } from '@/utils/markdown'

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
  async function sendMessage () {
    if (!newMessage.value.trim()) return

    const userMessage: Message = {
      type: 'user',
      content: newMessage.value,
      timestamp: new Date(),
    }

    messages.value.push(userMessage)
    const messageToSend = newMessage.value
    newMessage.value = ''

    await scrollToBottom()

    // Show typing indicator
    isTyping.value = true

    try {
      const response = await fetch(apiUrl('chat'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageToSend,
          name: 'User',
        }),
      })

      const data = await response.json()

      const botMessage: Message = {
        type: 'bot',
        content: data.reply || 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }

      messages.value.push(botMessage)
    } catch {
      const errorMessage: Message = {
        type: 'bot',
        content: 'Sorry, I\'m having trouble connecting to the server. Please check if the backend is running and try again.',
        timestamp: new Date(),
      }
      messages.value.push(errorMessage)
    } finally {
      isTyping.value = false
      await scrollToBottom()
    }
  }

  function sendQuickMessage (message: string) {
    newMessage.value = message
    sendMessage()
  }

  async function scrollToBottom () {
    await nextTick()
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }

  function formatTime (date: Date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
</script>

<style scoped>
.chat-interface {
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
  min-width: 100px;
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

.bg-azure-blue {
  background-color: #2196f3 !important;
}

.bg-olive-green {
  background-color: #689f38 !important;
}
</style>
