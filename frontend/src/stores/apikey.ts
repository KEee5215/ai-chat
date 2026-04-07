import { ref } from 'vue'
import { defineStore } from 'pinia'

export interface ApiKey {
  id: string
  name: string
  key: string
  createdAt: string
}

function loadKeys(): ApiKey[] {
  const raw = localStorage.getItem('api_keys')
  if (!raw) return []
  try {
    return JSON.parse(raw) as ApiKey[]
  } catch {
    return []
  }
}

function saveKeys(keys: ApiKey[]) {
  localStorage.setItem('api_keys', JSON.stringify(keys))
}

function generateKey(): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = 'sk-'
  for (let i = 0; i < 48; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

export const useApiKeyStore = defineStore('apikey', () => {
  const keys = ref<ApiKey[]>(loadKeys())

  function addKey(name: string): ApiKey {
    const newKey: ApiKey = {
      id: Date.now().toString(),
      name,
      key: generateKey(),
      createdAt: new Date().toISOString(),
    }
    keys.value.push(newKey)
    saveKeys(keys.value)
    return newKey
  }

  function removeKey(id: string) {
    keys.value = keys.value.filter((k) => k.id !== id)
    saveKeys(keys.value)
  }

  return { keys, addKey, removeKey }
})
