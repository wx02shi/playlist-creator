"use client";
import { useEffect, useState } from "react";
import Message from "./Message";
import {
  type Message as MessageType,
  type Tracks,
  sendChatMessage,
  getChatTracks,
} from "@/lib/api";

interface ChatInterfaceProps {
  conversationId: string;
  initialMessages: MessageType[];
  onTracksUpdate: (tracks: Tracks) => void;
}

const ChatInterface = ({
  conversationId,
  initialMessages,
  onTracksUpdate,
}: ChatInterfaceProps) => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    if (initialMessages && initialMessages.length > 0) {
      setMessages(initialMessages);
      updateTracks();
    }
  }, [initialMessages]);

  const updateTracks = async () => {
    try {
      const tracks = await getChatTracks(conversationId);
      onTracksUpdate(tracks);
    } catch (error) {
      console.error("Failed to fetch tracks:", error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: MessageType = {
      content: input,
      timestamp: new Date().toISOString(),
      role: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput(""); // Clear input after sending

    try {
      const response = await sendChatMessage(conversationId, input);
      setMessages((prev) => [...prev, response]);
      await updateTracks();
    } catch (error) {
      console.error("Failed to send message:", error);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4">
        <div className="flex flex-col space-y-4">
          {messages.map((message, index) => (
            <Message key={index} message={message} />
          ))}
        </div>
      </div>

      <div className="border-t p-4">
        <form className="w-full px-4" onSubmit={handleSubmit}>
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
      </div>
    </div>
  );
};

export default ChatInterface;
