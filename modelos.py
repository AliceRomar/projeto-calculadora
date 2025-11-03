from abc import ABC, abstractmethod


class Usuario:

    def __init__(self):
        self._meta_calorica = 0.0

    def set_meta_calorica(self, meta: float):
        if meta > 0:
            self._meta_calorica = meta
        else:
            print("Erro: A meta de calorias deve ser uma valor positivo.")

    def get_meta_calorica(self) -> float:
        return self._meta_calorica


class Alimento(ABC):

    def __init__(self, nome: str):
        self._nome = nome

    @abstractmethod
    def calcular_calorias(self, quantidade: float) -> float:
        pass

    @abstractmethod
    def to_dict(self):
        pass

    def get_nome(self) -> str:
        return self._nome


class AlimentoPorGrama(Alimento):

    def __init__(self, nome: str, calorias_por_100g: float):
        super().__init__(nome)
        self._calorias_por_100g = calorias_por_100g

    def calcular_calorias(self, gramas: float) -> float:
        return (self._calorias_por_100g / 100) * gramas

    def to_dict(self):
        return {
            "tipo": "grama",
            "nome": self._nome,
            "calorias": self._calorias_por_100g,
        }


class AlimentoPorUnidade(Alimento):

    def __init__(self, nome: str, calorias_por_unidade: float):
        super().__init__(nome)
        self._calorias_por_unidade = calorias_por_unidade

    def calcular_calorias(self, unidades: float) -> float:
        return self._calorias_por_unidade * unidades

    def to_dict(self):
        return {
            "tipo": "unidade",
            "nome": self._nome,
            "calorias": self._calorias_por_unidade,
        }


class ItemConsumido:

    def __init__(self, alimento: Alimento, quantidade: float):
        self._alimento = alimento
        self._quantidade = quantidade

    def get_calorias(self) -> float:
        return self._alimento.calcular_calorias(self._quantidade)

    def get_descricao(self) -> str:
        return f"{self._alimento.get_nome()}: {self._quantidade}"


class Refeicao:
    def __init__(self, nome: str):
        self._nome = nome
        self._itens = []

    def adicionar_item(self, alimento: Alimento, quantidade: float):
        item = ItemConsumido(alimento, quantidade)
        self._itens.append(item)

    def calcular_total_calorias(self) -> float:
        total = 0.0
        for item in self._itens:
            total += item.get_calorias()
        return total

    def get_nome(self) -> str:
        return self._nome

    def get_itens(self):
        return self._itens


class InterfaceTerminal:

    def exibir_resumo(self, usuario: Usuario, refeicoes: list):
        print("\n--- RESUMO DIÁRIO ---")
        total_calorias_dia = 0.0

        for refeicao in refeicoes:
            calorias_refeicao = refeicao.calcular_total_calorias()
            total_calorias_dia += calorias_refeicao
            print(f"\nRefeição: {refeicao.get_nome()} ({calorias_refeicao:.2f} kcal)")

            for item in refeicao.get_itens():
                print(f"  - {item.get_descricao()} ({item.get_calorias():.2f} kcal)")

        print("\n---------------------")
        print(f"Total de Calorias Consumidas: {total_calorias_dia:.2f} kcal")

        meta = usuario.get_meta_calorica()
        restante = meta - total_calorias_dia

        print(f"Meta Diária: {meta:.2f} kcal")
        if restante >= 0:
            print(f"Calorias Restantes: {restante:.2f} kcal")
        else:
            # abs() pega o valor absoluto (sem o sinal de negativo)
            print(f"Você excedeu a meta em {abs(restante):.2f} kcal")
        print("---------------------")
