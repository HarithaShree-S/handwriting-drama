"""
Handwriting Forensics Lab - Scoring and Malayalam Dialogue Engine
Translates OpenCV metrics into hilarious Malayalam movie dialogues and dramatic lab conclusions.
"""

import random
from typing import Dict, Any


def generate_dramatic_report(metrics: Dict[str, int]) -> Dict[str, Any]:
    """
    Translates raw OpenCV metrics into hilarious Malayalam movie dialogues and dramatic lab conclusions.
    
    Expected keys in metrics:
      - pen_aggression: int
      - letter_ego: int
      - personal_space: int
      - chaos_level: int
    """
    pen = metrics.get("pen_aggression", 50)
    ego = metrics.get("letter_ego", 50)
    space = metrics.get("personal_space", 50)
    chaos = metrics.get("chaos_level", 50)

    # Calculate Main Character Energy (weighted combination)
    main_character_energy = int((ego * 0.4) + (pen * 0.3) + (chaos * 0.3))
    main_character_energy = max(1, min(99, main_character_energy))

    # --- 1. PEN AGGRESSION DIALOGUES (Pressure / Ink Density) ---
    if pen > 70:
        pen_dialogue = "🔥 'Po Mone Dinesha!' — You press the pen so hard the notebook needs medical insurance."
    elif pen > 40:
        pen_dialogue = "😌 'Ellam Ok Aanu!' — Moderate pen pressure. Emotionally balanced ink flow."
    else:
        pen_dialogue = "👻 'Athukondau njan paranjathu...' — Whisper thin lines. Are you writing secrets or running out of ink?"

    # --- 2. LETTER EGO DIALOGUES (Contour Size) ---
    if ego > 70:
        ego_verdict = "👑 'Manavalan at your service!' — Huge letters! Total main character attitude on paper."
    elif ego > 40:
        ego_verdict = "👌 'Simple, humble, powerful.' — Normal sizing. Modest self-esteem."
    else:
        ego_verdict = "🔍 'Ithu aara paranjathu?' — Microscopic handwriting. Are you writing secret notes for ants?"

    # --- 3. WORD PERSONAL SPACE DIALOGUES (Spacing Gaps) ---
    if space > 60:
        space_verdict = "🌴 'Sadanam Kayyilundo?' — Words are sitting in two different districts. Emotionally healthy distancing!"
    elif space > 30:
        space_verdict = "🤝 'Njangal Onnaanu!' — Respectful distance between words. Cozy yet polite."
    else:
        space_verdict = "🚨 'Entammey, enthoru thirukku!' — Your words are suffocating each other like a KSRTC bus at 5 PM."

    # --- 4. CHAOS LEVEL DIALOGUES (Height Variation) ---
    if chaos > 60:
        chaos_verdict = "🌪️ 'Ormayundo Ee Mukham?' — Unstable heights! Your letters change identity every line."
    else:
        chaos_verdict = "📐 'Perfect geometry!' — Unnaturally neat. Are you human or a laser printer?"

    # --- 5. ABSURD MALAYALAM FORENSIC VERDICTS ---
    conclusions = [
        "🚨 LAB DIAGNOSIS: 'Ente Dashanane...!' Your pen strokes carry 100% comedy movie villain energy.",
        "🧪 FORENSIC VERDICT: 'Savari Giri Giri!' Extremely dramatic handwriting detected.",
        "⚠️ WARNING: 'Pavanayi Shavamayi!' Step away from the pen before you tear another notebook page.",
        "🎭 CERTIFICATE OF DRAMA: 'Njan Oru Paavam Human Being!' Your handwriting screams chaos.",
    ]

    # Check whether the sample qualifies for dramatic vs comedy sound effects
    is_high_drama = (main_character_energy >= 65 or pen > 70 or chaos > 60)

    return {
        "main_character_energy": main_character_energy,
        "pen_dialogue": pen_dialogue,
        "ego_verdict": ego_verdict,
        "space_verdict": space_verdict,
        "chaos_verdict": chaos_verdict,
        "final_conclusion": random.choice(conclusions),
        "is_high_drama": is_high_drama,
    }