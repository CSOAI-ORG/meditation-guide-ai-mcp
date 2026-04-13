import random
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("meditation-guide")

BREATHING_EXERCISES = {
    "box": {"inhale": 4, "hold": 4, "exhale": 4, "hold_empty": 4, "description": "Box breathing: equal counts in, hold, out, hold."},
    "4-7-8": {"inhale": 4, "hold": 7, "exhale": 8, "hold_empty": 0, "description": "4-7-8 breathing to promote relaxation."},
    "coherent": {"inhale": 5, "hold": 0, "exhale": 5, "hold_empty": 0, "description": "Coherent breathing at 5 seconds in, 5 seconds out."},
}

MEDITATION_SCRIPTS = {
    "calm": "Sit comfortably. Close your eyes. Breathe slowly. With each exhale, let tension melt away. Rest in this calm for a few minutes.",
    "focus": "Find a steady point to focus on. When thoughts arise, gently return your attention to the breath. Each return is a moment of mindfulness.",
    "gratitude": "Bring to mind three things you are grateful for. Feel the warmth of appreciation in your body. Let it expand with each breath.",
}

REMINDERS = [
    "Pause and take three deep breaths.",
    "Notice five things you can see right now.",
    "Place a hand on your heart and breathe slowly.",
    "Let go of one worry with your next exhale.",
]

@mcp.tool()
def get_breathing_exercise(name: str = "box") -> dict:
    """Get a breathing exercise."""
    exercise = BREATHING_EXERCISES.get(name)
    if not exercise:
        return {"error": "Exercise not found", "available": list(BREATHING_EXERCISES.keys())}
    return {"exercise": name, "details": exercise}

@mcp.tool()
def get_meditation_script(theme: str = "calm") -> dict:
    """Get a meditation script."""
    script = MEDITATION_SCRIPTS.get(theme)
    if not script:
        return {"error": "Theme not found", "available": list(MEDITATION_SCRIPTS.keys())}
    return {"theme": theme, "script": script}

@mcp.tool()
def suggest_mindfulness_reminder() -> dict:
    """Get a random mindfulness reminder."""
    return {"reminder": random.choice(REMINDERS)}

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
