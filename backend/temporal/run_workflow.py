import asyncio
import json
import os
import sys
from temporalio.client import Client
from workflows import BatchAudioProcessing

current_dir = os.path.dirname(os.path.abspath(__file__))

# Change to the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from src.models.audio import AudioBase


async def main():
    client = await Client.connect("localhost:7233")

    # Example batch of files
    music_path = "music/"
    with open(music_path + "tracks.json", "r") as f:
        data = json.load(f)

    data = data["tracks"]
    audio_to_process = [
        AudioBase(
            title=d["title"],
            artists=d["artists"],
            collection=d.get("collection", None),
            path=music_path + d["path"],
        )
        for d in data
    ]

    result = await client.execute_workflow(
        BatchAudioProcessing.run,
        audio_to_process,
        id=f"audio-batch-processing",
        task_queue="audio-processing-queue",
    )

    print(f"Processing results: {result}")


if __name__ == "__main__":
    asyncio.run(main())
