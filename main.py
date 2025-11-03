import json
from modelos import (
    Usuario,
    AlimentoPorGrama,
    AlimentoPorUnidade,
    Refeicao,
    InterfaceTerminal,
)

NOME_ARQUIVOS_ALIMENTOS = "alimentos.json"


def carregar_alimentos_do_json():
    try:
        with open(NOME_ARQUIVOS_ALIMENTOS, "r") as f:
            lista_de_dicionarios = json.load(f)

        banco_de_alimentos = []

        for item in lista_de_dicionarios:
            if item["tipo"] == "grama":
                alimento = AlimentoPorGrama(item["nome"], item["calorias"])
            elif item["tipo"] == "unidade":
                alimento = AlimentoPorUnidade(item["nome"], item["calorias"])
            banco_de_alimentos.append(alimento)

        print(
            f"Banco de dados de alimentos carregados. {len(banco_de_alimentos)} alimentos encontrados."
        )
        return banco_de_alimentos
    except FileNotFoundError:
        print(
            "Arquivo de alimentos não encontrado. Começando com banco de dados vazio."
        )
        return []
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo JSON. Começando com banco de dados vazio.")
        return []


def salvar_alimentos_no_json(lista_de_alimentos: list):

    lista_para_salvar = [alimento.to_dict() for alimento in lista_de_alimentos]

    try:
        with open(NOME_ARQUIVOS_ALIMENTOS, "w") as f:
            # Salva a lista de dicionários no JSON
            json.dump(lista_para_salvar, f, indent=4)
    except IOError as e:
        print(f"Erro ao salvar alimentos no JSON: {e}")


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


def adicionar_refeicao(lista_de_refeicoes: list, banco_de_alimentos: list):
    print("\n ADICIONAR NOVA REFEIÇÃO")

    if not banco_de_alimentos:
        print("Erro: O banco de dados de alimentos está vazio.")
        print(
            "Por favor, vá ao menu '4. Gerenciar Banco de Alimentos' e cadastre alguns alimentos primeiro."
        )
        return

    nome_refeicao = input("Qual o nome da refeição? (ex: Café da Manhã, Almoço)\n")
    nova_refeicao = Refeicao(nome_refeicao)

    while True:
        print(f"\nAdicionando alimento para '{nome_refeicao}':")

        listar_alimentos(banco_de_alimentos)
        try:
            print("\nDigite o NÚMERO do alimento que deseja adicionar.")
            escolha_str = input("Ou digite [0] para cadastrar um novo alimento: ")
            escolha_num = int(escolha_str)

            if escolha_num == 0:
                # 5. Atalho para cadastrar um novo alimento
                adicionar_novo_alimento(banco_de_alimentos)
                print("--- Retornando à adição de refeição ---")
                continue

            indice = escolha_num - 1

            if 0 <= indice < len(banco_de_alimentos):
                alimento_escolhido = banco_de_alimentos[indice]

                if isinstance(alimento_escolhido, AlimentoPorGrama):
                    quantidade = float(
                        input(
                            f"  Quantas gramas de '{alimento_escolhido.get_nome()}'? "
                        )
                    )
                elif isinstance(alimento_escolhido, AlimentoPorUnidade):
                    quantidade = float(
                        input(
                            f"  Quantas unidades de '{alimento_escolhido.get_nome()}'? "
                        )
                    )
                else:
                    print("Erro: Tipo de alimento desconhecido.")
                    continue
                nova_refeicao.adicionar_item(alimento_escolhido, quantidade)
                print(f"'{alimento_escolhido.get_nome()}' adicionado à refeição!")

            else:
                print("Número inválido. Tente novamente.")

        except ValueError:
            print("Entrada inválida. Por favor, digite apenas números.")
            continue  # Reinicia o loop de adicionar alimento

        continuar = input(
            "\nDeseja adicionar outro alimento a esta refeição? [s/n]: "
        ).lower()
        if continuar != "s":
            break

        lista_de_refeicoes.append(nova_refeicao)
    print(f"Refeição '{nome_refeicao}' adicionada com sucesso!")


def ver_resumo(
    usuario: Usuario, lista_de_refeicoes: list, interface: InterfaceTerminal
):
    if not lista_de_refeicoes:
        print("\nVocê ainda não adicionou nenhuma refeição hoje.")
        return

    interface.exibir_resumo(usuario, lista_de_refeicoes)


