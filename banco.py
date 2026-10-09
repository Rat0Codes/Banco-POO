from abc import ABC, abstractmethod


class ExcecaoValorInvalido(Exception):
    pass


class Conta(ABC):
    

    def __init__(self, titular: str, numero_conta: str, saldo_inicial: float = 0.0):
        self.titular = titular  
        self._numero_conta = numero_conta
        self.saldo = saldo_inicial  
    @property
    def titular(self) -> str:
        return self._titular

    @titular.setter
    def titular(self, valor: str):
        if not valor or not valor.strip():
            raise ExcecaoValorInvalido("O nome do titular não pode ser vazio.")
        self._titular = valor.strip()

    @property
    def numero_conta(self) -> str:
        return self._numero_conta

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float):
        if valor < 0:
            raise ExcecaoValorInvalido("O saldo não pode ser negativo.")
        self._saldo = valor

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ExcecaoValorInvalido("O valor do depósito deve ser positivo.")
        self._saldo += valor

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ExcecaoValorInvalido("O valor do saque deve ser positivo.")
        if valor > self._saldo:
            raise ExcecaoValorInvalido("Saldo insuficiente para esta operação.")
        self._saldo -= valor

    @abstractmethod
    def aplicar_taxa_manutencao(self) -> None:
        pass

    def __str__(self) -> str:
        return f"Conta {self._numero_conta} | Titular: {self._titular} | Saldo: R$ {self._saldo:.2f}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(titular='{self._titular}', numero_conta='{self._numero_conta}', saldo={self._saldo})"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Conta):
            return False
        return self._numero_conta == outro._numero_conta

    def __lt__(self, outro: "Conta") -> bool:
        if not isinstance(outro, Conta):
            return NotImplemented
        return self._saldo < outro._saldo


class ContaCorrente(Conta):

    def __init__(self, titular: str, numero_conta: str, saldo_inicial: float = 0.0, limite_cheque_especial: float = 500.0):
        super().__init__(titular, numero_conta, saldo_inicial)
        self.limite_cheque_especial = limite_cheque_especial

    @property
    def limite_cheque_especial(self) -> float:
        return self._limite_cheque_especial

    @limite_cheque_especial.setter
    def limite_cheque_especial(self, valor: float):
        if valor < 0:
            raise ExcecaoValorInvalido("O limite do cheque especial não pode ser negativo.")
        self._limite_cheque_especial = valor

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ExcecaoValorInvalido("O valor do saque deve ser positivo.")
        if valor > (self._saldo + self._limite_cheque_especial):
            raise ExcecaoValorInvalido("Saque excede o saldo e o limite de cheque especial disponível.")
        self._saldo -= valor

    def aplicar_taxa_manutencao(self) -> None:
        self._saldo -= 15.0

    def __str__(self) -> str:
        return f"[Conta Corrente] {super().__str__()} | Limite: R$ {self._limite_cheque_especial:.2f}"


class ContaPoupanca(Conta):

    def __init__(self, titular: str, numero_conta: str, saldo_inicial: float = 0.0, taxa_rendimento: float = 0.005):
        super().__init__(titular, numero_conta, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self) -> float:
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor: float):
        if valor < 0:
            raise ExcecaoValorInvalido("A taxa de rendimento não pode ser negativa.")
        self._taxa_rendimento = valor

    def aplicar_taxa_manutencao(self) -> None:
        rendimento = self._saldo * self._taxa_rendimento
        self._saldo += rendimento

    def __str__(self) -> str:
        return f"[Conta Poupança] {super().__str__()} | Taxa Rendimento: {self._taxa_rendimento * 100:.1f}%"


class ContaInvestimento(Conta):

    def __init__(self, titular: str, numero_conta: str, saldo_inicial: float = 0.0, perfil_risco: str = "Moderado"):
        super().__init__(titular, numero_conta, saldo_inicial)
        self.perfil_risco = perfil_risco

    @property
    def perfil_risco(self) -> str:
        return self._perfil_risco

    @perfil_risco.setter
    def perfil_risco(self, valor: str):
        perfis_validos = ["Conservador", "Moderado", "Arrojado"]
        if valor not in perfis_validos:
            raise ExcecaoValorInvalido(f"Perfil inválido. Escolha entre: {', '.join(perfis_validos)}")
        self._perfil_risco = valor

    def aplicar_taxa_manutencao(self) -> None:
        taxa = self._saldo * 0.01
        self._saldo -= taxa

    def __str__(self) -> str:
        return f"[Conta Investimento] {super().__str__()} | Perfil: {self._perfil_risco}"



if __name__ == "__main__":
    print("=== 1. CRIAÇÃO DE INSTÂNCIAS (10 OBJETOS) ===")
    
    contas = [
        ContaCorrente("Ana Silva", "CC-001", 1500.0, 1000.0),
        ContaCorrente("Bruno Lima", "CC-002", 500.0, 300.0),
        ContaCorrente("Carla Dias", "CC-003", 2500.0, 2000.0),
        ContaCorrente("Daniel Rocha", "CC-004", 100.0, 200.0),
        
        ContaPoupanca("Eduarda Costa", "CP-001", 3000.0),
        ContaPoupanca("Fernando Souza", "CP-002", 12000.0, 0.007),
        ContaPoupanca("Gabriela Ramos", "CP-003", 850.0),
        
        ContaInvestimento("Heitor Alves", "CI-001", 50000.0, "Arrojado"),
        ContaInvestimento("Isabela Martins", "CI-002", 15000.0, "Moderado"),
        ContaInvestimento("João Pedro", "CI-003", 2000.0, "Conservador")
    ]

    for c in contas:
        print(c)

    print("\n=== 2. DEMONSTRAÇÃO DE POLIMORFISMO ===")
    print("Aplicando o método 'aplicar_taxa_manutencao()' de forma polimórfica:\n")
    
    for conta in contas:
        saldo_anterior = conta.saldo
        conta.aplicar_taxa_manutencao()  # Cada classe executa uma lógica própria
        print(f"{conta.numero_conta} ({conta.__class__.__name__}): Saldo Anterior = R$ {saldo_anterior:.2f} -> Novo Saldo = R$ {conta.saldo:.2f}")

    print("\n=== 3. TESTE DE MÉTODOS ESPECIAIS (DUNDER) ===")
    c1 = contas[0]
    c2 = contas[1]
    
    print(f"repr(c1): {repr(c1)}")
    print(f"Comparação __eq__ (c1 == c2): {c1 == c2}")
    
    contas_ordenadas = sorted(contas)
    print("\nContas ordenadas pelo saldo (__lt__):")
    for c in contas_ordenadas:
        print(f"  R$ {c.saldo:.2f} - {c.titular} ({c.numero_conta})")

    print("\n=== 4. TRATAMENTO DE EXCEÇÕES E ENCAPSULAMENTO (@property) ===")
    
    try:
        print("\nTentando criar conta com saldo negativo...")
        c_invalida = ContaCorrente("Lucas", "CC-999", -200.0)
    except ExcecaoValorInvalido as e:
        print(f" Capturado com sucesso: {e}")

    try:
        print("\nTentando atribuir perfil de risco inválido...")
        c_invest = contas[7]
        c_invest.perfil_risco = "Super Arriscado"
    except ExcecaoValorInvalido as e:
        print(f" Capturado com sucesso: {e}")

    try:
        print("\nTentando realizar saque maior que o saldo + limite de cheque especial...")
        c_corrente = contas[1]  
        c_corrente.sacar(1000.0)
    except ExcecaoValorInvalido as e:
        print(f" Capturado com sucesso: {e}")