import requests


def get_stages_info() -> str:
    url = "https://twin-central-server.onrender.com/api/stages"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        stages = response.json()
        if not stages:
            return "There are currently no active festival stages available."

        lines = ["Here is the current live information about the festival stages:"]
        for stage in stages:
            name = stage.get("name", "Unknown Stage")
            zone = stage.get("zoneCode", "UNKNOWN")
            crowd = stage.get("currentCrowd", 0)
            capacity = stage.get("capacity", 0)
            overcrowded = stage.get("overcrowded", False)
            status = "currently overcrowded" if overcrowded else "operating normally"
            lines.append(
                f"- {name} (zone {zone}) has {crowd} people "
                f"out of a maximum capacity of {capacity} and is {status}."
            )
        lines.append(
            "Use this information to answer user questions about crowd levels, stage capacity, and busy areas."
        )
        return "\n".join(lines)

    except requests.RequestException as e:
        return f"Unable to retrieve live stage information right now. Error: {str(e)}"
