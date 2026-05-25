"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Message } from "@/stores/chat";
import { Bot, User } from "lucide-react";

interface Props {
  message: Message;
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 py-5 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm ${
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-secondary border border-border text-muted-foreground"
        }`}
      >
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      {/* Content */}
      <div className={`flex-1 max-w-3xl ${isUser ? "flex justify-end" : ""}`}>
        {isUser ? (
          <div className="inline-block px-4 py-2.5 bg-primary text-primary-foreground rounded-2xl rounded-tr-sm text-sm leading-relaxed max-w-lg">
            {message.content}
          </div>
        ) : (
          <div className="text-sm leading-relaxed">
            {message.content || message.streaming ? (
              <div className="prose-chat">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content + (message.streaming && !message.content.endsWith("▌") ? "▌" : "")}
                </ReactMarkdown>
              </div>
            ) : (
              <div className="flex gap-1">
                <span className="w-2 h-2 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:0ms]" />
                <span className="w-2 h-2 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:150ms]" />
                <span className="w-2 h-2 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:300ms]" />
              </div>
            )}

            {/* Agent badge */}
            {message.agent && !message.streaming && (
              <div className="mt-2 flex items-center gap-1.5">
                <AgentBadge agent={message.agent} confidence={message.confidence} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function AgentBadge({ agent, confidence }: { agent: string; confidence?: number }) {
  const labels: Record<string, string> = {
    sql: "Database",
    rag: "Knowledge Base",
    chat: "AI Chat",
  };
  const colors: Record<string, string> = {
    sql: "bg-blue-500/10 text-blue-600 dark:text-blue-400",
    rag: "bg-purple-500/10 text-purple-600 dark:text-purple-400",
    chat: "bg-green-500/10 text-green-600 dark:text-green-400",
  };

  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${colors[agent] || "bg-muted text-muted-foreground"}`}>
      {labels[agent] || agent}
      {confidence !== undefined && confidence < 0.75 && " · under review"}
    </span>
  );
}
