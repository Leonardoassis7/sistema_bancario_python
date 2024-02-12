# menu que aparece para o cliente 
menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUE = 3

while True: #loop infinito
    
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito:"))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("operação inválida")    
        

    elif opcao == "s":
        valor = float(input("Informe o valor do saque:"))

        exedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUE

        if excedeu_saques:
            print("Operação inválida! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação inválida! O Valor do saque excede o Limite.")

        elif excedeu_saques:
            print("Operação inválida! Numero maximo de saques excedido.")  

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1 

        else:
            print("Operação inválida! ")               

    elif opcao == "e":
        print("\n========== Extrato ==========")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("===============================")


    elif opcao == "q":
        break

    else:
        print ("Operação invalida, por favor selecione novamente a operacão desejada.")