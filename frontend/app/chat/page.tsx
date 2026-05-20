"use client";

import { useEffect, useState } from "react";

import { useRouter } from "next/navigation";

import { validateSession } from "@/lib/auth";

import Sidebar from "@/components/chat/ChatSidebar";

import ChatHeader from "@/components/chat/ChatHeader";

import ChatWindow from "@/components/chat/ChatWindow";

import ChatInput from "@/components/chat/ChatInput";

export default function ChatPage() {
  const router = useRouter();

  const [ready, setReady] = useState(false);

  useEffect(() => {
    check();
  }, []);

  async function check() {
    const ok = await validateSession();

    if (!ok) {
      router.replace("/login");

      return;
    }

    setReady(true);
  }

  if (!ready) {
    return (
      <div className="h-screen flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="h-screen flex">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <ChatHeader />

        <ChatWindow />

        <ChatInput />
      </div>
    </div>
  );
}
