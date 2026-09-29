import re

def build_comic_layout(outline, story_text, image_paths):
    panels = []
    # Parse story_text into dict
    panel_stories = {}
    # split by PANEL X:
    matches = re.split(r'PANEL\s+(\d+):', story_text, flags=re.IGNORECASE)
    # matches[0] is before first, then [num, text, num, text]
    for i in range(1, len(matches), 2):
        try:
            num = int(matches[i])
            content = matches[i+1].strip()
            # extract Caption and Narration
            caption_match = re.search(r'Caption:\s*(.*?)(?:Narration:|$)', content, re.S | re.I)
            narration_match = re.search(r'Narration:\s*(.*)', content, re.S | re.I)
            caption = caption_match.group(1).strip() if caption_match else ""
            narration = narration_match.group(1).strip() if narration_match else content[:200]
            panel_stories[num] = {"caption": caption, "narration": narration, "full_text": content}
        except:
            continue

    for idx, out in enumerate(outline):
        p_num = out.get("panel", idx+1)
        story_data = panel_stories.get(p_num, {"caption": out.get("scene_description",""), "narration": "Adventure continues...", "full_text": out.get("scene_description","")})
        panels.append({
            "panel_number": p_num,
            "title": out.get("title", f"Panel {p_num}"),
            "scene_description": out.get("scene_description", ""),
            "image_prompt": out.get("image_prompt", ""),
            "image_path": image_paths[idx] if idx < len(image_paths) else "",
            "caption": story_data["caption"],
            "narration": story_data["narration"],
        })
    return panels
