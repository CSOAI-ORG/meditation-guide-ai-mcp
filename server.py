#!/usr/bin/env python3
"""Meditation Guide AI — guided meditations, breathing exercises, and mindfulness practices. MEOK AI Labs."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

# Meditation templates
_MEDITATIONS = {
    "calm": {
        "title": "Calm Mind Meditation",
        "steps": [
            "Find a comfortable seated position and close your eyes.",
            "Take three deep breaths, inhaling through the nose, exhaling through the mouth.",
            "Let your breathing return to its natural rhythm.",
            "Notice any thoughts that arise — acknowledge them and let them pass like clouds.",
            "Bring your attention gently back to the sensation of breathing.",
            "Feel the stillness growing in the space between your thoughts.",
            "When you are ready, slowly open your eyes.",
        ],
    },
    "focus": {
        "title": "Focus & Clarity Meditation",
        "steps": [
            "Sit upright with a straight spine. Close your eyes.",
            "Breathe in for 4 counts, hold for 4, exhale for 4.",
            "Visualize a single point of light in the centre of your mind.",
            "With each breath, let the light grow brighter and steadier.",
            "If distractions arise, gently guide your attention back to the light.",
            "Feel mental clarity building with every exhale.",
            "Open your eyes slowly, carrying this focus with you.",
        ],
    },
    "sleep": {
        "title": "Sleep Preparation Meditation",
        "steps": [
            "Lie down comfortably. Let your body sink into the surface beneath you.",
            "Close your eyes and take five slow, deep breaths.",
            "Starting from your toes, consciously relax each body part upward.",
            "Release tension in your feet, calves, thighs, hips, stomach, chest.",
            "Relax your shoulders, arms, hands, neck, jaw, and forehead.",
            "Imagine a warm, gentle wave of relaxation washing over you.",
            "Let your thoughts dissolve. There is nothing to do but rest.",
        ],
    },
    "stress": {
        "title": "Stress Relief Meditation",
        "steps": [
            "Sit or lie in a comfortable position. Close your eyes.",
            "Take a deep breath in and sigh it out audibly.",
            "Place one hand on your chest and one on your belly.",
            "Breathe deeply into your belly — feel it rise and fall.",
            "With each exhale, imagine releasing one worry or tension.",
            "Repeat a calming phrase: 'I am safe. I am calm. I am enough.'",
            "Continue for several minutes, then open your eyes gently.",
        ],
    },
}

# Breathing exercise library
_BREATHING = {
    "box": {"name": "Box Breathing", "inhale": 4, "hold_in": 4, "exhale": 4, "hold_out": 4, "rounds": 5, "purpose": "calm and focus"},
    "478": {"name": "4-7-8 Breathing", "inhale": 4, "hold_in": 7, "exhale": 8, "hold_out": 0, "rounds": 4, "purpose": "relaxation and sleep"},
    "energize": {"name": "Energizing Breath", "inhale": 2, "hold_in": 0, "exhale": 2, "hold_out": 0, "rounds": 20, "purpose": "energy and alertness"},
    "calm": {"name": "Extended Exhale", "inhale": 4, "hold_in": 0, "exhale": 8, "hold_out": 0, "rounds": 6, "purpose": "anxiety relief"},
}

# Session tracking
_sessions: list[dict] = []

mcp = FastMCP("meditation-guide-ai", instructions="Generate guided meditations, breathing exercises, and mindfulness practices. By MEOK AI Labs.")


@mcp.tool()
def get_meditation(style: str = "calm", duration_minutes: int = 10, api_key: str = "") -> str:
    """Get a guided meditation script. Styles: calm, focus, sleep, stress. Duration adjusts detail level."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    style = style.lower()
    if style not in _MEDITATIONS:
        return json.dumps({"error": f"Unknown style '{style}'. Choose from: {', '.join(_MEDITATIONS.keys())}"})
    med = _MEDITATIONS[style]
    duration_minutes = max(3, min(duration_minutes, 60))
    seconds_per_step = (duration_minutes * 60) // len(med["steps"])
    return json.dumps({
        "title": med["title"],
        "style": style,
        "duration_minutes": duration_minutes,
        "seconds_per_step": seconds_per_step,
        "steps": med["steps"],
        "tip": "Find a quiet space. Silence notifications. Be gentle with yourself.",
    }, indent=2)


