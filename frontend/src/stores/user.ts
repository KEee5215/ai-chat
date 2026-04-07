import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export interface UserInfo {
  id: string
  username: string
  email: string
  avatar?: string
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function setUserInfo(info: UserInfo) {
    userInfo.value = info
  }

  function login(username: string, password: string) {
    // TODO: Replace with real API call
    const mockToken = 'mock-token-' + Date.now()
    setToken(mockToken)
    setUserInfo({
      id: '1',
      username,
      email: `${username}@example.com`,
      avatar: '',
    })
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return { token, userInfo, isLoggedIn, setToken, setUserInfo, login, logout }
})
