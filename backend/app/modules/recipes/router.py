from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, HttpUrl
from app.schemas.recipe import ScheduledTask
from app.modules.recipes.service import RecipePipelineService

router = APIRouter()
service = RecipePipelineService()

class ScheduleURLRequest(BaseModel):
    url: HttpUrl
    num_people: int = 1
    num_burners: int = 4
    num_ovens: int = 1

@router.post("/optimize/url", response_model=list[ScheduledTask])
async def schedule_from_url(payload: ScheduleURLRequest):
    try:
        return await service.process_url(
            url=str(payload.url),
            people=payload.num_people,
            burners=payload.num_burners,
            ovens=payload.num_ovens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize/pdf", response_model=list[ScheduledTask])
async def schedule_from_pdf(
    file: UploadFile = File(...),
    num_people: int = Form(1),
    num_burners: int = Form(4),
    num_ovens: int = Form(1)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_bytes = await file.read()
    return await service.process_pdf(
        pdf_bytes=file_bytes,
        people=num_people,
        burners=num_burners,
        ovens=num_ovens
    )