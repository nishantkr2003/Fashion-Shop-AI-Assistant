"use client";

export default function UserProfile() {
  async function logout() {
    await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/auth/logout`,
      {
        method: "POST",
        credentials: "include",
      },
    );
    window.location.href = "/login";
  }

  return (
    <div className="p-5 border-t">
      <button
        onClick={logout}
        className="w-full rounded-xl border p-3 text-white bg-black">
        Logout
      </button>
    </div>
  );
}
