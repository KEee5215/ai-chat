<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formType = ref<'login' | 'register'>('login')
const username = ref('')
const email = ref('')
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
    await userStore.login(username.value, password.value)
    router.push({ name: 'chat' })
  } catch (e: any) {
    errorMsg.value = e.message || 'Login failed, please try again'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  if (!username.value || !email.value || !password.value) {
    errorMsg.value = 'Please fill in all fields'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    await userStore.register(username.value, email.value, password.value)
    formType.value = 'login'
    errorMsg.value = 'Registration successful! You can now login.'
  } catch (e: any) {
    errorMsg.value = e.message || 'Registration failed, please try again'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title justify-center text-2xl mb-4">
          {{ formType === 'login' ? 'AI Chat Login' : 'Register' }}
        </h2>

        <div class="tabs">
          <div class="tab tab-active" @click="formType = 'login'">
            Login
          </div>
          <div class="tab" @click="formType = 'register'">
            Register
          </div>
        </div>

        <form @submit.prevent="formType === 'login' ? handleLogin() : handleRegister()">
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

          <div v-if="formType === 'register'" class="form-control w-full mb-4">
            <label class="label">
              <span class="label-text">Email</span>
            </label>
            <input
              v-model="email"
              type="email"
              placeholder="Enter your email"
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
              <span v-else>{{ formType === 'login' ? 'Login' : 'Register' }}</span>
            </button>
          </div>

          <div class="mt-4 text-center text-sm">
            <span @click="formType = formType === 'login' ? 'register' : 'login'">
              {{ formType === 'login' ? 'Not registered? Register' : 'Already have an account? Login' }}
            </span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
