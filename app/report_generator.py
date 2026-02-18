import os
from openai import OpenAI
from prompt_medico import construir_prompt


client = OpenAI(api_key=os.environ("OPENAI_API_KEY"))

def generar_informe_radiologico(hallazgos: dict) -> str:
    """
    Convierte hallazgos estructurados en informe radiológico profesional.
    """

    try:
        prompt = construir_prompt(hallazgos)

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # modelo estable y económico
            messages=[
                {"role": "system", "content": "Eres un médico radiólogo experto en tórax."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ Error OpenAI:", e)

        # fallback para que la demo nunca muera
        return f"""
EL ESTUDIO RADIOLÓGICO DEL TÓRAX, MUESTRA:

{hallazgos}

IMPRESIÓN DIAGNÓSTICA:
Hallazgos descritos por sistema automatizado.
Se recomienda correlación clínica.
"""

    return response.output[0].content[0].text