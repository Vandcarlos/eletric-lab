from fastapi import FastAPI, File, HTTPException, UploadFile
from src.api.schemas import InspectionReport
from src.api.agent import router as agent_router
from src.service.inspection import inspect_image

app = FastAPI(title="Eletric Lab API", version="0.2.0")
app.include_router(agent_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/inspections", response_model=InspectionReport, status_code=201)
async def create_inspection(image: UploadFile = File(...)) -> InspectionReport:
    try:
        content = await image.read(10 * 1024 * 1024 + 1)
        return inspect_image(content, image.content_type)
    except ValueError as exc:
        code = 413 if "limite" in str(exc) else 415 if "formato" in str(exc) else 400
        raise HTTPException(status_code=code, detail=str(exc)) from exc
    finally:
        await image.close()
