import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { listApiKeys, createApiKey, deleteApiKey } from '../api/index'

export interface ApiKeyResponse {
  id: string
  name: string
  key_preview: string
  last_used_at: string | null
  created_at: string
}

export const useApiKeyStore = defineStore('apikey', () => {
  const keys = ref<ApiKeyResponse[]>([])

  const isLoggedIn = computed(() => !!useUserStore().token.value)

  async function fetchKeys() {
    if (!isLoggedIn.value) return
    const response = await listApiKeys(useUserStore().token.value)
    keys.value = response.keys
  }

  async function createKey(name: string) {
    if (!isLoggedIn.value) return
    const result = await createApiKey(useUserStore().token.value, name)
    const newKey: ApiKeyResponse = {
      id: result.id,
      name: result.name,
      key_preview: result.key_preview,
      last_used_at: result.last_used_at,
      created_at: result.created_at,
    }
    keys.value.push(newKey)
    return newKey
  }

  async function removeKey(keyId: string) {
    if (!isLoggedIn.value) return
    await deleteApiKey(useUserStore().token.value, keyId)
    keys.value = keys.value.filter((k) => k.id !== keyId)
  }

  return { keys, fetchKeys, createKey, removeKey, isLoggedIn }
})
