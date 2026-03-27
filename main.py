import time
import sys

salas = [1501, 1502, 1504, 1508, 1701, 1703, 1704, 1706, 1710, 2201, 
             2202, 2203, 2204, 2301, 2302, 2303, 2304, 2501, 2502, 2503, 2603, 
             2701, 2702, 2703, 2704, 2801, 2802, 2803, 2804, 2901, 2902, 2903]
salas_reservadas = [1501, 2204]
reservadores = ["teste"]

def loading_fake(duracao=2):
    inicio = time.time()
    estados = [".", "..", "..."]
    i = 0

    while time.time() - inicio < duracao:
        texto = estados[i % len(estados)]
        sys.stdout.write("\r" + " " * 30)
        sys.stdout.write("\r" + texto)
        sys.stdout.flush()
        time.sleep(0.25)
        i += 1
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()

def getlab(nome: str, opcao: str) -> str:
    

    if opcao == "1":
        print("\n→ Listando salas disponíveis...")
        loading_fake(2)
        print("→ Salas disponíveis:")
        
        for s in salas:
            if s in salas_reservadas:
                status = "RESERVADA"
            else:
                status = "DISPONÍVEL"
            print(f"  - Sala {s} | {status}")
        print("--Favor selecionar a opção desejada--")

    elif opcao == "2":
        print("\n→ Processo de reserva iniciado...")
        loading_fake(2)
        if nome in reservadores:
            print("✗Você já possui uma reserva ativa!\nSelecione outra opção!")
            return
        sala = input("→Informe a sala desejada para realizar reserva:")

    elif opcao == "3":
        print("\n→ Processo de consulta iniciado...")
        loading_fake(2)

    elif opcao == "4":
        print("\n→ Processo de cancelamento iniciado...")
        loading_fake(2)

    elif opcao == "5":
        print("\n⊗ Encerrando serviço de consulta")
        return False
    else:
        print("\n✗ Opção inválida! Escolha uma opção válida!")
    



# Serviço

print("▶ Iniciando serviço GetLab")
loading_fake(2)
user = input("Favor inserir nome de usuário: ")
loading_fake(1)
print("\n===== GETLAB =====\n")
print(f"Bem vindo, {user}!\n")
rodando = True
print("--Favor selecionar a opção desejada--")
while rodando:
    print("1- Listar todas as salas")
    print("2- Reservar uma sala")
    print("3- Consultar reserva atual")
    print("4- Cancelar reserva de sala")
    print("5- Encerrar serviço")
    opcao = input("Escolha: ")
    resposta = getlab(user, opcao)
    if resposta == False:
        rodando = False