@mcp.tool()
def track_session(style: str, duration_minutes: int, mood_before: int = 5, mood_after: int = 7, api_key: str = "") -> str:
    """Log a completed meditation session. Mood scores 1-10 (1=worst, 10=best)."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    mood_before = max(1, min(mood_before, 10))
    mood_after = max(1, min(mood_after, 10))
    session = {
        "id": len(_sessions) + 1,
        "style": style.lower(),
        "duration_minutes": max(1, duration_minutes),
        "mood_before": mood_before,
        "mood_after": mood_after,
        "mood_change": mood_after - mood_before,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _sessions.append(session)
    total_minutes = sum(s["duration_minutes"] for s in _sessions)
    avg_improvement = sum(s["mood_change"] for s in _sessions) / len(_sessions)
    return json.dumps({
        "logged": session,
        "streak": {
            "total_sessions": len(_sessions),
            "total_minutes": total_minutes,
            "avg_mood_improvement": round(avg_improvement, 1),
        },
    }, indent=2)


@mcp.tool()
def get_breathing_exercise(technique: str = "box", api_key: str = "") -> str:
    """Get a structured breathing exercise. Techniques: box, 478, energize, calm."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    technique = technique.lower()
    if technique not in _BREATHING:
        return json.dumps({"error": f"Unknown technique '{technique}'. Choose from: {', '.join(_BREATHING.keys())}"})
    ex = _BREATHING[technique]
    total_seconds = (ex["inhale"] + ex["hold_in"] + ex["exhale"] + ex["hold_out"]) * ex["rounds"]
    instructions = []
    for r in range(1, ex["rounds"] + 1):
        steps = [f"Round {r}: Inhale for {ex['inhale']}s"]
        if ex["hold_in"]: steps.append(f"Hold for {ex['hold_in']}s")
        steps.append(f"Exhale for {ex['exhale']}s")
        if ex["hold_out"]: steps.append(f"Hold for {ex['hold_out']}s")
        instructions.append(" → ".join(steps))
    return json.dumps({
        "name": ex["name"],
        "purpose": ex["purpose"],
        "total_duration_seconds": total_seconds,
        "rounds": ex["rounds"],
        "pattern": {"inhale": ex["inhale"], "hold_in": ex["hold_in"], "exhale": ex["exhale"], "hold_out": ex["hold_out"]},
        "instructions": instructions,
    }, indent=2)


@mcp.tool()
def suggest_practice(goal: str = "general", available_minutes: int = 10, api_key: str = "") -> str:
    """Suggest a meditation or breathing practice based on your goal and available time. Goals: general, sleep, focus, stress, energy."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    goal = goal.lower()
    suggestions = {
        "sleep": {"meditation": "sleep", "breathing": "478", "advice": "Do the breathing exercise first, then the meditation while lying down."},
        "focus": {"meditation": "focus", "breathing": "box", "advice": "Start with box breathing to settle, then move into the focus meditation."},
        "stress": {"meditation": "stress", "breathing": "calm", "advice": "Begin with extended exhale breathing, then transition to the stress relief meditation."},
        "energy": {"meditation": "focus", "breathing": "energize", "advice": "Do energizing breaths first to wake up, then a short focus meditation."},
        "general": {"meditation": "calm", "breathing": "box", "advice": "Box breathing followed by a calm meditation is a great all-purpose practice."},
    }
    if goal not in suggestions:
        return json.dumps({"error": f"Unknown goal '{goal}'. Choose from: {', '.join(suggestions.keys())}"})
    s = suggestions[goal]
    available_minutes = max(3, min(available_minutes, 60))
    breathing_minutes = min(3, available_minutes // 3)
    meditation_minutes = available_minutes - breathing_minutes
    # Check session history for personalized tips
    history_tip = None
    if _sessions:
        best_style = max(set(s["style"] for s in _sessions), key=lambda st: sum(1 for s in _sessions if s["style"] == st))
        avg_duration = sum(s["duration_minutes"] for s in _sessions) / len(_sessions)
        history_tip = f"You've done {len(_sessions)} sessions. Your most-used style is '{best_style}' (avg {round(avg_duration)}min)."
    return json.dumps({
        "goal": goal,
        "available_minutes": available_minutes,
        "plan": {
            "step_1": {"type": "breathing", "technique": s["breathing"], "duration_minutes": breathing_minutes},
            "step_2": {"type": "meditation", "style": s["meditation"], "duration_minutes": meditation_minutes},
        },
        "advice": s["advice"],
        "history_insight": history_tip,
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
