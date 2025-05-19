import json
import os
from datetime import datetime
import pytz
from tzlocal import get_localzone

# Arquivos para salvar os dados
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"

# Dicionários
usuarios = {}  # Cadastro de usuários (CPF como chave)
contas = {}    # Contas bancárias (CPF como chave)

# Limites
LIMITE_SAQUE = 500
LIMITE_TRANSACOES_DIARIAS = 3

# Usuário logado
usuario_logado = None

# Menu
menu = """
================ MENU =================
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
=======================================
"""

# Funções utilitárias
def data_hora():
    agora = datetime.now(pytz.timezone('America/Sao_Paulo'))
    data = agora.strftime("%d-%m-%Y")
    hora = agora.strftime("%H:%M:%S")
    timezone = str(get_localzone())
    return data, hora, timezone

# Salvamento e carregamento
def salvar_dados():
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    with open(ARQUIVO_CONTAS, 'w', encoding='utf-8') as f:
        json.dump(contas, f, indent=4, ensure_ascii=False)

def carregar_dados():
    global usuarios, contas
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    if os.path.exists(ARQUIVO_CONTAS):
        with open(ARQUIVO_CONTAS, 'r', encoding='utf-8') as f:
            contas = json.load(f)

# Cadastro
def cadastrar_usuario():
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")
    cpf = input("CPF (somente números): ")

    if cpf in usuarios:
        print("CPF já cadastrado.\n")
        return

    senha = input("Crie uma senha: ")

    usuarios[cpf] = {
        "nome": nome,
        "telefone": telefone,
        "endereco": endereco,
        "cpf": cpf,
        "senha": senha
    }

    contas[cpf] = {
        "saldo": 0.0,
        "transacoes": {},
        "limite_transacoes": LIMITE_TRANSACOES_DIARIAS
    }

    salvar_dados()
    print(f"Usuário {nome} cadastrado com sucesso!\n")

# Login
def login():
    global usuario_logado
    cpf = input("CPF: ")
    senha = input("Senha: ")

    if cpf in usuarios and usuarios[cpf]["senha"] == senha:
        usuario_logado = cpf
        print(f"\nBem-vindo(a), {usuarios[cpf]['nome']}!\n")
        return True
    else:
        print("CPF ou senha inválidos.\n")
        return False

# Número de transações no dia
def numero_transacoes_do_dia(cpf, data):
    return len(contas[cpf]["transacoes"].get(data, {}))

# Depósito
def depositar():
    valor = float(input("Valor para depósito: "))
    if valor <= 0:
        print("Valor inválido.\n")
        return

    data, hora, timezone = data_hora()
    if numero_transacoes_do_dia(usuario_logado, data) >= LIMITE_TRANSACOES_DIARIAS:
        print("Limite de transações diárias atingido.\n")
        return

    contas[usuario_logado]["saldo"] += valor
    if data not in contas[usuario_logado]["transacoes"]:
        contas[usuario_logado]["transacoes"][data] = {}

    id_transacao = len(contas[usuario_logado]["transacoes"][data]) + 1
    contas[usuario_logado]["transacoes"][data][str(id_transacao)] = {
        "tipo": "depósito",
        "valor": valor,
        "hora": hora,
        "timezone": timezone
    }

    salvar_dados()
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso.\n")

# Saque
def sacar():
    valor = float(input("Valor para saque: "))
    saldo = contas[usuario_logado]["saldo"]

    if valor <= 0:
        print("Valor inválido.\n")
        return
    if valor > saldo:
        print("Saldo insuficiente.\n")
        return
    if valor > LIMITE_SAQUE:
        print(f"Limite de saque por transação é R$ {LIMITE_SAQUE:.2f}.\n")
        return

    data, hora, timezone = data_hora()
    if numero_transacoes_do_dia(usuario_logado, data) >= LIMITE_TRANSACOES_DIARIAS:
        print("Limite de transações diárias atingido.\n")
        return

    contas[usuario_logado]["saldo"] -= valor
    if data not in contas[usuario_logado]["transacoes"]:
        contas[usuario_logado]["transacoes"][data] = {}

    id_transacao = len(contas[usuario_logado]["transacoes"][data]) + 1
    contas[usuario_logado]["transacoes"][data][str(id_transacao)] = {
        "tipo": "saque",
        "valor": valor,
        "hora": hora,
        "timezone": timezone
    }

    salvar_dados()
    print(f"Saque de R$ {valor:.2f} realizado com sucesso.\n")

# Extrato
def extrato():
    data = input("Digite a data (dd-mm-aaaa): ")
    transacoes = contas[usuario_logado]["transacoes"].get(data)

    print("\n============== EXTRATO ==============")
    print(f"Data: {data}")
    if not transacoes:
        print("Nenhuma transação nesta data.\n")
    else:
        for id, t in transacoes.items():
            print(f"{id} - {t['tipo'].capitalize()} - R$ {t['valor']:.2f} - {t['hora']} - {t['timezone']}")
    print(f"Saldo atual: R$ {contas[usuario_logado]['saldo']:.2f}")
    print("=====================================\n")

# Menu pós-login
def menu_usuario():
    while True:
        opcao = input(menu)
        if opcao == "1":
            depositar()
        elif opcao == "2":
            sacar()
        elif opcao == "3":
            extrato()
        elif opcao == "4":
            print("Saindo...\n")
            break
        else:
            print("Opção inválida.\n")

# Programa principal
def main():
    carregar_dados()
    while True:
        print("===== SISTEMA BANCÁRIO =====")
        print("[1] Cadastrar usuário")
        print("[2] Fazer login")
        print("[3] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            if login():
                menu_usuario()
        elif opcao == "3":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    main()
