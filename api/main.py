from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from api.schema import VerificationRequest, VerificationResponse
from gravit_verifier.engine import EpistemicEngine

app = FastAPI(title="Gravit Epistemic Verifier", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
Instrumentator().instrument(app).expose(app)
engine = EpistemicEngine()


@app.post("/verify", response_model=VerificationResponse)
async def verify_action(request: VerificationRequest):
    result = engine.verify(
        intent=request.intent,
        action=request.action,
        model_id=request.model_id,
        prompt=request.prompt,
        intermediate_steps=request.intermediate_steps,
    )
    return VerificationResponse(**result, verifier_version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}
