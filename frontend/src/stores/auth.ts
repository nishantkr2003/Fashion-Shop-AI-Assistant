import { create } from "zustand";
import { authApi } from "@/lib/api";

interface User {
  id: number;
  full_name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
  setToken: (token: string) => void;
  login: (email: string, password: string) => Promise<void>;
  register: (full_name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: typeof window !== "undefined" ? localStorage.getItem("token") : null,
  loading: false,
  error: null,

  setToken: (token) => {
    localStorage.setItem("token", token);
    set({ token });
  },

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const res = await authApi.login({ email, password });
      const token = res.data.access_token;
      localStorage.setItem("token", token);
      set({ token, loading: false });
      await get().fetchMe();
    } catch (err: any) {
      set({ loading: false, error: err.response?.data?.detail || "Login failed" });
      throw err;
    }
  },

  register: async (full_name, email, password) => {
    set({ loading: true, error: null });
    try {
      const res = await authApi.register({ full_name, email, password });
      const token = res.data.access_token;
      localStorage.setItem("token", token);
      set({ token, loading: false });
      await get().fetchMe();
    } catch (err: any) {
      set({ loading: false, error: err.response?.data?.detail || "Registration failed" });
      throw err;
    }
  },

  logout: () => {
    localStorage.removeItem("token");
    set({ user: null, token: null });
    window.location.href = "/login";
  },

  fetchMe: async () => {
    try {
      const res = await authApi.me();
      set({ user: res.data });
    } catch {
      set({ user: null });
    }
  },

  clearError: () => set({ error: null }),
}));
