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
  <div class="drawer lg:drawer-open">
    <input id="chat-drawer" type="checkbox" class="drawer-toggle" />

    <!-- Drawer Content (Main Chat Area) -->
    <div class="drawer-content flex flex-col">
      <!-- Navbar -->
      <nav class="navbar bg-base-300 sticky top-0 z-10">
        <label for="chat-drawer" aria-label="open sidebar" class="btn btn-square btn-ghost">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-6">
            <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
            <line x1="9" x2="9" y1="3" y2="21" />
          </svg>
        </label>
        <div class="flex-1 px-4">
          <span class="font-semibold text-lg">AI Chat</span>
        </div>
        <div class="px-2">
          <button @click="handleLogout" class="btn btn-ghost btn-sm" title="Logout">
            Logout
          </button>
        </div>
      </nav>

      <!-- Messages Area -->
      <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
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
            class="textarea textarea-bordered flex-1 resize-none"
            rows="1"
          ></textarea>
          <button
            @click="sendMessage"
            :disabled="!inputMessage.trim() || isTyping"
            class="btn btn-primary shrink-0"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-5">
              <path d="m22 2-7 20-4-9-9-4Z" />
              <path d="M22 2 11 13" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Drawer Side (Sidebar) -->
    <div class="drawer-side is-drawer-close:overflow-visible">
      <label for="chat-drawer" aria-label="close sidebar" class="drawer-overlay"></label>

      <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-14 is-drawer-open:w-64">
        <!-- Sidebar Header -->
        <div class="p-4 border-b border-base-300 w-full flex items-center justify-between">
          <h1 class="font-bold text-xl is-drawer-close:hidden">AI Chat</h1>
          <span class="is-drawer-close:block is-drawer-open:hidden text-primary font-bold">AI</span>
        </div>

        <!-- New Chat Button -->
        <div class="p-2 w-full">
          <button class="btn btn-outline w-full is-drawer-close:justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-4">
              <path d="M5 12h14" />
              <path d="M12 5v14" />
            </svg>
            <span class="is-drawer-close:hidden">New Chat</span>
          </button>
        </div>

        <!-- Recent Chats Menu -->
        <ul class="menu w-full grow px-2 pt-2">
          <li class="menu-title is-drawer-close:hidden">
            <span class="text-xs text-base-content/50">Recent Chats</span>
          </li>
          <li>
            <a class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Sample Chat">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-4">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              <span class="is-drawer-close:hidden">Sample Chat</span>
            </a>
          </li>
        </ul>

        <!-- API Keys Nav -->
        <ul class="menu w-full px-2">
          <li>
            <router-link to="/api-keys" class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="API Keys">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-4">
                <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
              </svg>
              <span class="is-drawer-close:hidden">API Keys</span>
            </router-link>
          </li>
        </ul>

        <!-- User Info Footer -->
        <div class="p-4 border-t border-base-300 w-full">
          <div class="flex items-center gap-2">
            <div class="avatar placeholder shrink-0">
              <div class="bg-primary text-primary-content rounded-full w-8">
                <span class="text-xs">{{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium truncate is-drawer-close:hidden">
                {{ userStore.userInfo?.username }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
