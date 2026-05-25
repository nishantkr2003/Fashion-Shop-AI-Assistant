"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useChatStore, ChatSession } from "@/stores/chat";
import { useAuthStore } from "@/stores/auth";
import { PencilLine, Trash2, LogOut, MessageSquare } from "lucide-react";

export default function Sidebar() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const { sessions, activeSessionId, loadSessions, createSession, selectSession, deleteSession } =
    useChatStore();

  useEffect(() => {
    loadSessions();
  }, []);

  const handleNewChat = async () => {
    const id = await createSession();
  };

  const handleDelete = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    await deleteSession(id);
  };

  return (
    <aside className="flex flex-col h-full bg-secondary/40 border-r border-border w-[var(--sidebar-width)]">
      {/* Header */}
      <div className="p-3 border-b border-border">
        <div className="flex items-center gap-2 px-2 py-1 mb-1">
          <div className="w-7 h-7 rounded-lg bg-primary text-primary-foreground flex items-center justify-center text-xs font-bold">✦</div>
          <span className="text-sm font-semibold">Fashion Shop AI</span>
        </div>
        <button
          onClick={handleNewChat}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg hover:bg-accent transition text-left"
        >
          <PencilLine className="w-4 h-4" />
          New chat
        </button>
      </div>

      {/* Session list */}
      <div className="flex-1 overflow-y-auto p-2 space-y-0.5">
        {sessions.length === 0 && (
          <p className="text-xs text-muted-foreground text-center py-8 px-4">
            No conversations yet. Start a new chat!
          </p>
        )}
        {sessions.map((session) => (
          <SessionItem
            key={session.id}
            session={session}
            active={session.id === activeSessionId}
            onSelect={() => selectSession(session.id)}
            onDelete={(e) => handleDelete(e, session.id)}
          />
        ))}
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-border">
        <div className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-accent transition group">
          <div className="w-7 h-7 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-medium flex-shrink-0">
            {user?.full_name?.charAt(0).toUpperCase() || "U"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium truncate">{user?.full_name || "User"}</p>
            <p className="text-xs text-muted-foreground truncate">{user?.email || ""}</p>
          </div>
          <button
            onClick={logout}
            className="opacity-0 group-hover:opacity-100 transition p-1 rounded hover:bg-destructive/10 hover:text-destructive"
            title="Logout"
          >
            <LogOut className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </aside>
  );
}

function SessionItem({
  session,
  active,
  onSelect,
  onDelete,
}: {
  session: ChatSession;
  active: boolean;
  onSelect: () => void;
  onDelete: (e: React.MouseEvent) => void;
}) {
  return (
    <div
      onClick={onSelect}
      className={`group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition text-sm ${
        active ? "bg-accent font-medium" : "hover:bg-accent/50"
      }`}
    >
      <MessageSquare className="w-3.5 h-3.5 flex-shrink-0 text-muted-foreground" />
      <span className="flex-1 truncate text-xs">{session.title}</span>
      <button
        onClick={onDelete}
        className="opacity-0 group-hover:opacity-100 transition p-1 rounded hover:bg-destructive/10 hover:text-destructive flex-shrink-0"
      >
        <Trash2 className="w-3 h-3" />
      </button>
    </div>
  );
}
