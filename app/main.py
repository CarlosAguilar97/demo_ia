import uuid
import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.model import analizar_radiografia
from app.report_generator import generar_informe_radiologico
from app.db import ejecutar
from app.prompt_medico import construir_prompt

app = FastAPI(title="Asistente Radiológico IA")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analizar")
async def analizar(file: UploadFile = File(...)):
    estudio_id = str(uuid.uuid4())
    ruta = f"{UPLOAD_DIR}/{estudio_id}.jpg"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1️⃣ Modelo visión
    resultado_modelo = analizar_radiografia(ruta)

    # 2️⃣ LLM redacta informe
    informe = generar_informe_radiologico(resultado_modelo["hallazgos"])

    # 3️⃣ Guardar BD
    ejecutar(
        "INSERT INTO estudio (id, ruta_imagen) VALUES (?, ?)",
        [estudio_id, ruta]
    )

    ejecutar(
        """
        INSERT INTO prediccion (id, estudio_id, patron_detectado, confianza)
        VALUES (?, ?, ?, ?)
        """,
        [
            str(uuid.uuid4()),
            estudio_id,
            "informe_generado",
            resultado_modelo["confianza"]
        ]
    )

    return {
        "estudio_id": estudio_id,
        "confianza": resultado_modelo["confianza"],
        "informe": informe
    }


@app.post("/validar")
def validar(
    estudio_id: str = Form(...),
    estado: str = Form(...),
    diagnostico: str = Form(...),
    comentario: str = Form("")
):
    ejecutar(
        """
        INSERT INTO validacion (id, estudio_id, estado, diagnostico_medico, comentario)
        VALUES (?, ?, ?, ?, ?)
        """,
        [str(uuid.uuid4()), estudio_id, estado, diagnostico, comentario]
    )

    return {"mensaje": "Validación registrada"}
