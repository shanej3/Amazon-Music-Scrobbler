import asyncio
import config
import lastfm

async def main():
    network = await config.get_network()
    
    while True:
        await lastfm.update_now_playing(network)
        await lastfm.attempt_to_scrobble(network)

        # Scan every 15 seconds
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(main())