TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_artist_info",
            "description": "Get information about a festival artist",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the artist",
                    }
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_live_events",
            "description": "Get events happening right now at the festival",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]