def adicionar_novo_alimento(banco_de_alimentos: list):
    print("\n ADICIONAR NOVO ALIMENTO AO BANCO DE DADOS ")
    nome_alimento = input("Nome do alimento: ")
    for ali in banco_de_alimentos:
        if ali.get_nome().lower() == nome_alimento.lower():
            print("Erro: Um alimento com este nome já existe.")
            return
    while True:
        tipo_medida = input("Como ele é medido? [1]Por Grama [2]Por Unidade: ")
        if tipo_medida in ["1", "2"]:
            break
        print("Opção inválida. Digite 1 ou 2.")

    try:
        if tipo_medida == "1":
            cal_por_100g = float(input("  Calorias a cada 100g: "))
            alimento = AlimentoPorGrama(nome_alimento, cal_por_100g)
        else:  # tipo_medida == '2'
            cal_por_unidade = float(input("  Calorias por unidade: "))
            alimento = AlimentoPorUnidade(nome_alimento, cal_por_unidade)

        banco_de_alimentos.append(alimento)
        salvar_alimentos_no_json(banco_de_alimentos)
        print(f"Alimento '{nome_alimento}' cadastrado com sucesso!")

    except ValueError:
        print("Erro: Você digitou um valor inválido para calorias.")


def listar_alimentos(banco_de_alimentos: list):
    print("\n ALIMENTOS CADASTRADOS NO BANCO DE DADOS ")
    if not banco_de_alimentos:
        print("Nenhum alimento cadastrado.")
        return
    for i, alimento in enumerate(banco_de_alimentos):
        # Usamos o método to_dict() que criamos no modelos.py
        info = alimento.to_dict()
        if info["tipo"] == "grama":
            print(f"  {i+1}. {info['nome']} (Grama) - {info['calorias']} kcal/100g")
        else:  # unidade
            print(
                f"  {i+1}. {info['nome']} (Unidade) - {info['calorias']} kcal/unidade"
            )


def excluir_alimento(banco_de_alimentos: list):
    print("\n EXCLUIR ALIMENTO DO BANCO DE DADOS")
    listar_alimentos(banco_de_alimentos)

    if not banco_de_alimentos:
        return

    try:
        numero_str = input(
            "Digite o NÚMERO do alimento que deseja excluir (ou 0 para cancelar): "
        )
        indice = int(numero_str) - 1

        if indice == -1:
            print("Exclusão cancelada.")
            return
        if 0 <= indice < len(banco_de_alimentos):
            alimento_removido = banco_de_alimentos.pop(indice)

            salvar_alimentos_no_json(banco_de_alimentos)
            print(
                f"Alimento '{alimento_removido.get_nome()}' foi excluído com sucesso!"
            )
        else:
            print("Número inválido. Nenhum alimento foi excluído.")

    except ValueError:
        print("Entrada inválida. Por favor, digite apenas um número.")


def gerenciar_alimentos(banco_de_alimentos: list):
    while True:
        print("\n GERENCIAR BANCO DE ALIMENTOS ")
        print("1. Adicionar novo alimento")
        print("2. Listar alimentos cadastrados")
        print("3. Excluir alimento")
        print("0. Voltar ao menu principal")

        escolha_crud = input("Digite a opção desejada: ")

        if escolha_crud == "1":
            adicionar_novo_alimento(banco_de_alimentos)

        elif escolha_crud == "2":
            listar_alimentos(banco_de_alimentos)

        elif escolha_crud == "3":
            excluir_alimento(banco_de_alimentos)

        elif escolha_crud == "0":
            print("Voltando ao menu principal...")
            break

        else:
            print("Opção inválida. Tente novamente.")


def main():

    usuario = Usuario()
    lista_de_refeicoes = []
    interface = InterfaceTerminal()
    banco_de_alimentos = carregar_alimentos_do_json()
    interface = InterfaceTerminal()

    print("Calculadora de Calorias")

    while True:
        print("\n MENU PRINCIPAL ")
        print("1. Definir meta de calorias diárias")
        print("2. Adicionar Refeição (Montar Refeição)")
        print("3. Ver resumo diário")
        print("4. Gerenciar Banco de Alimentos")
        print("0. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            definir_meta_usuario(usuario)

        elif escolha == "2":
            adicionar_refeicao(lista_de_refeicoes, banco_de_alimentos)

        elif escolha == "3":
            ver_resumo(usuario, lista_de_refeicoes, interface)

        elif escolha == "4":
            gerenciar_alimentos(banco_de_alimentos)

        elif escolha == "0":
            print("\nObrigado por usar a Calculadora!")
            break

        else:
            print("\nOpção inválida! Por favor, tente novamente.")


if __name__ == "__main__":
    main()
