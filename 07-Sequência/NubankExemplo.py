class BancoDeDados:
    def __init__(self):
        self.saldos = {"user_123": 500.0}

    def verificar_saldo(self, user_id: str) -> float:
        return self.saldos.get(user_id, 0.0)

    def debitar(self, user_id: str, valor: float) -> bool:
        saldo_atual = self.verificar_saldo(user_id)
        
        if saldo_atual >= valor:
            self.saldos[user_id] = saldo_atual - valor
            return True
        else:
            return False

class ServidorNubank:
    def __init__(self):
        self.banco = BancoDeDados()

    def processar_transferencia(self, user_id: str, valor: float) -> dict:
        saldo_atual = self.banco.verificar_saldo(user_id)

        if saldo_atual >= valor:
            self.banco.debitar(user_id, valor)
            saldo_restante = self.banco.verificar_saldo(user_id)
            return {
                "status": "aprovado",
                "saldo_restante": saldo_restante
            }
        else:
            return {
                "status": "recusado",
                "motivo": "saldo insuficiente"
            }

class AppNubank:
    def __init__(self):
        self.servidor = ServidorNubank()

    def transferir(self, user_id: str, valor: float):
        print(f"[APP] Iniciando transferência de R$ {valor:.2f}...")
        resultado = self.servidor.processar_transferencia(user_id, valor)
        if resultado["status"] == "aprovado":
            print(f"✅ Aprovado! Saldo restante: R$ {resultado['saldo_restante']:.2f}")
        else:
            print(f"❌ Recusado! Motivo: {resultado['motivo']}")

# Testes
app = AppNubank()

print("=== Teste 1: Transferência dentro do saldo ===")
app.transferir("user_123", 200.0)

print("\n=== Teste 2: Transferência acima do saldo ===")
app.transferir("user_123", 500.0)

print("\n=== Teste 3: Múltiplas transferências ===")
app.transferir("user_123", 100.0)
app.transferir("user_123", 250.0)   