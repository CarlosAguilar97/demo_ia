import sys
import os

# Permitir importar la carpeta app
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app