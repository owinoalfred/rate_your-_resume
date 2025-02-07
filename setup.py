import subprocess
import importlib.util

def is_spacy_model_installed(model_name):
    model_spec = importlib.util.find_spec(model_name)
    return model_spec is not None

def download_spacy_model(model_name):
    subprocess.run(["python", "-m", "spacy", "download", model_name])

if __name__ == "__main__":
    model_name = "en_core_web_sm"
    if not is_spacy_model_installed(model_name):
        download_spacy_model(model_name)