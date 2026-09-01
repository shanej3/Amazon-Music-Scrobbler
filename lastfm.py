import scan

async def update_now_playing(network): 
    media_info = await scan.get_media_info()
    
    if await is_valid_track(media_info):
        network.update_now_playing(
            artist=media_info['artist'],
            title=media_info['title'],
        )

async def is_valid_track(info):
    # Reject if any field is missing
    required_fields = ["title", "artist", "status", "app"]
    for field in required_fields:
        if not info[field]:
            print(f"Track not scrobbled, missing {field}.")
            return False
    return True