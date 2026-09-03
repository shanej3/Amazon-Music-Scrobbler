import scan
import datetime

times_scanned = 0
current_track = None

async def update_now_playing(network): 
    track_info = await scan.get_track_info()
    
    if await is_valid_track(track_info):
        network.update_now_playing(
            artist=track_info['artist'],
            title=track_info['title'],
        )

async def attempt_to_scrobble(network):
    global current_track, times_scanned
    scanned_track = await scan.get_track_info()

    if await is_amazon_music(scanned_track) is False:
        return

    if scanned_track["status"] != "Playing":
        return

    # if track has been scanned 4 times and is different from the newly scanned track, scrobble it
    if current_track != scanned_track:
        if times_scanned > 4:
            await scrobble_track(network, current_track)
            print(f"[INFO] Scrobbled track: {current_track['artist']} - {current_track['title']}")

        if await is_valid_track(scanned_track):
            print(f"[INFO] New track detected: {scanned_track['artist']} - {scanned_track['title']}")
            current_track = scanned_track
            times_scanned = 1
        return
    times_scanned += 1

async def scrobble_track(network, track):
    network.scrobble(
        artist=track['artist'],
        title=track['title'],
        timestamp=int(datetime.datetime.now().timestamp())
    )
    
async def is_valid_track(track_info):
    # Reject if any field is missing
    required_fields = ["title", "artist", "status"]
    for field in required_fields:
        if not track_info.get(field):
            print(f"[WARN] Track not valid, missing {field}.")
            return False
    return True

async def is_amazon_music(track_info):
     # reject if not Amazon Music
    app = track_info.get("app", "").lower()
    if not ("amazon" in app and "music" in app):
        print(f"[WARN] Track not valid, invalid app: {track_info.get('app')}")
        return False 