from twin_talk_engine.tools.artist import get_artists_info, get_lineup_info
from twin_talk_engine.tools.events import get_latest_alerts_info
from twin_talk_engine.tools.points_of_interest import get_points_of_interest_info
from twin_talk_engine.tools.schemas import TOOLS
from twin_talk_engine.tools.stages import get_stages_info

TOOL_REGISTRY = {
    "get_artists_info": get_artists_info,
    "get_lineup_info": get_lineup_info,
    "get_latest_alerts_info": get_latest_alerts_info,
    "get_stages_info": get_stages_info,
    "get_points_of_interest_info": get_points_of_interest_info,
}
