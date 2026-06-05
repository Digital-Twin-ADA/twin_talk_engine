import requests


def get_points_of_interest_info() -> str:
    url = "https://twin-central-server.onrender.com/api/points-of-interest"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        points_of_interest_info = response.json()
        if not points_of_interest_info:
            return "There is currently no information available about the points of interest of the festival."

        lines = ["Here are the current points of interest:"]
        for point_of_interest in points_of_interest_info:
            name = point_of_interest.get("name", "Unknown Artist")
            type = point_of_interest.get("type", "Unknown Tyoe")
            description = point_of_interest.get(
                "description", "No description available."
            )
            zone_code = point_of_interest.get("zoneCode", "Unknown Zone Code")
            opening_hours = point_of_interest.get(
                "openingHours", "Unknown Opening Hours"
            )

            lines.append(
                f"- {name} is a {type} described as {description} in zone {zone_code}. Opening hours: {opening_hours}."
            )
        lines.append(
            "Use this information to answer user questions about points of interest."
        )
        return "\n".join(lines)

    except requests.RequestException as e:
        return f"Unable to retrieve information about points of interest right now. Error: {str(e)}"
