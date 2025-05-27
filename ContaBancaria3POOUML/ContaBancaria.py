from datetime import datetime
import pytz
from tzlocal import get_localzone


# =============== UTILITÁRIOS ===================
def data_hora():
    data = datetime.now(pytz.timezone('America/Sao_Paulo'))
    data_formatada = data.strftime("%d-%m-%Y")
    hora_formatada = data.strftime("%H:%M:%S")
    timezone = get_localzone()
    return data_formatada, hora_formatada, timezone


# =============== CLASSES ========================

class Cliente:
    def __init__(self, nome, telefone, endereco, cpf):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.cpf = cpf
        self.conta = None

    def vincular_conta(self, conta):
        self.conta = conta


class ContaBancaria:
    LIMITE_SAQUE = 500
    LIMITE_TRANSACOES = 3

    def __init__(self, cliente, saldo_inicial=0):
        self.cliente = cliente
        self.saldo = saldo_inicial
        self.transacoes = {}  # {'data': {id: dados}}
        cliente.vincular_conta(self)

    def contar_transacoes_dia(self, data):
        return len(self.transacoes.get(data, {}))

    def registrar_transacao(self, tipo, valor):
        data, hora, timezone = data_hora()

        if data not in self.transacoes:
            self.transacoes[data] = {}

        id_transacao = self.contar_transacoes_dia(data) + 1
        self.transacoes[data][id_transacao] = {
            'tipo': tipo,
            'valor': valor,
            'hora': hora,
            'timezone': timezone
        }

    def deposito(self, valor):
        if valor <= 0:
            print("Operação falhou! Valor inválido.\n")
            return

        if self.contar_transacoes_dia(data_hora()[0]) >= ContaBancaria.LIMITE_TRANSACOES:
            print("Número máximo de transações diárias atingido.\n")
            return

        self.saldo += valor
        self.registrar_transacao("Depósito", valor)
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\nSaldo atual: R$ {self.saldo:.2f}\n")

    def saque(self, valor):
        if valor <= 0:
            print("Operação falhou! Valor inválido.\n")
            return

        if valor > self.saldo:
            print(f"Saldo insuficiente. Saldo atual: R$ {self.saldo:.2f}\n")
            return

        if valor > ContaBancaria.LIMITE_SAQUE:
            print(f"Valor excede o limite de saque de R$ {ContaBancaria.LIMITE_SAQUE:.2f}\n")
            return

        if self.contar_transacoes_dia(data_hora()[0]) >= ContaBancaria.LIMITE_TRANSACOES:
            print("Número máximo de transações diárias atingido.\n")
            return

        self.saldo -= valor
        self.registrar_transacao("Saque", valor)
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!\nSaldo atual: R$ {self.saldo:.2f}\n")

    def extrato(self, data):
        if data not in self.transacoes:
            print(f"Nenhuma transação encontrada para a data {data}.\n")
            return

        mensagem = f"""
==================== EXTRATO ====================
Data: {data}
-------------------------------------------------
"""
        for id, dados in self.transacoes[data].items():
            mensagem += f"{id} - {dados['tipo']} - R$ {dados['valor']:.2f} - {dados['hora']} - {dados['timezone']}\n"

        mensagem += f"-------------------------------------------------\nSaldo atual: R$ {self.saldo:.2f}\n==================================================\n"
        print(mensagem)


# =============== SISTEMA =========================

class Banco:
    def __init__(self):
        self.clientes = {}

    def cadastrar_cliente(self, nome, telefone, endereco, cpf):
        if nome in self.clientes:
            print("Cliente já cadastrado.\n")
            return

        cliente = Cliente(nome, telefone, endereco, cpf)
        self.clientes[nome] = cliente
        print(f"Cliente {nome} cadastrado com sucesso!\n")

    def criar_conta(self, nome, saldo_inicial):
        cliente = self.clientes.get(nome)

        if not cliente:
            print("Cliente não cadastrado. Cadastre primeiro.\n")
            return

        if cliente.conta:
            print("Cliente já possui conta.\n")
            return

        if saldo_inicial < 0:
            print("Saldo inicial não pode ser negativo.\n")
            return

        ContaBancaria(cliente, saldo_inicial)
        print(f"Conta criada com sucesso para {nome} com saldo inicial de R$ {saldo_inicial:.2f}\n")

    def buscar_cliente(self, nome):
        return self.clientes.get(nome)


# =============== INICIALIZAÇÃO ===================

banco = Banco()

usuarios_iniciais = [
    {"nome": "Thiago", "telefone": "123456789", "endereco": "Rua A, 123", "cpf": "123.456.789-00"},
    {"nome": "Lucas", "telefone": "987654321", "endereco": "Rua B, 456", "cpf": "987.654.321-00"},
    {"nome": "Ana", "telefone": "456789123", "endereco": "Rua C, 789", "cpf": "456.789.123-00"},
    {"nome": "Maria", "telefone": "321654987", "endereco": "Rua D, 101", "cpf": "321.654.987-00"},
    {"nome": "João", "telefone": "654321789", "endereco": "Rua E, 202", "cpf": "654.321.789-00"}
]

for u in usuarios_iniciais:
    banco.cadastrar_cliente(**u)

for nome, saldo in zip(["Thiago", "Lucas", "Ana", "Maria", "João"], [0.10, 0.20, 0.30, 0.40, 0.50]):
    banco.criar_conta(nome, saldo)


# =============== MENU =========================

menu = """
================ MENU =================
Escolha uma opção:
[r] Registrar cliente
[c] Criar Conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=======================================
"""

while True:
    opcao = input(menu).lower()

    if opcao == "r":
        nome = input("Nome: ")
        if banco.buscar_cliente(nome):
            print("Cliente já cadastrado.\n")
            continue
        telefone = input("Telefone: ")
        endereco = input("Endereço: ")
        cpf = input("CPF: ")
        banco.cadastrar_cliente(nome, telefone, endereco, cpf)

    elif opcao == "c":
        nome = input("Nome do cliente: ")
        saldo = float(input("Saldo inicial: "))
        banco.criar_conta(nome, saldo)

    elif opcao == "d":
        nome = input("Nome do cliente: ")
        cliente = banco.buscar_cliente(nome)
        if not cliente or not cliente.conta:
            print("Cliente não possui conta.\n")
            continue
        valor = float(input("Valor do depósito: "))
        cliente.conta.deposito(valor)

    elif opcao == "s":
        nome = input("Nome do cliente: ")
        cliente = banco.buscar_cliente(nome)
        if not cliente or not cliente.conta:
            print("Cliente não possui conta.\n")
            continue
        valor = float(input("Valor do saque: "))
        cliente.conta.saque(valor)

    elif opcao == "e":
        nome = input("Nome do cliente: ")
        cliente = banco.buscar_cliente(nome)
        if not cliente or not cliente.conta:
            print("Cliente não possui conta.\n")
            continue
        data = input("Digite a data (dd-mm-aaaa): ")
        cliente.conta.extrato(data)

    elif opcao == "q":
        print("Obrigado por utilizar nosso banco. Até mais!")
        break

    else:
        print("Opção inválida. Tente novamente.\n")
