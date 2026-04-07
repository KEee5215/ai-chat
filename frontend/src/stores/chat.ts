import { ref, computed, nextTick } from 'vue'
import { defineStore } from 'pinia'
import { listSessions, createSession as apiCreateSession, getSession, sendMessage, streamMessage } from '../api/index'

export interface Message {
  id: string
  session_id: string
  role: string
  content: string
  tokens_used: number
  created_at: string
}

export interface ChatSession {
  id: string
  user_id: string
  title: string | null
  created_at: string
  updated_at: string
  messages: Message[]
}

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>([])
  const currentSessionId = ref<string | null>(null)

  const currentUserSession = computed(() => {
    if (!currentSessionId.value) return null
    return sessions.value.find(s => s.id === currentSessionId.value)
  })

  async function fetchSessions(token: string) {
    const response = await listSessions(token)
    sessions.value = response as ChatSession[]
  }

  async function createSession(token: string, title?: string) {
    const result = await apiCreateSession(token, title)
    const session: ChatSession = {
      id: result.id,
      user_id: result.user_id,
      title: result.title || null,
      created_at: result.created_at,
      updated_at: result.updated_at,
      messages: [],
    }
    sessions.value.push(session)
    currentSessionId.value = session.id
    return session
  }

  function selectSession(sessionId: string) {
    currentSessionId.value = sessionId
  }

  async function loadSession(token: string, sessionId: string) {
    const response = await getSession(token, sessionId)
    return response as ChatSession
  }

  async function sendSimpleMessage(token: string, content: string) {
    if (!currentSessionId.value) return
    const result = await sendMessage(token, currentSessionId.value, content)
    return result as Record<string, unknown>
  }

  async function sendStreamMessage(
    token: string,
    sessionId: string,
    content: string,
    onChunk: (text: string, done: boolean) => void,
    onDone: () => void,
    onError: (err: string) => void
  ) {
    await streamMessage(token, sessionId, content, onChunk, onDone, onError)
  }

  function getCurrentMessages() {
    return currentUserSession.value?.messages ?? []
  }

  function addMessageToCurrentSession(message: Message) {
    if (currentUserSession.value) {
      currentUserSession.value.messages.push(message)
      scrollToBottom()
    }
  }

  function scrollToBottom() {
    nextTick(() => {
      const container = document.getElementById('messages-container')
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    })
  }

  return {
    sessions,
    currentSessionId,
    currentUserSession,
    fetchSessions,
    createSession,
    selectSession,
    loadSession,
    sendSimpleMessage,
    sendStreamMessage,
    getCurrentMessages,
    addMessageToCurrentSession,
    scrollToBottom,
  }
})
