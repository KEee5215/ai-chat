import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import {
  register as apiRegister,
  login as apiLogin,
  getMe,
} from "../api/index";

export interface UserInfo {
  id: string;
  username: string;
  email: string;
  token?: string;
}

export const useUserStore = defineStore("user", () => {
  const token = ref<string>(localStorage.getItem("token") || "");
  const userInfo = ref<UserInfo | null>(null);

  const isLoggedIn = computed(() => !!token.value);

  function setToken(newToken: string) {
    token.value = newToken;
    localStorage.setItem("token", newToken);
  }

  function setUserInfo(info: UserInfo) {
    userInfo.value = info;
  }

  async function login(username: string, password: string): Promise<void> {
    const result = await apiLogin(username, password);
    setToken(result.access_token);
    const user = await getMe(result.access_token);
    setUserInfo({
      id: user.id,
      username: user.username,
      email: user.email,
    });
  }

  async function register(
    username: string,
    email: string,
    password: string,
  ): Promise<void> {
    await apiRegister(username, email, password);
  }

  async function fetchMe(): Promise<void> {
    if (!token.value) return;
    const user = await getMe(token.value);
    setUserInfo({
      id: user.id,
      username: user.username,
      email: user.email,
    });
  }

  function logout() {
    token.value = "";
    userInfo.value = null;
    localStorage.removeItem("token");
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    setToken,
    setUserInfo,
    login,
    register,
    fetchMe,
    logout,
  };
});
