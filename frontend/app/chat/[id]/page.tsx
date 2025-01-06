import ChatContainer from "@/components/ChatContainer";
import { getChatHistory, sendChatMessage, type Message } from "@/lib/api";

interface ChatPageProps {
  params: Promise<{
    id: string;
  }>;
  searchParams: Promise<{
    prompt?: string;
  }>;
}

export default async function ChatPage({
  params,
  searchParams,
}: ChatPageProps) {
  const { id } = await params;
  const { prompt } = await searchParams;
  const initialPrompt = prompt ? decodeURIComponent(prompt) : undefined;

  // Try to get existing chat history
  let messages: Message[] = [];
  try {
    messages = await getChatHistory(id);

    // If no history exists and we have an initial prompt, create the chat
    if (messages.length === 0 && initialPrompt) {
      const response = await sendChatMessage(id, initialPrompt);
      messages = [
        {
          content: initialPrompt,
          timestamp: new Date().toISOString(),
          role: "user",
        },
        response,
      ];
    }
  } catch (error) {
    console.error("Failed to load chat:", error);
  }

  return <ChatContainer conversationId={id} initialMessages={messages} />;
}
