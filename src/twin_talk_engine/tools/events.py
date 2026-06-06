from datetime import datetime, timezone

import requests


def get_latest_alerts_info() -> str:
    url = "https://twin-central-server.onrender.com/api/alerts?page=0&size=3&sort=createdAt,desc"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        alerts_data = response.json()
        alerts = alerts_data.get("content", [])

        if not alerts:
            return "There are currently no recent festival alerts."

        lines = ["Here are the latest festival alerts:"]

        now = datetime.now(timezone.utc)

        for alert in alerts:
            alert_type = alert.get("type", "Unknown")
            message = alert.get("message", "No message provided.")
            stage_id = alert.get("stageId", "Unknown Stage")
            severity = alert.get("severity", "UNKNOWN")
            created_at = alert.get("createdAt")
            resolved = alert.get("resolved", False)

            # Optional: human-friendly recent time
            time_info = ""
            if created_at:
                try:
                    created_dt = datetime.fromisoformat(
                        created_at.replace("Z", "+00:00")
                    )
                    minutes_ago = int((now - created_dt).total_seconds() // 60)

                    if minutes_ago < 1:
                        time_info = "just now"
                    elif minutes_ago < 60:
                        time_info = f"{minutes_ago} minutes ago"
                    else:
                        hours_ago = minutes_ago // 60
                        time_info = f"{hours_ago} hours ago"
                except Exception:
                    time_info = created_at

            status = "Resolved" if resolved else "Active"

            lines.append(
                f"- [{status}] {alert_type} alert at stage {stage_id}: "
                f"{message}. Severity: {severity}. Reported {time_info}."
            )

        lines.append(
            "Use this information to answer user questions about recent festival alerts and incidents."
        )

        return "\n".join(lines)

    except requests.RequestException as e:
        return f"Unable to retrieve festival alerts right now. Error: {str(e)}"


def get_current_events_for_each_stage() -> str:
    url = "https://twin-central-server.onrender.com/api/events/current"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        stages = response.json()

        if not stages:
            return "No information about stages or events is currently available."

        lines = ["Here are the current events happening at each stage:"]

        for stage in stages:
            stage_name = stage.get("stageName", "Unknown Stage")
            events = stage.get("events", [])

            if not events:
                lines.append(f"- {stage_name}: No event is currently taking place.")
            else:
                event_details = []
                for event in events:
                    title = event.get("title", "Unknown Event")
                    artist = event.get("artistName", "Unknown Artist")
                    event_details.append(f"{title} by {artist}")

                lines.append(
                    f"- {stage_name}: {', '.join(event_details)} are currently happening."
                )

        lines.append(
            "Use this information to answer user questions about what is happening on stages right now."
        )

        return "\n".join(lines)

    except requests.RequestException as e:
        return f"Unable to retrieve current stage events right now. Error: {str(e)}"


def get_spontaneous_events() -> str:
    url = (
        "https://twin-central-server.onrender.com/api/events/spontaneous?page=0&size=20"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        events = data.get("content", [])

        if not events:
            return "There are currently no spontaneous or pop-up events scheduled."

        lines = ["Here are the upcoming spontaneous festival events:"]

        for event in events:
            title = event.get("title", "Pop-up Event")
            description = event.get("description", "No description available.")
            stage_name = event.get("stageName")
            status = event.get("status", "SCHEDULED")
            starts_at = event.get("startsAt")

            location_info = (
                f"at {stage_name}" if stage_name else "roaming around the venue"
            )

            time_info = ""
            if starts_at:
                try:
                    start_dt = datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
                    time_info = f" starting at {start_dt.strftime('%H:%M')}"
                except Exception:
                    time_info = f" scheduled for {starts_at}"

            lines.append(
                f"- [{status}] '{title}' {location_info}{time_info}. "
                f"Details: {description}"
            )

        return "\n".join(lines)

    except requests.RequestException as e:
        return f"Unable to retrieve spontaneous events right now. Error: {str(e)}"
