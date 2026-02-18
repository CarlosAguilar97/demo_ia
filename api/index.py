import uuid
import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.model import analizar_radiografia
from app.report_generator import generar_informe_radiologico
from app.db import ejecutar
from app.prompt_medico import construir_prompt

app = FastAPI()

# Vercel solo permite escritura en /tmp
UPLOAD_DIR = "/tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analizar")
async def analizar(
    file: UploadFile = File(...),
    edad: str = Form(""),
    sintomas: str = Form(""),
    tiempo: str = Form(""),
    antecedentes: str = Form("")
):
    estudio_id = str(uuid.uuid4())
    ruta = f"{UPLOAD_DIR}/{estudio_id}.jpg"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resultado_modelo = analizar_radiografia(ruta)

    datos_clinicos = {
        "edad": edad,
        "sintomas": sintomas,
        "tiempo_evolucion": tiempo,
        "antecedentes": antecedentes
    }

    informe = generar_informe_radiologico(
        resultado_modelo["hallazgos"],
        datos_clinicos
    )

    ejecutar(
        "INSERT INTO estudio (id, ruta_imagen) VALUES (?, ?)",
        [estudio_id, ruta]
    )

    return {
        "estudio_id": estudio_id,
        "confianza": resultado_modelo["confianza"],
        "informe": informe
    }