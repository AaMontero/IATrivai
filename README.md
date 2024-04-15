# Configuración del Entorno y Ejecución

## Creación del Entorno Virtual

1. Crear un entorno virtual para ejecutar las dependencias:

```bash
py -m venv entornoMV
cd entornoMV
cd Scripts 
activate 
sudo apt install python3-pip
pip install --upgrade pip
pip install google-auth
pip install google-cloud-speech
pip install google-cloud-texttospeech
pip install Flask
pip install pydub
py main.py
