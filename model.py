import random

def analizar_radiografia(ruta_imagen: str):
    """
    Simulación de salida estructurada de un modelo de visión.
    Luego esto será reemplazado por MONAI/PyTorch real.
    """

    hallazgos = {
        "airway": "tráquea centrada",
        "pulmones": random.choice([
            "patrón intersticial basal leve",
            "sin consolidaciones focales",
            "aumento de marcas pulmonares"
        ]),
        "pleura": random.choice([
            "engrosamiento pleural basal",
            "senos costofrénicos discretamente borrados",
            "sin derrame evidente"
        ]),
        "cardiaco": "silueta cardíaca conservada",
        "otros": "sin lesiones óseas agudas visibles"
    }

    confianza_global = round(random.uniform(0.80, 0.93), 2)

    return {
        "hallazgos": hallazgos,
        "confianza": confianza_global
    }