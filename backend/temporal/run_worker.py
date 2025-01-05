# run_worker.py
import asyncio
import os
import sys
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import BatchAudioProcessing

# # Get the current directory
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Change to the parent directory
# parent_dir = os.path.dirname(current_dir)

# # Add the parent directory to sys.path
# sys.path.insert(0, parent_dir)
from src.activities.parse_audio import parse_audio


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="audio-processing-queue",
        workflows=[BatchAudioProcessing],
        activities=[parse_audio],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
