from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Enterprise AI Knowledge & Risk Copilot",
    version="0.1.0",
)


class CaseRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)


class CaseResponse(BaseModel):
    case_id: str
    status: str


_CASES: dict[str, CaseResponse] = {}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/cases/analyze", response_model=CaseResponse, status_code=202)
async def analyze_case(request: CaseRequest) -> CaseResponse:
    case_id = str(uuid4())
    response = CaseResponse(case_id=case_id, status="received")
    _CASES[case_id] = response
    return response


@app.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str) -> CaseResponse:
    if case_id not in _CASES:
        raise HTTPException(status_code=404, detail="Case not found")
    return _CASES[case_id]
