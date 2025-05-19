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
    salvar_dados()
    print(f"\nCadastro realizado com sucesso!\nNome: {nome}, Telefone: {telefone}, Endereço: {endereco}, CPF: {cpf}\n")
