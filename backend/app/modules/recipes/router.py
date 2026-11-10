# app/modules/recipes/router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.modules.extraction.extractor import scrape_recipe_content
from app.modules.extraction.service import parse_recipe_with_llm
# from app.modules.scheduler.engine_rs import solve_schedule  # (When Rust is ready)

router = APIRouter(prefix="/recipes", tags=["recipes"])

class IngestRecipeRequest(BaseModel):
    url: HttpUrl

@router.post("/process")
async def process_recipe_url(payload: IngestRecipeRequest):
    try:
        # Step A: Scrape URL
        raw_recipe = scrape_recipe(str(payload.url))
        
        # Step B: LLM extracts graph + durations + dependencies
        recipe_graph = parse_recipe_with_llm(raw_recipe)
        
        # Step C: (Optional) Pass to Rust engine for schedule ordering
        # scheduled_steps = solve_schedule(recipe_graph.tasks)
        
        return {
            "title": recipe_graph.recipe_title,
            "tasks": recipe_graph.tasks,
            "review_insights": recipe_graph.review_insights
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process recipe: {str(e)}")

# @router.post("/optimize/pdf", response_model=list[ScheduledTask])
# async def schedule_from_pdf(
#     file: UploadFile = File(...),
#     num_people: int = Form(1),
#     num_burners: int = Form(4),
#     num_ovens: int = Form(1)
# ):
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
#     file_bytes = await file.read()
#     return await service.process_pdf(
#         pdf_bytes=file_bytes,
#         people=num_people,
#         burners=num_burners,
#         ovens=num_ovens
#     )