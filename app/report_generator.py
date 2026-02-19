import os
from openai import OpenAI
from app.prompt_medico import construir_prompt
#from dotenv import load_dotenv

#load_dotenv()

def generar_informe_radiologico(hallazgos: dict) -> str:
    """
    Convierte hallazgos estructurados en informe radiológico profesional.
    """

    try:
        # ✅ Crear cliente dentro de la ejecución (serverless-safe)
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        prompt = construir_prompt(hallazgos)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un médico radiólogo experto en tórax."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ Error OpenAI:", e)

        # fallback para demo (clave en serverless)
        return f"""
EL ESTUDIO RADIOLÓGICO DEL TÓRAX, MUESTRA:

{hallazgos}

IMPRESIÓN DIAGNÓSTICA:
Hallazgos descritos por sistema automatizado.
Se recomienda correlación clínica.
"""