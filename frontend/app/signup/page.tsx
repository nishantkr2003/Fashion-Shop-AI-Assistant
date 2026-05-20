"use client";

import { useState } from "react";

import { useRouter } from "next/navigation";

import Link from "next/link";

import AuthCard from "@/components/auth/AuthCard";

import AuthInput from "@/components/auth/AuthInput";

import AuthHeader from "@/components/auth/AuthHeader";

export default function Signup() {
  const router = useRouter();

  const [full_name, setName] = useState("");

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  async function submit() {
    try {
      setLoading(true);

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/register`,

        {
          method: "POST",

          credentials: "include",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            full_name,

            email,

            password,
          }),
        },
      );

      if (res.ok) {
        router.replace("/chat");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="h-screen bg-gray-50 flex items-center justify-center">
      <AuthCard>
        <AuthHeader />

        <AuthInput label="Full Name" value={full_name} onChange={setName} />

        <AuthInput label="Email" value={email} onChange={setEmail} />

        <AuthInput
          label="Password"
          type="password"
          value={password}
          onChange={setPassword}
        />

        <button
          onClick={submit}
          className="w-full bg-black text-white rounded-xl p-4 mt-2">
          {loading ? "Creating..." : "Create Account"}
        </button>

        <div className="mt-6 text-center text-sm">
          <span className="text-gray-500">
            Already have an account?
          </span>

          <Link href="/login"
            className="ml-2 font-semibold text-indigo-600 hover:underline">
            Login
          </Link>
        </div>
      </AuthCard>
    </div>
  );
}
