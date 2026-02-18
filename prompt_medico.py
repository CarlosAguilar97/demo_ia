def construir_prompt(hallazgos: dict, datos_clinicos: dict | None = None) -> str:
    """
    Construye un prompt médico que integra:
    - Hallazgos radiológicos
    - Síntomas del paciente (si existen)
    - Correlación clínico-radiológica
    """

    sintomas = datos_clinicos.get("sintomas", "No referidos") if datos_clinicos else "No referidos"
    edad = datos_clinicos.get("edad", "No especificada") if datos_clinicos else "No especificada"
    antecedentes = datos_clinicos.get("antecedentes", "No referidos") if datos_clinicos else "No referidos"
    tiempo = datos_clinicos.get("tiempo_evolucion", "No especificado") if datos_clinicos else "No especificado"

    return f"""
Actúa como un MÉDICO RADIÓLOGO TORÁCICO con experiencia hospitalaria.

Debes redactar un INFORME RADIOLÓGICO REAL, integrando hallazgos de imagen
con la información clínica disponible.

⚠️ NO EMITAS DIAGNÓSTICO DEFINITIVO.
⚠️ SOLO ORIENTACIÓN CLÍNICO-RADIOLÓGICA.
⚠️ Usa lenguaje médico prudente como en práctica real.

===============================
DATOS CLÍNICOS
===============================
Edad: {edad}
Síntomas principales: {sintomas}
Tiempo de evolución: {tiempo}
Antecedentes relevantes: {antecedentes}

===============================
HALLAZGOS RADIOLÓGICOS IA
===============================
Airway: {hallazgos["airway"]}
Pulmones: {hallazgos["pulmones"]}
Pleura: {hallazgos["pleura"]}
Cardíaco: {hallazgos["cardiaco"]}
Otros: {hallazgos["otros"]}

===============================
REDACCIÓN SOLICITADA
===============================

EL ESTUDIO RADIOLÓGICO DEL TÓRAX, MUESTRA:

1. Descripción técnica sistemática A-B-C-D-E.
2. Detalle morfológico de hallazgos.
3. Hallazgos ausentes relevantes.
4. Correlación con síntomas proporcionados.
5. Posibles procesos fisiopatológicos que PODRÍAN explicar la imagen
   (infeccioso, inflamatorio, restrictivo, obstructivo, secuelar, etc.).

IMPRESIÓN RADIOLÓGICA:
• Máximo 3 conclusiones.
• Expresar probabilidad, NO certeza.
• Recomendar correlación clínica o estudios adicionales si aplica.
"""