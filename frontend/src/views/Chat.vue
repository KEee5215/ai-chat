<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const messages = ref<Message[]>([
  { id: 1, role: 'assistant', content: 'Hello! How can I help you today?', timestamp: new Date() },
])
const inputMessage = ref('')
const isTyping = ref(false)
const chatContainer = ref<HTMLElement | null>(null)

let messageId = 2

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

async function sendMessage() {
  if (!inputMessage.value.trim()) return

  const userMsg: Message = {
    id: messageId++,
    role: 'user',
    content: inputMessage.value.trim(),
    timestamp: new Date(),
  }
  messages.value.push(userMsg)
  inputMessage.value = ''
  isTyping.value = true
  scrollToBottom()

  // TODO: Replace with real API call
  setTimeout(() => {
    const assistantMsg: Message = {
      id: messageId++,
      role: 'assistant',
      content: `This is a mock response to: "${userMsg.content}"`,
      timestamp: new Date(),
    }
    messages.value.push(assistantMsg)
    isTyping.value = false
    scrollToBottom()
  }, 1000)
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

function handleLogout() {
  userStore.logout()
  router.push({ name: 'login' })
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="flex h-screen bg-base-200">
    <!-- Sidebar -->
    <div class="w-64 bg-base-100 border-r border-base-300 flex flex-col">
      <div class="p-4 border-b border-base-300">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-bold">AI Chat</h1>
          <button @click="handleLogout" class="btn btn-ghost btn-sm btn-square">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-4">
        <button class="btn btn-outline w-full justify-start mb-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          New Chat
        </button>

        <div class="space-y-1">
          <div class="text-xs text-base-content/50 px-2 py-1">Recent Chats</div>
          <!-- Placeholder for chat history -->
          <button class="btn btn-ghost btn-sm w-full justify-start text-left truncate">
            Sample Chat
          </button>
        </div>
      </div>

      <!-- User info -->
      <div class="p-4 border-t border-base-300">
        <div class="flex items-center gap-2">
          <div class="avatar placeholder">
            <div class="bg-primary text-primary-content rounded-full w-8">
              <span class="text-xs">{{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
            </div>
          </div>
          <span class="text-sm truncate">{{ userStore.userInfo?.username }}</span>
        </div>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col">
      <!-- Chat Header -->
      <div class="navbar bg-base-100 border-b border-base-300 px-6">
        <div class="flex-1">
          <span class="text-lg font-semibold">Chat</span>
        </div>
      </div>

      <!-- Messages -->
      <div ref="chatContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="chat"
          :class="msg.role === 'user' ? 'chat-end' : 'chat-start'"
        >
          <div class="chat-image avatar">
            <div class="w-10 rounded-full" :class="msg.role === 'user' ? 'bg-primary text-primary-content' : 'bg-secondary text-secondary-content'">
              <span class="text-sm">
                {{ msg.role === 'user' ? (userStore.userInfo?.username?.charAt(0)?.toUpperCase() || 'U') : 'AI' }}
              </span>
            </div>
          </div>

          <div class="chat-header">
            {{ msg.role === 'user' ? 'You' : 'AI Assistant' }}
            <time class="text-xs opacity-50 ml-2">{{ formatTime(msg.timestamp) }}</time>
          </div>

          <div class="chat-bubble" :class="msg.role === 'user' ? 'chat-bubble-primary' : ''">
            {{ msg.content }}
          </div>
        </div>

        <!-- Typing indicator -->
        <div v-if="isTyping" class="chat chat-start">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full bg-secondary text-secondary-content">
              <span class="text-sm">AI</span>
            </div>
          </div>
          <div class="chat-bubble">
            <span class="loading loading-dots loading-sm"></span>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="bg-base-100 border-t border-base-300 p-4">
        <div class="flex gap-2 max-w-4xl mx-auto">
          <textarea
            v-model="inputMessage"
            @keydown="handleKeydown"
            placeholder="Type a message... (Enter to send, Shift+Enter for new line)"
            class="textarea textarea-bordered flex-1"
            rows="1"
          ></textarea>
          <button
            @click="sendMessage"
            :disabled="!inputMessage.trim() || isTyping"
            class="btn btn-primary"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
