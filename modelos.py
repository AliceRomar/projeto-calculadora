from abc import ABC, abstractmethod


class Usuario:
    """Guarda a meta de calorias do usuário para a sessão atual."""

    def __init__(self):
        self._meta_calorica = 0.0

    def set_meta_calorica(self, meta: float):
        """Define a meta de calorias se o valor for positivo."""
        if meta > 0:
            self._meta_calorica = meta
        else:
            print("Erro: A meta de calorias deve ser uma valor positivo.")

    def get_meta_calorica(self) -> float:
        """Retorna o valor da meta de calorias definida."""
        return self._meta_calorica


class Alimento(ABC):
    """Classe base abstrata para todos os tipos de alimentos."""

    def __init__(self, nome: str):
        self._nome = nome

    @abstractmethod
    def calcular_calorias(self, quantidade: float) -> float:
        """Método abstrato para calcular calorias. A implementação varia."""
        pass

    @abstractmethod
    def to_dict(self):
        """Converte o objeto para um dicionário serializável em JSON."""
        pass

    def get_nome(self) -> str:
        """Retorna o nome do alimento."""
        return self._nome


class AlimentoPorGrama(Alimento):
    """Representa um alimento medido em gramas."""

    def __init__(self, nome: str, calorias_por_100g: float):
        super().__init__(nome)
        self._calorias_por_100g = calorias_por_100g

    def calcular_calorias(self, gramas: float) -> float:
        """Calcula as calorias com base no peso em gramas."""
        return (self._calorias_por_100g / 100) * gramas

    def to_dict(self):
        return {
            "tipo": "grama",
            "nome": self._nome,
            "calorias": self._calorias_por_100g,
        }


class AlimentoPorUnidade(Alimento):
    """Representa um alimento medido em unidades."""

    def __init__(self, nome: str, calorias_por_unidade: float):
        super().__init__(nome)
        self._calorias_por_unidade = calorias_por_unidade

    def calcular_calorias(self, unidades: float) -> float:
        """Calcula as calorias com base no número de unidades."""
        return self._calorias_por_unidade * unidades

    def to_dict(self):
        return {
            "tipo": "unidade",
            "nome": self._nome,
            "calorias": self._calorias_por_unidade,
        }


class ItemConsumido:
    """Representa a junção de um objeto Alimento com a quantidade consumida."""

    def __init__(self, alimento: Alimento, quantidade: float):
        self._alimento = alimento
        self._quantidade = quantidade

    def get_calorias(self) -> float:
        """Pede ao objeto Alimento associado para calcular suas calorias."""
        return self._alimento.calcular_calorias(self._quantidade)

    def get_descricao(self) -> str:
        """Retorna uma descrição textual do item para o resumo."""
        return f"{self._alimento.get_nome()}: {self._quantidade}"


class Refeicao:
    def __init__(self, nome: str):
        self._nome = nome
        self._itens = []

    def adicionar_item(self, alimento: Alimento, quantidade: float):
        """Criamos um ItemConsumido e o adiciona à lista da refeição."""
        item = ItemConsumido(alimento, quantidade)
        self._itens.append(item)

    def calcular_total_calorias(self) -> float:
        """Soma as calorias de todos os itens da refeição."""
        total = 0.0
        for item in self._itens:
            total += item.get_calorias()
        return total

    def get_nome(self) -> str:
        """Retorna o nome da refeição."""
        return self._nome

    def get_itens(self):
        """Retorna a lista de itens da refeição."""
        return self._itens


class InterfaceTerminal:
    """Responsável por exibir os resumos e interagir com o usuário no terminal."""

    def exibir_resumo(self, usuario: Usuario, refeicoes: list):
        """Recebe o usuário e a lista de refeições e exibe um resumo formatado."""
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
