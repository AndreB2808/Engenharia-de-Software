import time
import sys
import json
import os

ARQUIVO_DADOS = "data/reservas.json"

def txt_reserva():
    return "\n<==Favor selecionar a opção desejada==>"

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        print("⚠ Arquivo reservas.json não encontrado!")
        print("→ Criando arquivo padrão...")

        dados_iniciais = {"reservas": []}

        with open(ARQUIVO_DADOS, "w") as f:
            json.dump(dados_iniciais, f, indent=4)

        print("✔ Arquivo reservas.json criado com sucesso!")
        return dados_iniciais

    try:
        with open(ARQUIVO_DADOS, "r") as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        print("⚠ Erro ao ler reservas.json (arquivo corrompido)")
        print("→ Resetando arquivo...")

        dados = {"reservas": []}

        with open(ARQUIVO_DADOS, "w") as f:
            json.dump(dados, f, indent=4)

        print("✔ Arquivo corrigido!")
        return dados

    # Garantir estrutura correta
    if "reservas" not in dados:
        print("⚠ Estrutura inválida detectada")
        print("→ Corrigindo estrutura do arquivo...")

        dados["reservas"] = []

        with open(ARQUIVO_DADOS, "w") as f:
            json.dump(dados, f, indent=4)

        print("✔ Estrutura corrigida!")

    return dados

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(dados, f, indent=4)

salas = [1501, 1502, 1504, 1508, 1701, 1703, 1704, 
         1706, 1710, 2201, 2202, 2203, 2204, 2301, 
         2302, 2303, 2304, 2501, 2502, 2503, 2603, 
         2701, 2702, 2703, 2704, 2801, 2802, 2803, 
         2804, 2901, 2902, 2903]
dados = carregar_dados()
reservas = dados["reservas"]

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
            if any(r["sala"] == s for r in reservas):
                status = "RESERVADA"
            else:
                status = "Disponível"
            print(f"  - Sala {s} | {status}")
        time.sleep(2)
        print(txt_reserva())
#-------------------------------------------------------------------------------------------------    
    elif opcao == "2":
        print("\n→ Processo de reserva iniciado...")
        loading_fake(2)

        # Bloquear múltiplas reservas
        if any(r["usuario"] == nome for r in reservas):
            print("✗ Você já possui uma reserva ativa!")
            time.sleep(1)
            print(txt_reserva())
            return

        while True:
            entrada = input("→ Informe a sala desejada (ou 0 para cancelar): ")

            try:
                sala = int(entrada)
            except ValueError:
                print("✗ Entrada inválida! Digite apenas números.")
                time.sleep(1)
                continue

            if sala == 0:
                print("→ Processo de reserva cancelado.")
                time.sleep(2)
                print(txt_reserva())
                return

            # Sala existe?
            if sala not in salas:
                print("✗ Sala inválida!")
                time.sleep(1)
                continue

            # Sala ocupada?
            if any(r["sala"] == sala for r in reservas):
                print("✗ Sala já está reservada!")
                time.sleep(1)
                continue
            
            print(f"→ Processando pedido de reserva")
            loading_fake(3)
            reservas.append({
                "usuario": nome,
                "sala": sala
            })
            salvar_dados({"reservas": reservas})
            print(f"✔ Reserva realizada para sala {sala} no nome de {nome}!")
            time.sleep(2)
            print(txt_reserva())
            return
#-------------------------------------------------------------------------------------------------    
    elif opcao == "3":
        print("\n→ Consultando reserva...")
        loading_fake(2)

        reserva = next((r for r in reservas if r["usuario"] == nome), None)

        if reserva:
            print(f"✔ Você reservou a sala {reserva['sala']}.")
        else:
            print("✗ Você não possui reserva.")
        time.sleep(2)
        print(txt_reserva())
#-------------------------------------------------------------------------------------------------    
    elif opcao == "4":
        print("\n→ Processo de cancelamento iniciado...")
        loading_fake(2)

        reserva = next((r for r in reservas if r["usuario"] == nome), None)

        if reserva:
            print(f"→ Reserva encontrada: Sala {reserva['sala']}")

            escolha = input("→ Deseja cancelar? (s/n): ")

            if escolha.lower() == "s":
                loading_fake(3)
                reservas.remove(reserva)
                salvar_dados({"reservas": reservas})
                print("✔ Reserva cancelada!")
            else:
                print("✗ Cancelamento abortado.")
        else:
            print("✗ Você não possui reserva ativa.")

        time.sleep(2)
        print(txt_reserva())
#-------------------------------------------------------------------------------------------------    
    elif opcao == "5":
        print("\n⊗ Encerrando serviço de consulta")
        time.sleep(2)
        return False
    else:
        print("\n✗ Opção inválida! Escolha uma opção válida!")
        time.sleep(2)
    



# Serviço

print("▶ Iniciando serviço GetLab")
loading_fake(2)
user = input("Favor inserir nome de usuário: ")
loading_fake(1)
print("\n===== GETLAB =====\n")
print(f"Bem vindo, {user}!")
rodando = True
print(txt_reserva())
while rodando:
    print("1- Listar todas as salas")
    print("2- Reservar uma sala")
    print("3- Consultar reserva ativa")
    print("4- Cancelar reserva ativa")
    print("5- Encerrar serviço")
    opcao = input("Escolha: ")
    resposta = getlab(user, opcao)
    if resposta == False:
        rodando = False