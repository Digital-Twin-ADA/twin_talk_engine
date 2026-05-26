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
