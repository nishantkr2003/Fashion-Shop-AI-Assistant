import { create } from "zustand";
import { chatApi, streamChat } from "@/lib/api";

export interface Message {
  id?: number;
  role: "user" | "assistant";
  content: string;
  agent?: string;
  confidence?: number;
  streaming?: boolean;
}

export interface ChatSession {
  id: number;
  title: string;
  created_at: string;
}

interface ChatState {
  sessions: ChatSession[];
  activeSessionId: number | null;
  messages: Message[];
  isStreaming: boolean;
  abortStream: (() => void) | null;

  loadSessions: () => Promise<void>;
  createSession: () => Promise<number>;
  selectSession: (id: number) => Promise<void>;
  deleteSession: (id: number) => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  stopStream: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  sessions: [],
  activeSessionId: null,
  messages: [],
  isStreaming: false,
  abortStream: null,

  loadSessions: async () => {
    const res = await chatApi.listSessions();
    set({ sessions: res.data });
  },

  createSession: async () => {
    const res = await chatApi.createSession();
    const session: ChatSession = res.data;
    set((s) => ({ sessions: [session, ...s.sessions], activeSessionId: session.id, messages: [] }));
    return session.id;
  },

  selectSession: async (id) => {
    set({ activeSessionId: id, messages: [] });
    const res = await chatApi.getMessages(id);
    const messages: Message[] = res.data.map((m: any) => ({
      id: m.id,
      role: m.role,
      content: m.content,
    }));
    set({ messages });
  },

  deleteSession: async (id) => {
    await chatApi.deleteSession(id);
    set((s) => {
      const sessions = s.sessions.filter((sess) => sess.id !== id);
      const activeSessionId = s.activeSessionId === id ? null : s.activeSessionId;
      return { sessions, activeSessionId, messages: activeSessionId === null ? [] : s.messages };
    });
  },

  sendMessage: async (content: string) => {
    const state = get();
    let sessionId = state.activeSessionId;

    if (!sessionId) {
      sessionId = await get().createSession();
    }

    // Add user message immediately
    const userMsg: Message = { role: "user", content };
    const assistantMsg: Message = { role: "assistant", content: "", streaming: true };
    set((s) => ({ messages: [...s.messages, userMsg, assistantMsg], isStreaming: true }));

    const abort = streamChat(
      sessionId,
      content,
      (chunk) => {
        set((s) => {
          const messages = [...s.messages];
          const last = messages[messages.length - 1];
          if (last.streaming) last.content += chunk;
          return { messages };
        });
      },
      (meta) => {
        set((s) => {
          const messages = [...s.messages];
          const last = messages[messages.length - 1];
          if (last.streaming) {
            last.streaming = false;
            last.agent = meta.agent;
            last.confidence = meta.confidence;
          }
          return { messages, isStreaming: false, abortStream: null };
        });
        // Refresh session list (title may have updated)
        get().loadSessions();
      },
      (err) => {
        set((s) => {
          const messages = [...s.messages];
          const last = messages[messages.length - 1];
          if (last.streaming) {
            last.streaming = false;
            last.content = "Sorry, something went wrong. Please try again.";
          }
          return { messages, isStreaming: false, abortStream: null };
        });
      }
    );

    set({ abortStream: abort });
  },

  stopStream: () => {
    const { abortStream } = get();
    if (abortStream) abortStream();
    set((s) => {
      const messages = [...s.messages];
      const last = messages[messages.length - 1];
      if (last.streaming) last.streaming = false;
      return { messages, isStreaming: false, abortStream: null };
    });
  },
}));
