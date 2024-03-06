from abc import ABC, abstractclassmethod, abstractproperty 
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco): 
        self.endereco = endereco #argumento cliente 
        self.contas = []  #conta inicia facil, não coloquei no construtor 

    def realizar_transacao(self, conta, transacao): # mapear as transação e conta 
        transacao.registrar(conta)

    def adicionar_conta(self, conta): # recebe so a conta
        self.contas.append(conta)  # ele adiciona essa conta recebida por parametros. aqui no nosso array de contas 

class PessoaFisica(Cliente): 
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)  #chamei o construtor da classe pai que no caso é o (endereço)
        self.nome = nome   #atribuir (nome, data_nascimento, cpf) que recebi do meu construtor
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero , cliente):    #atributos privados esses saldo, numero, agencia, cliente,historico
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()        

    @classmethod
    def nova_conta(cls, cliente, numero): # mapear classmethod de nova conta
        return cls(numero, cliente) # que recebe cliente e numero, e retorna uma instancia de conta 

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    #são as operações 
    def sacar(self, valor):
        self = self.saldo
        excedeu_saldo = valor > valor

        if excedeu_saldo:
            print("\n==== Operação falhou! Você não tem saldo suficiente. ====")

        elif valor > 0:
            self._saldo -= valor
            print("\n==== Saque realizado com Sucesso! ====")
            return True

        else:
            print("\n==== operação falhou! O Valor informado é inválido. ====")

        return False 
    
    def depositar(self, valor):  
        if valor > 0:
            self._self += valor
            print("\n==== Depósito realizado com Sucesso ! ====")
        else:
            print("\n=== Operação falhou! O valor informado é inválido. ====")
            return False

        return True           
                    
class ContaCorrente(Conta): 
    def __init__(self, numero, cliente, limite=500, limite_saques= 3):
        super().__init__(numero, cliente) #construtor 
        self.limite = limite  
        self.limite_saque = limite_saques

    def sacar(self, valor):  #aqui tem que fazer algumas validações
        numero_saques = len(  #tamanho da lista com o len
            [transacao for transacao in self.historico. # aqui é uma compressão de lista com histórico, todas as transações da conta 
            transacoes if transacao["tipo"] == Saque.
            __name__]
        )

        excedeu_limte = valor > self.limite
        excedeu_saques = numero_saques >- self.limite_saques

        if excedeu_limte:
            print("\n==== Operação falhou! O Valor do saque excede o limite. ====")

        elif excedeu_saques:
            print("\n ==== Operação falhou! Número Máximo de saques excedido. ====")

        else:
            return super().sacar(valor)  #metodo pai
        
        return False

    def __str__(self):  #aqui é uma representação da classe 
        return f"""\n
            Agência:\n{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []  #lista de transações

    @property
    def transacoes(self):
        return self._transacoes  #tem a propiedade para pegar as transaçoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
           #aqui é um adicionario
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime  #data atual do sistema 
                ("%d-%m-%Y %H:%M:%s"),  #%d é dia, %m mes, %Y ano, %H horas, % M minutos , %S segundos
            }
        )    

class Transacao(ABC): #interface de transação. que é uma classe abstratas 
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass
  
class Saque(Transacao): # mapear o saque
    def __init__(self,valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor 
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)  

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)   

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
   
    @property
    def valor(self):
        return self._valor 
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)   


def menu():
    
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))            

def filtrar_cliente(cpf, clientes):  #são objetos 
    clientes_filtrados = [cliente for cliente in 
    clientes if cliente.cpf == cpf] #é uma estancia da classe cliente 
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n==== Cliente não possui conta! ====")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n==== Cliente não encontrado! ====")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n==== Cliente não encontrado! ====")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n==== Cliente não encontrado! ====")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n==== Já existe cliente com esse CPF! ====")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n==== Cliente não encontrado, fluxo de criação de conta encerrado! ====")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n==== Operação inválida, por favor selecione novamente a operação desejada. =====")


main()