from .now import now

available = [
  {
    "func": now,
    "desc": {
      "name": "now",
      "description": "Get the current date and time.",
      "parameters": {
        "type": "object",
        "properties": {
          "tz": {
            "type": "string",
            "description": "Timezone, e.g. Asia/Seoul"
          }
        },
        "required": ["tz"],
      }
    }
  },
]