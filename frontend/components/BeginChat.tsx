"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

interface BeginChatProps {
  handleSubmit?: (input: string) => void;
}

const BeginChat = ({ handleSubmit = () => {} }: BeginChatProps) => {
  const [input, setInput] = useState("");

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSubmit(input);
    setInput("");
  };

  return (
    <form className="w-full max-w-4xl px-4" onSubmit={onSubmit}>
      <div className="flex items-center gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-4 text-lg rounded-lg border border-grey-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="I want to listen to..."
        />
        <button
          type="submit"
          className="p-4 bg-blue-500 text-white rounded-full hover:bg-blue-600 h-14 w-14 flex items-center justify-center flex-shrink-0"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
            />
          </svg>
        </button>
      </div>
    </form>
  );
};

export default BeginChat;
