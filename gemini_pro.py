import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

STORY_PROMPT = """
Expand this comic outline into narration:
Outline: {outline}

Character: {character_name}, Setting: {setting}, Tone: {tone}

For each panel, write:
Caption: (ambient description)
Narration: (what character does/says, engaging dialogue)

Return panel by panel in format:
PANEL 1:
Caption:...
Narration:...

... up to PANEL 5. Keep story cohesive and {tone}.
"""

def generate_story(outline, character_name, setting, tone):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        prompt = STORY_PROMPT.format(outline=str(outline), character_name=character_name, setting=setting, tone=tone)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Pro Error: {e}")
        # Fallback story
        story = ""
        for p in outline:
            story += f"PANEL {p['panel']}:\nCaption: {p['scene_description']}\nNarration: {character_name} says 'What an adventure in {setting}!'.\n\n"
        return story
