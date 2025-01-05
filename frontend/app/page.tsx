"use client";
import BeginChat from "@/components/BeginChat";
import { createChat } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const handleSubmit = async (input: string) => {
    try {
      const { id } = await createChat(input);
      router.push(`/chat/${id}?prompt=${encodeURIComponent(input)}`);
    } catch (error) {
      console.error("Failed to create chat:", error);
      // You might want to show an error message to the user here
    }
  };

  return (
    <div>
      <main className="flex h-screen bg-gray-100 items-center justify-center">
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-4xl font-bold mb-8 text-gray-800">
            What does your next music playlist look like?
          </h1>
          <BeginChat handleSubmit={handleSubmit} />
        </div>
      </main>
      <footer className=""></footer>
    </div>
  );
}
