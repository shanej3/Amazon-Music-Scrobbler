import asyncio
from scan import get_media_info

async def main():
    while True:
        media_info = await get_media_info()
        if media_info:
            print(f"[{media_info['status']}] {media_info['title']} - {media_info['artist']}")
        
        # Scan every 10 second
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())