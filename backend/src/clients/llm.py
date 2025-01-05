from litellm import completion


def helper_agent_completion(instructions, msg, model="gemini/gemini-2.0-flash-exp"):
    print("STARTING AGENT COMPLETION ...")
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": msg},
        ],
    )
    print("COMPLETION RESPONSE: ", response)
    return response.choices[0].message.content
