from twin_talk_engine.tools.artist import get_artist_info
from twin_talk_engine.tools.events import get_live_events

TOOL_REGISTRY = {
    "get_artist_info": get_artist_info,
    "get_live_events": get_live_events,
}
