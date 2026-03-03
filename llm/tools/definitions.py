# llm/tools/definitions.py


# ─────────────────────────────────────────────
# NEW: llm/tools/definitions.py
# OpenAI-format tool schemas that Qwen sees.
# One function per action — simpler for a 3b model.
# ─────────────────────────────────────────────
def get_tool_definitions() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "send_imessage",
                "description": "Send an iMessage to a phone number or contact name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "phoneNumber": {
                            "type": "string",
                            "description": "Phone number or contact name",
                        },
                        "message": {"type": "string", "description": "Text to send"},
                    },
                    "required": ["phoneNumber", "message"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_imessage",
                "description": "Read recent messages from a contact.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "phoneNumber": {
                            "type": "string",
                            "description": "Phone number or contact name",
                        },
                        "limit": {
                            "type": "number",
                            "description": "How many messages to fetch (default 5)",
                        },
                    },
                    "required": ["phoneNumber"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "unread_imessages",
                "description": "Check all unread iMessages.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "number",
                            "description": "Max unread messages to return (default 10)",
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web for current information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_reminder",
                "description": "Create a reminder in Apple Reminders.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Reminder title"},
                        "dueDate": {
                            "type": "string",
                            "description": "Due date in ISO format (optional)",
                        },
                        "notes": {
                            "type": "string",
                            "description": "Extra notes (optional)",
                        },
                        "listName": {
                            "type": "string",
                            "description": "List to add to (optional)",
                        },
                    },
                    "required": ["name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_reminders",
                "description": "List all current reminders.",
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_calendar_event",
                "description": "Create an event in Apple Calendar.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Event title"},
                        "startDate": {
                            "type": "string",
                            "description": "Start datetime in ISO format",
                        },
                        "endDate": {
                            "type": "string",
                            "description": "End datetime in ISO format",
                        },
                        "location": {
                            "type": "string",
                            "description": "Location (optional)",
                        },
                        "notes": {"type": "string", "description": "Notes (optional)"},
                        "isAllDay": {
                            "type": "boolean",
                            "description": "All-day event (optional)",
                        },
                    },
                    "required": ["title", "startDate", "endDate"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_calendar_events",
                "description": "List upcoming calendar events.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fromDate": {
                            "type": "string",
                            "description": "Start date ISO (optional, default today)",
                        },
                        "toDate": {
                            "type": "string",
                            "description": "End date ISO (optional, default 7 days)",
                        },
                        "limit": {
                            "type": "number",
                            "description": "Max events (optional, default 10)",
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_contacts",
                "description": "Search Apple Contacts by name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name to search (partial match ok)",
                        },
                    },
                },
            },
        },
    ]
