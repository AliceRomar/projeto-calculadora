
from modelos import Usuario, AlimentoPorGrama, AlimentoPorUnidade, Refeicao, InterfaceTerminal

print("--- Iniciando Simulação da Calculadora de Calorias ---")

print("\n1. Criando usuário e definindo a meta...")
usuario_teste = Usuario()
usuario_teste.set_meta_calorica(2000.0)
print(f"   -> Meta de calorias definida para: {usuario_teste.get_meta_calorica()} kcal")

print("\n2. Criando os tipos de alimentos que serão consumidos...")
arroz = AlimentoPorGrama(nome="Arroz Branco", calorias_por_100g=130)
bife = AlimentoPorGrama(nome="Bife Grelhado", calorias_por_100g=250)
maca = AlimentoPorUnidade(nome="Maçã", calorias_por_unidade=95)
banana = AlimentoPorUnidade(nome="Banana", calorias_por_unidade=105)
print("   -> Alimentos criados em memória.")

print("\n3. Montando as refeições do dia...")


almoco = Refeicao(nome="Almoço")

almoco.adicionar_item(arroz, 200)  # 200g de arroz
almoco.adicionar_item(bife, 150)   # 150g de bife
print(f"   -> Refeição '{almoco.get_nome()}' montada.")


lanche = Refeicao(nome="Lanche da Tarde")
lanche.adicionar_item(maca, 1)     # 1 maçã
lanche.adicionar_item(banana, 2)   # 2 bananas
print(f"   -> Refeição '{lanche.get_nome()}' montada.")

refeicoes_do_dia = [almoco, lanche]

print("\n4. Gerando o resumo final...")

interface = InterfaceTerminal()

interface.exibir_resumo(usuario_teste, refeicoes_do_dia)

print("\n--- Simulação Finalizada ---")
