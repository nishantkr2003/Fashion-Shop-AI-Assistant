"use client";

type Props = {
  label: string;
  type?: string;
  value: string;
  onChange: (v: string) => void;
};

export default function AuthInput({
  label,
  type = "text",
  value,
  onChange,
}: Props) {
  return (
    <div className="mb-4">
      <label className="text-sm mb-2 block">
        {label}
      </label>

      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full border rounded-xl p-4 outline-none focus:ring">
        </input>
    </div>
  );
}
