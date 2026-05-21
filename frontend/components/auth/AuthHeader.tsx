"use client";

import Brand from "@/components/Brand";

export default function AuthHeader() {
  return (
    <div className="mb-10">
      <Brand />

      <h1 className="mt-8 text-3xl font-bold">
        Welcome
      </h1>

      <p className="text-gray-500 mt-2">
        Continue to your shopping assistant
      </p>
    </div>
  );
}
