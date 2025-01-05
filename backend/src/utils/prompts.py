description_prompt = """You are an intelligent music analysis agent specialized in understanding music. Your task is to write a comprehensive description for a given audio track. Provide as much detail as possible, as your response will eventually be analyzed by someone else and compared against other descriptions.

You will receive basic information about the track in the following format:
<track_title>
{{title}}
</track_title>
<track_artists>
{{artists}}
</track_artists>
<track_collection>
{{collection_title}}
</track_collection>

Note: track_collection refers to whether the track is part of an Album or EP. If it is not provided, then this track is a single. 

Afterwards, you will be provided the track audio itself.

Your goal is to write a detailed description of the music track. Follow these steps:
1. Identify relevant genres present in the music. Usually there is a dominant genre, but it is possible for sub-genres or genre mixes to be incorporated
2. Identify instruments used in the track
3. Describe the mood, energy, or vibe of the track. How do you feel when you listen to it?
4. If the track, summarize the lyrics and what the artists are saying
5. Determine if the artists are trying to convey any meaning in this track, and explain their message if it exists. 

Wrap your analysis in <analysis> tags. Include the following:
- Basic details about the track: title, artists, collection, genres
- Mood, energy, vibe, and the feeling of the track
- Unique instruments and sounds, if prominent
- Summary of the lyrics, if present
- Explanation of the artists' intent, if present

After your analysis, provide your final summary of all the details you discussed.

Output only the final summary, without any additional text or explanation."""


track_details = """<track_title>{title}</track_title>
<track_artists>{artists}</track_artists>
<track_collection>{collection_title}</track_collection>"""


summarize_requirements = """Your task is to create a comprehensive summary for a user’s request.
The user believes they are interacting with a chat bot, but you are not the chat bot. You are an intermediary who will create a summary of the user's request, which will be passed to a request handler agent.
The request handler agent does not interact with the user, so be thorough, concise, and descriptive in your summary so that they can understand all of the user's request.
The user will request to create a music playlist that closely matches and follows their description. 

Your goal is to write a detailed summary of the user’s request and description of their ideal playlist. Identify the user’s requirements and preferences. Follow these rules:
- DO NOT respond to the user’s request. Create a clear and concise summary of their requirements
- DO NOT create a list of points in your response. Use in natural language

Output only the final summary, without any additional text or explanation."""

update_requirements_summary = """Your task is to refine a comprehensive summary of a user’s request.
The user believes they are interacting with a chat bot, but you are not the chat bot. You are an intermediary who will create a summary of the user's request, which will be passed to the actual chat bot. 
The request handler agent does not interact with the user, so be thorough, concise, and descriptive in your summary so that they can understand all of the user's request.
The user will request to create a music playlist that closely matches and follows their description. 
The user believes they are continuing their conversation with the chat bot, and are looking to change their requirements for their playlist.

The following is a summary of the user's previous requirements:
<summary>
{summary}
</summary>

Your goal is to update the detailed summary of the user’s request and description of their ideal playlist. Identify the user’s new requirements and preferences. Follow these rules:
- DO NOT respond to the user’s request. Create a clear and concise summary of their requirements
- DO NOT create a list of points in your response. Use in natural language
- Update the summary with the the new requirements
- Replace any old requirements if the new ones contradict 

Output only the final summary, without any additional text or explanation.
"""

inject_pinned = """Your task is to create a concise summary of some given music tracks.
For context, a user has requested to create a music playlist that closely matches and follows their description.
The user has pinned some tracks, indicating that those ones highly match their preference.

You will receive a list of pinned tracks in the following format:
<pinned_tracks>
[
    {
        "title": "Track Title",
        "artists": ["Artist 1", "Artist 2"],
        "collection": "Collection Title",
        "description": "Description of the track"
    },
    {
        "title": "Track Title",
        "artists": ["Artist 1", "Artist 2"],
        "collection": "Collection Title",
        "description": "Description of the track"
    }
]
</pinned_tracks>

Your goals is to write a detailed summary of user's the pinned and preferred tracks. Identify similarities between the descriptions of the pinned tracks.

Wrap your analysis in <analysis> tags. Do the following:
- Identify any common genres, moods, or themes across the pinned tracks
- Identify any common instruments and sounds
- Identify any common lyrics or messages
- Identify any common artist intent or meaning
- Identify any common artists or collections

After your analysis, provide your final summary of all the details you discussed.

Output only the final summary, without any additional text or explanation.
"""

compare_summaries = """Your task is to compare two segments of text, and respond to a user's request.
For context, the user has requested to create a music playlist that closely matches and follows their description.
Both texts are summaries of the user's requirements and preferences, but the second one is a newer version.

The following is the user's latest request:
<latest_request>
{latest_request}
</latest_request>

You will receive two summaries in the following format:
<old_summary>
{{old_summary}}
</old_summary>
<new_summary>
{{new_summary}}
</new_summary>

Your goal is to respond to the user and describe the differences between the two summaries. Follow these rules:
- Use colloquial and informal language to respond to the user's latest request
- Identify the differences in the two summaries
- Describe the differences as if these are changes that you made to the music playlist

Output only the final response, without any additional text or explanation.
"""
