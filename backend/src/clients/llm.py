from litellm import completion


def helper_agent_completion(instructions, msg, model="gemini/gemini-2.0-flash-exp"):
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": msg},
        ],
    )
    return response["messages"][0]["content"]
