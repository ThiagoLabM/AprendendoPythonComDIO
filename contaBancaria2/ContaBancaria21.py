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

prezado = ""
saudacao = f"""
================ BEM VINDO =================
Olá, seja bem vindo {prezado}ao nosso banco!
Aqui você pode criar uma conta, depositar, sacar e consultar o extrato.
===========================================
"""

saldo = 0
limite = 500
LIMITE_SAQUES = 3
contas = {}
cad = {}

def conta_NTransacao(nome, data):
    if nome in cad and "data_transacao" in cad[nome] and data in cad[nome]["data_transacao"]:
        return len(cad[nome]["data_transacao"][data])
    return 0

def data_hora():
    data = datetime.now(pytz.timezone('America/Sao_Paulo'))
    data_formatada = data.strftime("%d-%m-%Y")
    hora_formatada = data.strftime("%H:%M:%S")
    timezone = get_localzone()
    return data_formatada, hora_formatada, timezone    

def cadastroUsuario(**kwargs):
    nome = kwargs['nome']
    telefone = kwargs['telefone']
    endereco = kwargs['endereco']
    cpf = kwargs['cpf']
    
    cad[nome] = {
        "nome": nome,
        "telefone": telefone,
        "endereco": endereco,
        "cpf": cpf,
        "saldo": 0,
        "data_transacao": {},
        "ntransacao": LIMITE_SAQUES
    }
    print(f"Cadastro realizado com sucesso!\nNome: {nome}, Telefone: {telefone}, Endereço: {endereco}, CPF: {cpf}\n")
    print("=========================================\n")

def cadastraBanco(**kwargs):
    saldo = kwargs['saldo']
    nome = kwargs['nome']
    
    if nome not in cad:
        print("Operação falhou! O usuário não está cadastrado.\n")
        return
    
    if saldo < 0:
        print("Operação falhou! O saldo não pode ser negativo.\n")
        return
    
    cad[nome]["saldo"] = saldo
    print(f"Conta atualizada com sucesso!\nNome: {nome}, seu saldo é de: R$ {saldo:.2f}\n")

def saque(**kwargs):
    valor = kwargs['valor']
    nome = kwargs['nome']
    
    if nome not in cad:
        print("Operação falhou! Usuário não encontrado.\n")
        return
    
    saldo = cad[nome]["saldo"]
    data, _, _ = data_hora()
    
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.\n")
        return
    
    if valor > saldo:
        print(f"Operação falhou! Saldo insuficiente.\nSaldo atual: R$ {saldo:.2f}\n")
        return
    
    if valor > limite:
        print(f"Operação falhou! Valor excede o limite de R$ {limite:.2f} por saque.\n")
        return
    
    if conta_NTransacao(nome, data) >= LIMITE_SAQUES:
        print(f"Operação falhou! Limite de {LIMITE_SAQUES} saques diários atingido.\n")
        return
    
    # Realiza o saque
    cad[nome]["saldo"] -= valor
    
    # Registra a transação
    data, hora, timezone = data_hora()
    if data not in cad[nome]["data_transacao"]:
        cad[nome]["data_transacao"][data] = {}
    
    transacao_id = len(cad[nome]["data_transacao"][data]) + 1
    cad[nome]["data_transacao"][data][transacao_id] = {
        'tipo': "saque",
        'valor': valor,
        'hora': hora,
        'timezone': timezone
    }
    
    print(f"Saque realizado com sucesso!\nNovo saldo: R$ {cad[nome]['saldo']:.2f}\n")

def deposito(**kwargs):
    valor = kwargs['valor']
    nome = kwargs['nome']
    
    if nome not in cad:
        print("Operação falhou! Usuário não encontrado.\n")
        return
    
    if valor <= 0:
        print("Operação falhou! O valor deve ser positivo.\n")
        return
    
    # Realiza o depósito
    cad[nome]["saldo"] += valor
    
    # Registra a transação
    data, hora, timezone = data_hora()
    if data not in cad[nome]["data_transacao"]:
        cad[nome]["data_transacao"][data] = {}
    
    transacao_id = len(cad[nome]["data_transacao"][data]) + 1
    cad[nome]["data_transacao"][data][transacao_id] = {
        'tipo': "deposito",
        'valor': valor,
        'hora': hora,
        'timezone': timezone
    }
    
    print(f"Depósito realizado com sucesso!\nNovo saldo: R$ {cad[nome]['saldo']:.2f}\n")

