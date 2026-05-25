"use client";

import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/auth";
import { useChatStore } from "@/stores/chat";
import Sidebar from "@/components/Sidebar";
import ChatMessage from "@/components/ChatMessage";
import ChatInput from "@/components/ChatInput";
import { Sparkles } from "lucide-react";

const SUGGESTIONS = [
  "Show me products under ₹1,000",
  "What's your return policy?",
  "Find red Nike shoes in my size",
  "How long does shipping take?",
];

export default function ChatPage() {
  const router = useRouter();
  const { token, user, fetchMe } = useAuthStore();
  const { messages, sendMessage, activeSessionId } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!token) {
      router.push("/login");
      return;
    }
    if (!user) fetchMe();
  }, [token]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const isEmpty = messages.length === 0;

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />

      {/* Main area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {isEmpty ? (
          <div className="flex-1 flex flex-col items-center justify-center px-4">
            <div className="text-center mb-10">
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary text-primary-foreground text-2xl mb-4">
                ✦
              </div>
              <h2 className="text-2xl font-semibold mb-2">How can I help?</h2>
              <p className="text-muted-foreground text-sm max-w-sm">
                Ask me about products, check stock, get policy info, or just chat.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-2 max-w-md w-full">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="text-left px-4 py-3 rounded-xl border border-border bg-secondary/40 hover:bg-accent text-sm transition leading-snug"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto">
            <div className="max-w-3xl mx-auto px-4">
              {messages.map((msg, i) => (
                <ChatMessage key={i} message={msg} />
              ))}
              <div ref={messagesEndRef} className="h-4" />
            </div>
          </div>
        )}

        <ChatInput />
      </main>
    </div>
  );
}
