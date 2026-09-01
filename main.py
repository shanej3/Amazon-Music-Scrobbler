import asyncio
from scan import get_media_info

async def main():
    while True:
        media_info = await get_media_info()
        if await is_valid_track(media_info):
            print(f"[{media_info['status']}] {media_info['title']} - {media_info['artist']}")

        # Scan every 1 second
        await asyncio.sleep(1)

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