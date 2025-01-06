import { env } from "@/config/env";

export async function createChat(prompt: string): Promise<{ id: string }> {
  const response = await fetch(`${env.apiUrl}/chat/create`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error("Failed to create chat");
  }

  return response.json();
}

export interface Message {
  content: string;
  timestamp: string;
  role: "user" | "assistant";
}

export interface Track {
  id: number;
  title: string;
  artists: string[];
  collection: {
    name: string;
    imageUrl: string;
  };
  description: string;
}

export interface Tracks {
  suggested: Track[];
  pinned: Track[];
}

export interface Conversation {
  id: string;
  req_summary: string;
}

export async function getAllChats(): Promise<Conversation[]> {
  const response = await fetch(`${env.apiUrl}/all-chats`);

  if (!response.ok) {
    throw new Error("Failed to fetch conversations");
  }

  const data = await response.json();
  return data.conversations;
}

export async function getChatTracks(id: string): Promise<Tracks> {
  const response = await fetch(`${env.apiUrl}/chat/${id}/tracks`);

  if (!response.ok) {
    throw new Error("Failed to fetch track suggestions");
  }

  return response.json();
}

export async function getChatHistory(id: string): Promise<Message[]> {
  const response = await fetch(`${env.apiUrl}/chat/${id}`);

  if (!response.ok) {
    if (response.status === 404) {
      return [];
    }
    throw new Error("Failed to fetch chat history");
  }

  return response.json();
}

export async function sendChatMessage(
  id: string,
  prompt: string
): Promise<Message> {
  const response = await fetch(`${env.apiUrl}/chat/${id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: prompt }),
  });

  if (!response.ok) {
    throw new Error("Failed to send chat message");
  }

  return response.json();
}

export async function pinTrack(conversationId: string, trackId: number) {
  const response = await fetch(
    `${env.apiUrl}/pin/${conversationId}/${trackId}`,
    {
      method: "PUT",
    }
  );
  if (!response.ok) {
    throw new Error("Failed to pin track");
  }
  return response.json();
}
