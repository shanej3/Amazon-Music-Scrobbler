from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus,
)

async def get_media_info():
    # Request access to the system media controls manager
    manager = await MediaManager.request_async()

    current_session = manager.get_current_session()
    
    if not current_session:
        print("No active media sessions found.")
        return None

    # Fetch track metadata and playback state
    media_properties = await current_session.try_get_media_properties_async()
    playback_info = current_session.get_playback_info()
    
    status_map = {
        PlaybackStatus.PLAYING: "Playing",
        PlaybackStatus.PAUSED: "Paused",
        PlaybackStatus.STOPPED: "Stopped"
    }

    info = {
        "title": media_properties.title,
        "artist": media_properties.artist,
        "status": status_map.get(playback_info.playback_status, "Unknown"),
        "app": current_session.source_app_user_model_id
    }
    
    return info