"use client";

export default function AuthCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="glass w-[460px] rounded-[32px] p-10 shadow-xl">
      {children}
    </div>
  );
}
