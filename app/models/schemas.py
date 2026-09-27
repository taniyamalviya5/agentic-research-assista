from pydantic import BaseModel, Field


class Source(BaseModel):
    id: str
    source_type: str
    title: str
    url: str | None = None
    page: int | None = None
    score: float | None = None
    snippet: str = ""


class ResearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=4000)
    use_web: bool = True
    top_k: int = Field(default=5, ge=1, le=15)


class ResearchResponse(BaseModel):
    answer: str
    route: str
    reasoning_summary: str
    sources: list[Source]
    metrics: dict[str, float | int | str]


class DocumentInfo(BaseModel):
    filename: str
    chunks: int
    status: str


class EvaluationRequest(BaseModel):
    answer: str
    context: list[str]
    citations: list[str] = []
