import requests


def get_artists_info() -> str:
    url = "https://twin-central-server.onrender.com/api/artists"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        artists_info = response.json()
        if not artists_info:
            return "There is currently no information available about the artists of the festival."

        lines = [
            "Here is the current live information about the artists of the festival:"
        ]
        for artist_info in artists_info:
            name = artist_info.get("name", "Unknown Artist")
            genre = artist_info.get("genre", "Unknown Genre")
            description = artist_info.get("bio", "No description available.")
            country = artist_info.get("country", "Unknown Country")
            lines.append(f"- {name} is a {genre} artist from {country}. {description}")
        lines.append("Use this information to answer user questions about artists.")
        return "\n".join(lines)

    except requests.RequestException as e:
        return (
            f"Unable to retrieve information about artists right now. Error: {str(e)}"
        )


def get_lineup_info() -> str:
    url = "https://twin-central-server.onrender.com/api/lineup"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        lineup_info = response.json()
        if not lineup_info:
            return (
                "There is currently no lineup information available for the festival."
            )

        lines = ["Here is the current live lineup information for the festival:"]

        for event in lineup_info:
            artist_name = event.get("artistName", "Unknown Artist")
            artist_genre = event.get("artistGenre", "Unknown Genre")
            stage_name = event.get("stageName", "Unknown Stage")
            starts_at = event.get("startsAt", "Unknown Start Time")
            ends_at = event.get("endsAt", "Unknown End Time")
            title = event.get("title", "Untitled Performance")
            status = event.get("status", "Unknown Status")

            lines.append(
                f"- '{title}' by {artist_name} ({artist_genre}) "
                f"will take place on {stage_name} from {starts_at} to {ends_at}. "
                f"Current status: {status}."
            )

        lines.append(
            "Use this information to answer user questions about the festival lineup and schedule."
        )

        return "\n".join(lines)

    except requests.RequestException as e:
        return f"Unable to retrieve lineup information right now. Error: {str(e)}"
