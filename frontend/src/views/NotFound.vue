<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToChat() {
  router.push({ name: 'chat' })
}

function goToLogin() {
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body text-center">
        <div class="text-6xl font-bold text-primary mb-4">404</div>
        <h2 class="card-title justify-center text-2xl mb-2">Page Not Found</h2>
        <p class="text-base-content/70 mb-6">
          The page you're looking for doesn't exist or has been moved.
        </p>

        <div class="flex gap-2 justify-center">
          <button @click="goToChat" class="btn btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-4">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            Go to Chat
          </button>
          <button @click="goToLogin" class="btn btn-ghost">
            Login
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
