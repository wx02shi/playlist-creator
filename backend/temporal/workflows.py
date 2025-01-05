# workflows.py
from datetime import timedelta
import os
import sys
from typing import List
from dotenv import load_dotenv
from temporalio import workflow
import asyncio

load_dotenv()
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Change to the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from src.models.audio import AudioBase

# Import activity through sandbox
with workflow.unsafe.imports_passed_through():
    from src.activities.parse_audio import parse_audio


@workflow.defn
class BatchAudioProcessing:
    @workflow.run
    async def run(self, audios: List[AudioBase]):

        # Process files in parallel
        tasks = []
        for audio in audios:
            task = workflow.execute_activity(
                parse_audio,
                audio,
                start_to_close_timeout=timedelta(minutes=5),
            )
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results
