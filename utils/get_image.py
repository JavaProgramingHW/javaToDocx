import asyncio

from carbon import Carbon

async def from_carbon(result, file, client):
    img = await client.create(result)
    return img

def get_image(result, file):
    client = Carbon(language="Plain Text")
    path = asyncio.run(from_carbon(result, file, client))
    return path