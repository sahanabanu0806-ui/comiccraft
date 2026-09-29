from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from models.schemas import PromptRequest
from models.gemini_flash import generate_outline
from models.gemini_pro import generate_story
from models.image_generator import generate_image
from models.layout_builder import build_comic_layout
from models.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    try:
        outline = generate_outline(story_prompt, character_name, setting, tone, art_style)
        story_text = generate_story(outline, character_name, setting, tone)

        image_paths = []
        for panel in outline:
            img_path = generate_image(panel['image_prompt'], panel['panel'], art_style)
            image_paths.append(img_path)

        layout = build_comic_layout(outline, story_text, image_paths)
        pdf_url, pdf_real_path = save_pdf(layout, character_name)

        return templates.TemplateResponse(request, "comic_preview.html", {
            "request": request,
            "layout": layout,
            "pdf_url": pdf_url,
            "character_name": character_name
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-comic/json")
async def generate_comic_json(data: PromptRequest):
    try:
        outline = generate_outline(data.story_prompt, data.character_name, data.setting, data.tone, data.art_style)
        story_text = generate_story(outline, data.character_name, data.setting, data.tone)
        image_paths = [generate_image(p['image_prompt'], p['panel'], data.art_style) for p in outline]
        layout = build_comic_layout(outline, story_text, image_paths)
        pdf_url, _ = save_pdf(layout, data.character_name)
        return {"layout": layout, "pdf_url": pdf_url, "story_text": story_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(request, "export_success.html", {"request": request})

@router.get("/test-image")
async def test_image(prompt: str = "a brave fox in enchanted forest, anime style"):
    path = generate_image(prompt, 1, "anime")
    return {"image_path": path}
