import uuid
import os
import shutil

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from model import analizar_radiografia
from report_generator import generar_informe_radiologico
from db import ejecutar

app = FastAPI(title="Asistente Radiológico IA")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
