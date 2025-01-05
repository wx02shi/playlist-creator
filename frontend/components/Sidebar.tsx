"use client";
import { useEffect, useState } from "react";
import { getAllChats, type Conversation } from "@/lib/api";
import Link from "next/link";

const Sidebar = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        setIsLoading(true);
        const chats = await getAllChats();
        console.log("Fetched chats:", chats); // Debug log
        setConversations(chats);
      } catch (error) {
        console.error("Failed to fetch conversations:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchConversations();
  }, []);

  return (
    <div className="w-64 h-full border-r border-gray-200 flex flex-col bg-gray-50">
      <Link
        href="/"
        className="p-4 border-b border-gray-200 text-center hover:bg-gray-100 font-medium text-gray-800"
      >
        Home
      </Link>
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="p-4 text-sm text-gray-500">
            Loading conversations...
          </div>
        ) : conversations.length === 0 ? (
          <div className="p-4 text-sm text-gray-500">No conversations yet</div>
        ) : (
          conversations.map((conv) => (
            <Link
              key={conv.id}
              href={`/chat/${conv.id}`}
              className="block p-4 hover:bg-gray-100 border-b border-gray-200"
            >
              <p className="text-sm text-gray-800 truncate">
                {conv.req_summary || "Untitled Conversation"}
              </p>
            </Link>
          ))
        )}
      </div>
    </div>
  );
};

export default Sidebar;