def extrato(**kwargs):
    nome = kwargs['nome']
    data = kwargs['data']
    
    if nome not in cad:
        print("Operação falhou! Usuário não encontrado.\n")
        return
    
    if data not in cad[nome]["data_transacao"]:
        print(f"Nenhuma transação encontrada para a data {data}\n")
        return
    
    mensagem = f"""
==================== EXTRATO ====================
----------------------Data----------------------
---------------------{data}----------------------

"""
    for id, dados in cad[nome]["data_transacao"][data].items():
        mensagem += f"{id} - {dados['tipo'].capitalize()} - R$ {dados['valor']:.2f} - {dados['hora']} - {dados['timezone']}\n"
    
    mensagem += f"""
------------------------------------------------
Saldo atual: R$ {cad[nome]['saldo']:.2f}
================================================
"""
    print(mensagem)

# Dados iniciais para teste
usuarios_teste = [
    {"nome": "Thiago", "telefone": "123456789", "endereco": "Rua A, 123", "cpf": "123.456.789-00"},
    {"nome": "Lucas", "telefone": "987654321", "endereco": "Rua B, 456", "cpf": "987.654.321-00"},
    {"nome": "Ana", "telefone": "456789123", "endereco": "Rua C, 789", "cpf": "456.789.123-00"},
    {"nome": "Maria", "telefone": "321654987", "endereco": "Rua D, 101", "cpf": "321.654.987-00"},
    {"nome": "João", "telefone": "654321789", "endereco": "Rua E, 202", "cpf": "654.321.789-00"}
]

for usuario in usuarios_teste:
    cadastroUsuario(**usuario)
    cadastraBanco(nome=usuario['nome'], saldo=0.10 * (usuarios_teste.index(usuario) + 1))

# Loop principal
while True:
    opcao = input(menu).lower()

    if opcao == "r":
        nome = input("Digite o nome do usuário: ")
        if nome in cad:
            print("Operação falhou! Usuário já cadastrado.\n")
            continue
            
        telefone = input("Digite o telefone do usuário: ")
        endereco = input("Digite o endereço do usuário: ")
        cpf = input("Digite o CPF do usuário: ")
        cadastroUsuario(nome=nome, telefone=telefone, endereco=endereco, cpf=cpf)

    elif opcao == "c":
        nome = input("Digite o nome do usuário: ")
        if nome not in cad:
            print("Operação falhou! Usuário não cadastrado.\n")
            continue
            
        saldo = float(input("Digite o saldo inicial da conta: "))
        cadastraBanco(nome=nome, saldo=saldo)

    elif opcao == "d":
        nome = input("Digite o nome do usuário: ")
        if nome not in cad:
            print("Operação falhou! Usuário não encontrado.\n")
            continue
            
        valor = float(input("Informe o valor do depósito: "))
        deposito(nome=nome, valor=valor)

    elif opcao == "s":
        nome = input("Digite o nome do usuário: ")
        if nome not in cad:
            print("Operação falhou! Usuário não encontrado.\n")
            continue
            
        valor = float(input("Informe o valor do saque: "))
        saque(nome=nome, valor=valor)

    elif opcao == "e":
        nome = input("Digite o nome do usuário: ")
        if nome not in cad:
            print("Operação falhou! Usuário não encontrado.\n")
            continue
            
        data = input("Digite a data no formato dd-mm-aaaa: ")
        extrato(nome=nome, data=data)

    elif opcao == "q":
        print("Saindo do sistema...")
        break

    else:
        print("Operação inválida. Por favor, selecione uma opção válida.\n")