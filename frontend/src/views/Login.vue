<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  if (!username.value || !password.value) {
    errorMsg.value = 'Please enter username and password'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    // TODO: Replace with real API call
    userStore.login(username.value, password.value)
    router.push({ name: 'chat' })
  } catch (e) {
    errorMsg.value = 'Login failed, please try again'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title justify-center text-2xl mb-4">AI Chat Login</h2>

        <form @submit.prevent="handleLogin">
          <div class="form-control w-full mb-4">
            <label class="label">
              <span class="label-text">Username</span>
            </label>
            <input
              v-model="username"
              type="text"
              placeholder="Enter your username"
              class="input input-bordered w-full"
            />
          </div>

          <div class="form-control w-full mb-4">
            <label class="label">
              <span class="label-text">Password</span>
            </label>
            <input
              v-model="password"
              type="password"
              placeholder="Enter your password"
              class="input input-bordered w-full"
            />
          </div>

          <div v-if="errorMsg" class="text-error text-sm mb-4 text-center">
            {{ errorMsg }}
          </div>

          <div class="form-control mt-4">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="loading loading-spinner loading-sm"></span>
              <span v-else>Login</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
