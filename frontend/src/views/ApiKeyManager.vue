<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useApiKeyStore, type ApiKeyResponse } from '@/stores/apikey'

const router = useRouter()
const userStore = useUserStore()
const apiKeyStore = useApiKeyStore()

const newKeyName = ref('')
const createdKey = ref<{ name: string; key: string } | null>(null)
const loading = ref(false)

onMounted(async () => {
  if (userStore.token) {
    await apiKeyStore.fetchKeys()
  }
})

async function handleCreateKey() {
  if (!newKeyName.value.trim()) return
  loading.value = true
  try {
    const result = await apiKeyStore.createKey(newKeyName.value.trim())
    if (result) {
      createdKey.value = { name: result.name, key: result.key_preview }
    }
    newKeyName.value = ''
  } catch (e: any) {
    alert(e.message || 'Failed to create API key')
  } finally {
    loading.value = false
  }
}

async function handleDeleteKey(id: string) {
  if (!confirm('Are you sure you want to delete this API key?')) return
  try {
    await apiKeyStore.removeKey(id)
  } catch (e: any) {
    alert(e.message || 'Failed to delete API key')
  }
}

function copyKey(key: string) {
  navigator.clipboard.writeText(key)
}

function maskKey(key: string): string {
  // Backend already provides key_preview which is masked
  return key
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function handleBack() {
  router.push({ name: 'chat' })
}

function handleLogout() {
  userStore.logout()
  router.push({ name: 'login' })
}

function dismissCreated() {
  createdKey.value = null
}
</script>

<template>
  <div class="min-h-screen bg-base-200">
    <!-- Navbar -->
    <nav class="navbar bg-base-300 sticky top-0 z-10 shadow-sm">
      <div class="flex-1">
        <button @click="handleBack" class="btn btn-ghost btn-sm gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-4">
            <path d="m15 18-6-6 6-6" />
          </svg>
          Back to Chat
        </button>
        <span class="font-semibold text-lg ml-2">API Key Management</span>
      </div>
      <div class="px-2">
        <button @click="handleLogout" class="btn btn-ghost btn-sm">Logout</button>
      </div>
    </nav>

    <div class="max-w-3xl mx-auto p-6 space-y-6">
      <!-- Created Key Alert -->
      <div v-if="createdKey" class="alert alert-success">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-6">
          <path d="M20 6 9 17l-5-5" />
        </svg>
        <div class="flex-1">
          <p class="font-medium">API key "{{ createdKey.name }}" created successfully!</p>
          <div class="flex items-center gap-2 mt-1">
            <code class="text-sm bg-success/10 px-2 py-1 rounded">{{ createdKey.key }}</code>
            <button @click="copyKey(createdKey.key)" class="btn btn-xs btn-ghost" title="Copy key">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-4">
                <rect width="14" height="14" x="8" y="8" rx="2" ry="2" />
                <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
              </svg>
            </button>
          </div>
          <p class="text-xs mt-1 opacity-70">Make sure to copy this key now, it won't be shown again.</p>
        </div>
        <button @click="dismissCreated" class="btn btn-sm btn-ghost">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-5">
            <path d="M18 6 6 18" />
            <path d="m6 6 12 12" />
          </svg>
        </button>
      </div>

      <!-- Create Key Card -->
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <h2 class="card-title">Create New API Key</h2>
          <div class="form-control mt-2">
            <div class="flex gap-2">
              <input
                v-model="newKeyName"
                type="text"
                placeholder="Enter a name for this key (e.g., Production, Testing)"
                class="input input-bordered flex-1"
                @keyup.enter="handleCreateKey"
              />
              <button
                @click="handleCreateKey"
                :disabled="!newKeyName.trim() || loading"
                class="btn btn-primary"
              >
                <span v-if="loading" class="loading loading-spinner loading-sm"></span>
                <span v-else>Create</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- API Keys List Card -->
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <h2 class="card-title">Your API Keys</h2>

          <!-- Empty State -->
          <div v-if="apiKeyStore.keys.length === 0" class="py-8 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="size-12 mx-auto text-base-content/20 mb-2">
              <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
            </svg>
            <p class="text-base-content/50">No API keys yet</p>
            <p class="text-sm text-base-content/40">Create a key above to get started</p>
          </div>

          <!-- Keys Table -->
          <div v-else class="overflow-x-auto">
            <table class="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Key</th>
                  <th>Last Used</th>
                  <th>Created</th>
                  <th class="w-28">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="k in apiKeyStore.keys" :key="k.id">
                  <td class="font-medium">{{ k.name }}</td>
                  <td>
                    <code class="text-sm">{{ k.key_preview }}</code>
                  </td>
                  <td class="text-sm text-base-content/60">{{ k.last_used_at ? formatDate(k.last_used_at) : 'Never' }}</td>
                  <td class="text-sm text-base-content/60">{{ formatDate(k.created_at) }}</td>
                  <td>
                    <button
                      @click="handleDeleteKey(k.id)"
                      class="btn btn-xs btn-error btn-outline"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
