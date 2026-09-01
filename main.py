import asyncio
from scan import get_media_info
from config import get_network

async def main():
    network = await get_network()
    
    while True:
        media_info = await get_media_info()
        if await is_valid_track(media_info):
            network.update_now_playing(
            artist=media_info['artist'],
            title=media_info['title'],
        )

        # Scan every 30 seconds
        await asyncio.sleep(30)

async def is_valid_track(info):
    # Reject if any field is missing
    required_fields = ["title", "artist", "status", "app"]
    for field in required_fields:
        if not info[field]:
            print(f"Track not scrobbled, missing {field}.")
            return False
    return True

if __name__ == "__main__":
    asyncio.run(main())