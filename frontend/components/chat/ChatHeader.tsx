"use client";

import Brand from "@/components/Brand";

export default function ChatHeader() {
  return (
    <div className="h-20 px-8 glass border-b flex items-center justify-between">
      <Brand />
      <div className="text-sm text-gray-500">
        Online
      </div>
    </div>
  );
}
