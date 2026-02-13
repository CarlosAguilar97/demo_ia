import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generar_informe_radiologico(hallazgos: dict):
    """
    Convierte hallazgos estructurados en informe tipo radiólogo.
    """

    prompt = f"""
Actúa como un radiólogo torácico con experiencia.

Redacta un INFORME RADIOLÓGICO estructurado usando metodología A-B-C-D-E.
NO des diagnóstico definitivo.
Usa lenguaje médico descriptivo.

Hallazgos detectados por IA:

Airway: {hallazgos['airway']}
Pulmones: {hallazgos['pulmones']}
Pleura: {hallazgos['pleura']}
Cardíaco: {hallazgos['cardiaco']}
Otros: {hallazgos['otros']}

Incluye:
1. Evaluación sistemática
2. Descripción de hallazgos
3. Hallazgos ausentes relevantes
4. Impresión radiológica (no diagnóstica)
"""

    response = client.responses.create(
        model="gpt-5.2",   # ✔ modelo correcto para Responses API
        input=prompt,
        temperature=0.2
    )

    return response.output[0].content[0].text