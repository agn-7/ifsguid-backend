import g4f
import traceback

g4f.debug.logging = True
g4f.check_version = False


async def generate_ai_response(
    content: str, model: g4f.Model = g4f.models.default
) -> str:
    try:
        response = await g4f.ChatCompletion.create_async(
            model=model,
            messages=[{"role": "human", "content": content}],
        )
        return response
    except Exception:
        traceback.print_exc()
        return "error!"
