from dotenv import load_dotenv

load_dotenv()

from src.models.audio import AudioBase

from backend.activities.parse_audio import parse_audio
from src.database.tracks import create_track


audio = AudioBase(
    path="music/still_feel.mp3",
    title="still feel.",
    artists=["half alive"],
    collection="Now, Not Yet",
)


res = parse_audio(audio)


# res = create_track(audio, "this is a test description", [1, 2, 3, 4, 5])

print(res)
