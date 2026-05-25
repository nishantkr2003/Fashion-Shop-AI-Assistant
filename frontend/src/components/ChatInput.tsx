"use client";

import { useState, useRef, useEffect } from "react";
import { ArrowUp, Square } from "lucide-react";
import { useChatStore } from "@/stores/chat";

export default function ChatInput() {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { sendMessage, isStreaming, stopStream } = useChatStore();

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 200) + "px";
  }, [value]);

  const handleSubmit = async () => {
    const trimmed = value.trim();
    if (!trimmed || isStreaming) return;
    setValue("");
    await sendMessage(trimmed);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="px-4 py-4 max-w-3xl mx-auto w-full">
      <div className="flex items-end gap-2 bg-secondary/60 border border-border rounded-2xl px-4 py-3 focus-within:ring-2 focus-within:ring-ring transition">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about products, policies, or anything else…"
          rows={1}
          disabled={isStreaming}
          className="flex-1 resize-none bg-transparent text-sm outline-none placeholder:text-muted-foreground disabled:opacity-50 max-h-[200px] leading-relaxed"
        />
        <button
          onClick={isStreaming ? stopStream : handleSubmit}
          disabled={!isStreaming && !value.trim()}
          className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition ${
            isStreaming
              ? "bg-primary text-primary-foreground hover:opacity-80"
              : value.trim()
              ? "bg-primary text-primary-foreground hover:opacity-80"
              : "bg-muted text-muted-foreground cursor-not-allowed"
          }`}
        >
          {isStreaming ? <Square className="w-3.5 h-3.5" /> : <ArrowUp className="w-4 h-4" />}
        </button>
      </div>
      <p className="text-center text-xs text-muted-foreground mt-2">
        AI can make mistakes. Check important info.
      </p>
    </div>
  );
}
