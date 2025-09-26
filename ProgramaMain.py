import requests
import os

produtos = []
token = None

def limpartela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def entercontinuar():
    input("Pressione Enter para continuar...")

def registroProduto():   
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o valor do produto em yuans: "))
    peso = float(input("Digite o peso do produto em gramas: "))
    freteint = float(input("Digite o frete interno em yuan: "))

    produto = {
        "nome": nome,
        "preco": preco,
        "peso": peso,
        "freteint": freteint
    }
    produtos.append(produto)
    print("Produto registrado com sucesso!\n")

def listarProdutos():
    if not produtos:
        print("Nenhum produto foi encontrado!\n")
    else:
        print("\nProdutos Cadastrados:")
        for i, p in enumerate(produtos, start=1):
            print(f"{i}: {p['nome']} - {p['preco']}¥ - {p['peso']}g - {p['freteint']}¥")
        print()

def calcularFrete(pesofrete, frete):
    if frete == "YD-BR-line-D":
        peso_inicial = 100
        preco_inicial = 68
        peso_adicional = 2900
        preco_adicional = 391.50
        taxa_alfandegaria = 10.00
    elif frete == "YX-BR":
        peso_inicial = 100
        preco_inicial = 50
        peso_adicional = 2900
        preco_adicional = 275.50
        taxa_alfandegaria = 0.00
    else:
        print("Frete inválido!")
        return None

    if pesofrete <= peso_inicial:
        preco_total = preco_inicial
    else:
        excesso = pesofrete - peso_inicial
        blocos = excesso / peso_adicional
        preco_total = preco_inicial + blocos * preco_adicional

    preco_total += taxa_alfandegaria
    return preco_total

def obter_cotacao_yuan():
    global token
    if not token:
        token = input("\nCole aqui seu Token Wise: ")
    url = "https://api.transferwise.com/v1/rates?source=CNY&target=BRL"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        return dados[0]["rate"]
    else:
        print("Erro ao obter cotação:", response.status_code)
        return None

def conversorprodutos():
    cotacao = obter_cotacao_yuan()
    if cotacao:
        print("\nPreços convertidos para R$:")
        for p in produtos:
            preco_brl = p["preco"] + p["freteint"] * cotacao
            print(f"{p['nome']} custa {preco_brl:.2f} R$ ({p['preco']}, {p['freteint']} ¥) com frete local imbutido")
        print()

def conversorvalor():
    cotacao = obter_cotacao_yuan()
    if cotacao:
        valor = float(input("Qual valor em ¥ você deseja converter: "))
        valor = valor * cotacao
        print(f"\nO valor convertido é: R${valor:.2f}")

def freteManual():
    print("\nCalculando frete manualmente:")
    peso = float(input("Digite o peso do pacote em gramas: "))
    print("\nOpções de frete:\nYD-BR-line-D(eletrônicos)\nYX-BR")
    frete = input("Qual frete deseja usar?: ")
    
    preco_frete = calcularFrete(peso, frete)
    if preco_frete is None:
        return
    
    cotacao = obter_cotacao_yuan()
    if cotacao:
        preco_frete_brl = preco_frete * cotacao
        print(f"Valor do frete: ¥{preco_frete:.2f} ou R${preco_frete_brl:.2f}")
    else:
        print(f"Valor do frete: ¥{preco_frete:.2f} (cotação não disponível)")

def precofinal():
    if not produtos:
        print("Nenhum produto cadastrado!")
        return

    print("\nProdutos cadastrados:")
    for i, p in enumerate(produtos, start=1):
        print(f"{i}: {p['nome']} - {p['preco']}¥ - {p['peso']}g - Frete interno: {p['freteint']}¥")

    selecionados = input("\nDigite os números dos produtos que deseja enviar (ex: 1,3,4): ")
    indices = [int(x.strip()) - 1 for x in selecionados.split(",")]

    peso_total = 0
    for i in indices:
        if 0 <= i < len(produtos):
            peso_total += produtos[i]['peso']
        else:
            print(f"Produto {i+1} inválido, ignorado.")
    
    valprodutos = 0
    for i in indices:
        if 0 <= i < len(produtos):
            valprodutos += produtos[i]['preco'] + produtos[i]['freteint']
        else:
            print(f"Produto {i+1} inválido, ignorado.")

    print(f"\nPeso total dos produtos selecionados: {peso_total}g")

    print("\nOpções de frete:\nYD-BR-line-D(eletrônicos)\nYX-BR")
    frete = input("Qual frete deseja usar?: ")

    valfrete_produtos = calcularFrete(peso_total, frete)
    if valfrete_produtos is None:
        return
    

    print("\nDivisão do frete proporcional ao peso do produto:")
    total_yuans = 0
    cotacao = obter_cotacao_yuan()
    for i in indices:
        if 0 <= i <len(produtos):
            p = produtos[i]
            prop_frete = (p['peso'] / peso_total) * valfrete_produtos
            subtotal = p['preco'] + p['freteint'] + prop_frete
            total_yuans += subtotal
            if cotacao:
                subtotal_brl = subtotal * cotacao
                print(f"\n{p['nome']}: {p['preco']}¥ + {p['freteint']}¥ (frete interno) + {prop_frete:.2f}¥ (frete internacional) = {subtotal:.2f}¥ ou R${subtotal_brl:.2f}")
            else:
                print(f"{p['nome']}: {p['preco']}¥ + {p['freteint']}¥ (frete interno) + {prop_frete:.2f}¥ (frete internacional) = {subtotal:.2f}¥")
            
    if cotacao:
        total_brl = total_yuans * cotacao
        print(f"\nO valor total utilizando o frete {frete} é: ¥{total_yuans:.2f} ou R${total_brl:.2f}")
    else:
        print(f"\nO valor total utilizando o frete {frete} é: ¥{total_yuans:.2f} (cotação não disponível)")

def main():
    while True: 
        limpartela()
        print("-------MENU-------"
              "\n1 - Registrar Produtos"
              "\n2 - Listar Produtos"
              "\n3 - Calcular frete (peso total manual)"
              "\n4 - Converter Preço dos produtos para BRL"
              "\n5 - Converter valor em ¥ para R$"
              "\n6 - Calcular valor final com frete (seleção de produtos)"
              "\n0 - Sair")
        opcao = int(input("Escolha sua opção: "))
        if opcao == 1:
            limpartela()
            registroProduto()
            entercontinuar()
        elif opcao == 2:
            limpartela()
            listarProdutos()
            entercontinuar()
        elif opcao == 3:
            limpartela()
            freteManual()
            entercontinuar()
        elif opcao == 4:
            limpartela()
            conversorprodutos()
            entercontinuar()
        elif opcao == 5:
            limpartela()
            conversorvalor()
            entercontinuar()
        elif opcao == 6:
            limpartela()
            precofinal()
            entercontinuar()
        elif opcao == 0:
            print("Saindo...")
            break
        else:
            print("Opção inválida!\n")
            entercontinuar()

def main_com_pausa():
    try:
        main()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main_com_pausa()
