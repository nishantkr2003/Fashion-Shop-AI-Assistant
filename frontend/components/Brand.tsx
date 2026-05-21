"use client";

export default function Brand() {
  return (
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-2xl bg-black text-white flex items-center       justify-center">
        F
      </div>
      <div>
        <h1 className="text-xl font-bold brand-gradient">
          Fashion Shop AI
        </h1>
        <p className="text-xs text-gray-500">
          Personal Shopping Assistant
        </p>
      </div>
    </div>
  );
}
