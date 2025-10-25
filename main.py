from modelos import (
    Usuario,
    AlimentoPorGrama,
    AlimentoPorUnidade,
    Refeicao,
    InterfaceTerminal
)

def definir_meta_usuario(usuario: Usuario):
    print("\n DEFINIR META DE CALORIAS")
    while True:
        try:
            meta_str = input("Digite sua meta diária de calorias (ex: 2000):")
            meta_float = float(meta_str)
            usuario.set_meta_calorica(meta_float)

            if usuario.get_meta_calorica() == meta_float:
                print(f"Meta de {meta_float}kcal definida com sucesso!")
                break
            else:
                print("Por favor, digite uma valor positivo.")

        except ValueError:
            print("Entrada inválida. Por favor, digite apenas números.")

def adicionar_refeicao(lista_de_refeicoes: list):
    print("\n ADICIONAR NOVA REFEIÇÃO")

    nome_refeicao = input("Qual o nome da refeição? (ex: Café da Manhã, Almoço)\n")
    nova_refeicao = Refeicao(nome_refeicao)

    while True:
        print(f"\nAdicionando alimento para '{nome_refeicao}':")
        nome_alimento = input(" Nome do alimento: \n")

        while True:
            tipo_medida = input(" Como ele é medido? [1]Por Grama [2]Por Unidade: \n")
            if tipo_medida in ['1', '2']:
                break
            print(" Opção inválida. Digite 1 ou 2.")

        try:
            if tipo_medida == '1':
                cal_por_100g = float(input(" Calorias a cada 100g: "))
                gramas = float(input(" Quantas gramas você consumiu? "))

                alimento = AlimentoPorGrama(nome_alimento, cal_por_100g)
                quantidade = gramas

            else:
                cal_por_unidade = float(input(" Calorias por unidade: "))
                unidades = float(input(" Quantas unidades você consumiu? "))

                alimento = AlimentoPorUnidade(nome_alimento, cal_por_unidade)
                quantidade = unidades

            nova_refeicao.adicionar_item(alimento, quantidade)
            print(f"'{nome_alimento}' adicionado à refeição!")
        except ValueError:
            print(" Erro: Você digitou uma valor inválido. Tente adicionar este alimento novamente.")
            continue

        continuar = input("\nDeseja adionar outro alimento a esta refeição? [s/n]: ").lower()
        if continuar != 's':
            break
    lista_de_refeicoes.append(nova_refeicao)
    print(f"Refeição '{nome_refeicao}' adicionada com sucesso!")

def ver_resumo(usuario: Usuario, lista_de_refeicoes: list, interface: InterfaceTerminal):
    if not lista_de_refeicoes:
        print("\nVocê ainda não adicionou nenhuma refeição hoje.")
        return

    interface.exibir_resumo(usuario, lista_de_refeicoes)

def main():
    usuario = Usuario()
    lista_de_refeicoes = []
    interface = InterfaceTerminal()

    print ("Calculadora de Calorias")

    while True:
        print("\n MENU PRINCIPAL ")
        print("1. Definir meta de calorias diárias")
        print("2. Adicionar Refeição (Montar Refeição)")
        print("3. Ver resumo diário")
        print("0. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == '1':
            definir_meta_usuario(usuario)

        elif escolha == '2':
            adicionar_refeicao(lista_de_refeicoes)

        elif escolha == '3':
            ver_resumo(usuario, lista_de_refeicoes, interface)

        elif escolha == '0':
            print("\nObrigado por usar a Calculadora!")
            break

        else:
            print("\nOpção inválida! Por favor, tente novamente.")
if __name__ == "__main__":
    main()
