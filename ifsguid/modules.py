import g4f

g4f.debug.logging = True
g4f.check_version = False


def generate_ai_response(
    content: str, model: str = "GPT4"
) -> str:  # TODO: use async version for future
    return g4f.ChatCompletion.create(
        model=g4f.models.gpt_4 if model == "GPT4" else g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": content}],
    )
