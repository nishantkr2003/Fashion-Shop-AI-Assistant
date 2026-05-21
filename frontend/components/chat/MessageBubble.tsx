"use client";

type Props = {
  role: string;

  content: string;
};

export default function MessageBubble({
  role,
  content,
}: Props) {
  const user = role === "user";

  return (
    <div className={`flex mb-6${user ? "justify-end" : "justify-start"}`}>
      <div 
      className={`max-w-[70%] rounded-3xl p-5 text-sm leading-7${user ? "bg-black text-white" : "bg-gray-100"}`}>
        {content}
      </div>
    </div>
  );
}
