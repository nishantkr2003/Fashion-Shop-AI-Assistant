// "use client";

// import { useEffect, useRef } from "react";
// import { useRouter } from "next/navigation";
// import { useAuthStore } from "@/stores/auth";
// import { useChatStore } from "@/stores/chat";
// import Sidebar from "@/components/Sidebar";
// import ChatMessage from "@/components/ChatMessage";
// import ChatInput from "@/components/ChatInput";
// import { Sparkles } from "lucide-react";

// const SUGGESTIONS = [
//   "Show me products under ₹1,000",
//   "What's your return policy?",
//   "Find red Nike shoes in my size",
//   "How long does shipping take?",
// ];

// export default function ChatPage() {
//   const router = useRouter();
//   const { token, user, fetchMe } = useAuthStore();
//   const { messages, sendMessage, activeSessionId } = useChatStore();
//   const messagesEndRef = useRef<HTMLDivElement>(null);

//   useEffect(() => {
//     if (!token) {
//       router.push("/login");
//       return;
//     }
//     if (!user) fetchMe();
//   }, [token]);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages]);

//   const isEmpty = messages.length === 0;

//   return (
//     <div className="flex h-screen overflow-hidden bg-background">
//       <Sidebar />

//       {/* Main area */}
//       <main className="flex-1 flex flex-col overflow-hidden">
//         {isEmpty ? (
//           <div className="flex-1 flex flex-col items-center justify-center px-4">
//             <div className="text-center mb-10">
//               <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary text-primary-foreground text-2xl mb-4">
//                 ✦
//               </div>
//               <h2 className="text-2xl font-semibold mb-2">How can I help?</h2>
//               <p className="text-muted-foreground text-sm max-w-sm">
//                 Ask me about products, check stock, get policy info, or just chat.
//               </p>
//             </div>

//             <div className="grid grid-cols-2 gap-2 max-w-md w-full">
//               {SUGGESTIONS.map((s) => (
//                 <button
//                   key={s}
//                   onClick={() => sendMessage(s)}
//                   className="text-left px-4 py-3 rounded-xl border border-border bg-secondary/40 hover:bg-accent text-sm transition leading-snug"
//                 >
//                   {s}
//                 </button>
//               ))}
//             </div>
//           </div>
//         ) : (
//           <div className="flex-1 overflow-y-auto">
//             <div className="max-w-3xl mx-auto px-4">
//               {messages.map((msg, i) => (
//                 <ChatMessage key={i} message={msg} />
//               ))}
//               <div ref={messagesEndRef} className="h-4" />
//             </div>
//           </div>
//         )}

//         <ChatInput />
//       </main>
//     </div>
//   );
// }

"use client";

import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/auth";
import { useChatStore } from "@/stores/chat";
import Sidebar from "@/components/Sidebar";
import ChatMessage from "@/components/ChatMessage";
import ChatInput from "@/components/ChatInput";
import {
  Sparkles,
  ShoppingBag,
  Package,
  HelpCircle,
  Truck,
} from "lucide-react";

const SUGGESTIONS = [
  {
    icon: ShoppingBag,
    label: "Browse products",
    prompt: "Show me products under ₹1,000",
    color: "text-violet-500",
    bg: "bg-violet-50 hover:bg-violet-100 border-violet-100",
  },
  {
    icon: HelpCircle,
    label: "Return policy",
    prompt: "What's your return policy?",
    color: "text-amber-500",
    bg: "bg-amber-50 hover:bg-amber-100 border-amber-100",
  },
  {
    icon: Package,
    label: "Find by style",
    prompt: "Find red Nike shoes in my size",
    color: "text-rose-500",
    bg: "bg-rose-50 hover:bg-rose-100 border-rose-100",
  },
  {
    icon: Truck,
    label: "Shipping info",
    prompt: "How long does shipping take?",
    color: "text-emerald-500",
    bg: "bg-emerald-50 hover:bg-emerald-100 border-emerald-100",
  },
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
        {/* Top bar (only when there are messages) */}
        {!isEmpty && (
          <div className="flex items-center justify-between px-6 py-3 border-b border-border bg-background/80 backdrop-blur-sm flex-shrink-0">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-lg bg-primary text-primary-foreground flex items-center justify-center text-xs font-bold">
                ✦
              </div>
              <span className="text-sm font-semibold text-foreground">
                Fashion Shop AI
              </span>
            </div>
            <span className="text-xs text-muted-foreground">
              Session active
            </span>
          </div>
        )}

        {isEmpty ? (
          /* ── Empty state ── */
          <div className="flex-1 flex flex-col items-center justify-center px-6 py-12">
            {/* Hero branding */}
            <div className="text-center mb-12">
              <div className="relative inline-flex mb-6">
                <div className="w-16 h-16 rounded-2xl bg-primary text-primary-foreground flex items-center justify-center text-2xl shadow-lg shadow-primary/20">
                  ✦
                </div>
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-emerald-400 rounded-full border-2 border-background animate-pulse" />
              </div>
              <h2 className="text-3xl font-bold tracking-tight text-foreground mb-3">
                How can I help?
              </h2>
              <p className="text-muted-foreground text-sm max-w-sm leading-relaxed">
                Ask about products, check availability, get style advice, or
                understand store policies — instantly.
              </p>
            </div>

            {/* Suggestion cards */}
            <div className="grid grid-cols-2 gap-3 w-full max-w-lg mb-10">
              {SUGGESTIONS.map(({ icon: Icon, label, prompt, color, bg }) => (
                <button
                  key={prompt}
                  onClick={() => sendMessage(prompt)}
                  className={`group flex flex-col items-start gap-3 px-4 py-4 rounded-2xl border ${bg} text-left transition-all duration-200`}
                >
                  <Icon className={`w-5 h-5 ${color}`} />
                  <div>
                    <p className="text-xs font-semibold text-foreground/80">
                      {label}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5 leading-snug">
                      {prompt}
                    </p>
                  </div>
                </button>
              ))}
            </div>

            {/* Subtle hint */}
            <p className="text-xs text-muted-foreground flex items-center gap-1.5">
              <Sparkles className="w-3 h-3" />
              AI Powered · Searches live inventory & policies
            </p>
          </div>
        ) : (
          /* ── Messages ── */
          <div className="flex-1 overflow-y-auto scroll-smooth">
            <div className="max-w-3xl mx-auto px-4 pt-4">
              {messages.map((msg, i) => (
                <ChatMessage key={i} message={msg} />
              ))}
              <div ref={messagesEndRef} className="h-6" />
            </div>
          </div>
        )}

        {/* Input */}
        <ChatInput />
      </main>
    </div>
  );
}