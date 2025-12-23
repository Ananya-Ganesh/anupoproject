from __future__ import annotations

import os
import tempfile
from typing import Dict, Any

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from po_frontend_adapter import compare_for_frontend


app = FastAPI(title="PO Comparison AI Tool")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Helpers --------------------
def _save_upload_to_temp(upload: UploadFile) -> str:
    suffix = os.path.splitext(upload.filename or "")[1] or ".pdf"
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as tmp:
        tmp.write(upload.file.read())
    return path


# -------------------- API --------------------
@app.post("/compare-pos")
async def compare_pos(
    po_a: UploadFile = File(...),
    po_b: UploadFile = File(...),
) -> Dict[str, Any]:
    """
    Accepts two PO files and returns comparison result
    """
    path_a = _save_upload_to_temp(po_a)
    path_b = _save_upload_to_temp(po_b)

    try:
        return compare_for_frontend(path_a, path_b)
    finally:
        for p in (path_a, path_b):
            try:
                os.remove(p)
            except OSError:
                pass


# -------------------- SERVE REACT FRONTEND --------------------
# React build MUST be in ./dist next to app.py

if os.path.isdir("dist"):
    # serve Vite assets
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

    @app.get("/")
    async def serve_react():
        return FileResponse("dist/index.html")
else:
    # fallback if dist not present
    @app.get("/")
    async def root():
        return {
            "message": "React build not found. Run npm run build and commit dist/"
        }
