import scan
import datetime

times_scanned = 0
current_track = None

async def update_now_playing(network): 
    media_info = await scan.get_media_info()
    
    if await is_valid_track(media_info):
        network.update_now_playing(
            artist=media_info['artist'],
            title=media_info['title'],
        )

async def attempt_to_scrobble(network):
    global current_track, times_scanned
    scanned_track = await scan.get_media_info()

    if scanned_track["status"] != "Playing":
        return

    # if track has been scanned 4 times and is different from the current track, scrobble it
    if await is_valid_track(scanned_track):
        if current_track != scanned_track:
            print(f"[INFO] New track detected: {scanned_track['artist']} - {scanned_track['title']}")
            if times_scanned > 4:
                await scrobble_track(network, current_track)
                print(f"[INFO] Scrobbled track: {current_track['artist']} - {current_track['title']}")
            current_track = scanned_track
            times_scanned = 1
        else:
            times_scanned += 1
    return

async def scrobble_track(network, track):
    network.scrobble(
        artist=track['artist'],
        title=track['title'],
        timestamp=int(datetime.datetime.now().timestamp())
    )
    
async def is_valid_track(info):
    # reject if not Amazon Music
    app = info.get("app", "").lower()
    if not ("amazon" in app and "music" in app):
        print(f"[WARN] Track not scrobbled, invalid app:: {info.get('app')}")
        return False 

    # Reject if any field is missing
    required_fields = ["title", "artist", "status"]
    for field in required_fields:
        if not info.get(field):
            print(f"[WARN] Track not scrobbled, missing {field}.")
            return False
    return True