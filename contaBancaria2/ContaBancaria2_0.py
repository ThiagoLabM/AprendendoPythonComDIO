from datetime import datetime
import pytz
from tzlocal import get_localzone

menu = """
================ MENU =================
Escolha uma opção:
[r] Registrar usuário
[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar Conta
[q] Sair
=======================================
"""

limite = 500
LIMITE_TASACAO = 3
cad = {}      # Cadastro de usuários
contas = {}   # Contas bancárias

def data_hora():
    data = datetime.now(pytz.timezone('America/Sao_Paulo'))
    data_formatada = data.strftime("%d-%m-%Y")
    hora_formatada = data.strftime("%H:%M:%S")
    timezone = get_localzone()
    return data_formatada, hora_formatada, timezone

def conta_NTransacao(nome, data):
    return len(contas[nome]["data_transacao"].get(data, {}))

def cadastroUsuario(**args):
    nome = args['nome']
    telefone = args['telefone']
    endereco = args['endereco']
    cpf = args['cpf']
    cad[nome] = {
        "nome": nome,
        "telefone": telefone,
        "endereco": endereco,
        "cpf": cpf
    }
    print(f"\nCadastro realizado com sucesso!\nNome: {nome}, Telefone: {telefone}, Endereço: {endereco}, CPF: {cpf}\n")

def cadastraBanco(**args):
    saldo = args['saldo']
    nome = args['nome']
    if nome not in cad:
        print("Usuário não cadastrado. Cadastre o usuário primeiro.\n")
        return
    if saldo < 0:
        print("Operação falhou! O saldo não pode ser negativo.\n")
        return
    contas[nome] = {
        "nome": nome,
        "saldo": saldo,
        "data_transacao": {},
        "ntransacao": LIMITE_TASACAO
    }
    print(f"\nConta criada com sucesso! Saldo inicial: R$ {saldo:.2f}\n")

def saque(**args):
    valor = args['valor']
    nome = args['nome']

    if nome not in contas:
        print("Usuário não possui conta.\n")
        return

    saldo = contas[nome]['saldo']
    data, hora, timezone = data_hora()

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.\n")
        return
    if valor > saldo:
        print(f"Saldo insuficiente. Saldo atual: R$ {saldo:.2f}\n")
        return
    if valor > limite:
        print(f"Valor excede o limite de saque: R$ {limite:.2f}\n")
        return
    if conta_NTransacao(nome, data) >= contas[nome]['ntransacao']:
        print(f"Número máximo de transações diárias atingido.\n")
        return

    contas[nome]['saldo'] -= valor
    if data not in contas[nome]['data_transacao']:
        contas[nome]['data_transacao'][data] = {}

    id_transacao = conta_NTransacao(nome, data) + 1
    contas[nome]['data_transacao'][data][id_transacao] = {
        'tipo': "saque",
        'valor': valor,
        'hora': hora,
        'timezone': timezone
    }

    print(f"Saque de R$ {valor:.2f} realizado com sucesso!\nSaldo atual: R$ {contas[nome]['saldo']:.2f}\n")

def deposito(**args):
    valor = args['valor']
    nome = args['nome']

    if nome not in contas:
        print("Usuário não possui conta.\n")
        return

    if valor <= 0:
        print("Operação falhou! Valor inválido.\n")
        return

    data, hora, timezone = data_hora()

    if conta_NTransacao(nome, data) >= contas[nome]['ntransacao']:
        print("Número máximo de transações diárias atingido.\n")
        return

    contas[nome]['saldo'] += valor
    if data not in contas[nome]['data_transacao']:
        contas[nome]['data_transacao'][data] = {}

    id_transacao = conta_NTransacao(nome, data) + 1
    contas[nome]['data_transacao'][data][id_transacao] = {
        'tipo': "deposito",
        'valor': valor,
        'hora': hora,
        'timezone': timezone
    }

    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\nSaldo atual: R$ {contas[nome]['saldo']:.2f}\n")

def extrato(**args):
    nome = args['nome']
    data = args['data']

    if nome not in contas:
        print("Usuário não possui conta.\n")
        return

    if data not in contas[nome]['data_transacao']:
        print(f"Nenhuma transação encontrada para a data {data}.\n")
        return

    mensagem = f"""
==================== EXTRATO ====================
Data: {data}
-------------------------------------------------
"""

    for id, dados in contas[nome]['data_transacao'][data].items():
        mensagem += f"{id} - {dados['tipo'].capitalize()} - R$ {dados['valor']:.2f} - {dados['hora']} - {dados['timezone']}\n"

    mensagem += f"-------------------------------------------------\nSaldo atual: R$ {contas[nome]['saldo']:.2f}\n==================================================\n"
    print(mensagem)

# ================= INICIALIZAÇÃO DE USUÁRIOS ==================
usuarios_iniciais = [
    {"nome": "Thiago", "telefone": "123456789", "endereco": "Rua A, 123", "cpf": "123.456.789-00"},
    {"nome": "Lucas", "telefone": "987654321", "endereco": "Rua B, 456", "cpf": "987.654.321-00"},
    {"nome": "Ana", "telefone": "456789123", "endereco": "Rua C, 789", "cpf": "456.789.123-00"},
    {"nome": "Maria", "telefone": "321654987", "endereco": "Rua D, 101", "cpf": "321.654.987-00"},
    {"nome": "João", "telefone": "654321789", "endereco": "Rua E, 202", "cpf": "654.321.789-00"}
]

for u in usuarios_iniciais:
    cadastroUsuario(**u)

for nome, saldo in zip(["Thiago", "Lucas", "Ana", "Maria", "João"], [0.10, 0.20, 0.30, 0.40, 0.50]):
    cadastraBanco(nome=nome, saldo=saldo)

# ================= LOOP PRINCIPAL ==================
while True:
    opcao = input(menu).lower()

    if opcao == "r":
        nome = input("Digite o nome do usuário: ")
        if nome in cad:
            print("Usuário já cadastrado.\n")
            continue
        telefone = input("Digite o telefone: ")
        endereco = input("Digite o endereço: ")
        cpf = input("Digite o CPF: ")
        cadastroUsuario(nome=nome, telefone=telefone, endereco=endereco, cpf=cpf)

    elif opcao == "c":
        nome = input("Digite o nome do usuário: ")
        if nome not in cad:
            print("Usuário não cadastrado. Cadastre primeiro.\n")
            continue
        if nome in contas:
            print("Usuário já possui conta.\n")
            continue
        saldo = float(input("Digite o saldo inicial: "))
        cadastraBanco(nome=nome, saldo=saldo)

    elif opcao == "d":
        nome = input("Digite o nome do usuário: ")
        valor = float(input("Digite o valor do depósito: "))
        deposito(nome=nome, valor=valor)

    elif opcao == "s":
        nome = input("Digite o nome do usuário: ")
        valor = float(input("Digite o valor do saque: "))
        saque(nome=nome, valor=valor)

    elif opcao == "e":
        nome = input("Digite o nome do usuário: ")
        data = input("Digite a data (dd-mm-aaaa): ")
        extrato(nome=nome, data=data)

    elif opcao == "q":
        print("Obrigado por usar nosso banco. Até mais!")
        break

    else:
        print("Opção inválida. Tente novamente.\n")
