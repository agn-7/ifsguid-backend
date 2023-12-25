import g4f
import traceback

from .schemas import Interaction

g4f.debug.logging = True
g4f.check_version = False


async def generate_ai_response(content: str, interaction: Interaction) -> str:
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.ModelUtils.convert[interaction.settings.model],
            messages=[
                {"role": "system", "content": interaction.settings.prompt},
                {"role": "user", "content": content},
            ],
        )
        return response
    except Exception:
        traceback.print_exc()
        return "error!"
