import asyncio

from carbon import Carbon

async def from_carbon(result, client):
    img = await client.create(result)
    return img

def get_image(result):
    client = Carbon(
        language="Plain Text",
        colour="rgba(255, 255, 255, 100)",
        horizontal_padding="10px",
        vertical_padding="10px",
        window_controls=True,
    )
    path = asyncio.run(from_carbon(result, client))
    return path