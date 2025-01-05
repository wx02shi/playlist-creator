"use client";
import { useState } from "react";
import ChatInterface from "./ChatInterface";
import SongList from "./SongList";
import { type Message, type Tracks } from "@/lib/api";

interface ChatContainerProps {
  conversationId: string;
  initialMessages: Message[];
}

export default function ChatContainer({
  conversationId,
  initialMessages,
}: ChatContainerProps) {
  const [tracks, setTracks] = useState<Tracks>({
    suggested: [],
    pinned: [],
  });

  return (
    <div className="h-screen flex">
      <div className="flex-1 max-w-4xl">
        <ChatInterface
          conversationId={conversationId}
          initialMessages={initialMessages}
          onTracksUpdate={setTracks}
        />
      </div>
      <div className="w-96 border-l border-gray-200 p-4 overflow-y-auto">
        <SongList suggested={tracks.suggested} pinned={tracks.pinned} />
      </div>
    </div>
  );
}
