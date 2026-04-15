# Meditation Guide AI

> By [MEOK AI Labs](https://meok.ai) — Guided meditations, breathing exercises, and mindfulness practices

## Installation

```bash
pip install meditation-guide-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `get_meditation`
Get a guided meditation script. Styles: calm, focus, sleep, stress. Duration adjusts detail level.

**Parameters:**
- `style` (str): Meditation style (default: "calm")
- `duration_minutes` (int): Duration 3-60 minutes (default: 10)

### `track_session`
Log a completed meditation session. Mood scores 1-10 (1=worst, 10=best).

**Parameters:**
- `style` (str): Meditation style used
- `duration_minutes` (int): Actual duration
- `mood_before` (int): Mood before session 1-10 (default: 5)
- `mood_after` (int): Mood after session 1-10 (default: 7)

### `get_breathing_exercise`
Get a structured breathing exercise. Techniques: box, 478, energize, calm.

**Parameters:**
- `technique` (str): Breathing technique (default: "box")

### `suggest_practice`
Suggest a meditation or breathing practice based on your goal and available time.

**Parameters:**
- `goal` (str): Goal: general, sleep, focus, stress, energy (default: "general")
- `available_minutes` (int): Time available (default: 10)

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
