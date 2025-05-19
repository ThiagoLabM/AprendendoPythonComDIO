import json
import os

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"

def salvar_dados():
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=4, default=str)
    with open(ARQUIVO_CONTAS, 'w', encoding='utf-8') as f:
        json.dump(contas, f, ensure_ascii=False, indent=4, default=str)

def carregar_dados():
    global cad, contas
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            cad = json.load(f)
    if os.path.exists(ARQUIVO_CONTAS):
        with open(ARQUIVO_CONTAS, 'r', encoding='utf-8') as f:
            contas = json.load(f)
