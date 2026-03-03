# Requisitos Fundamentais
# - O sistema deve validar o nome do exercício
# - O peso deve estar entre 1 e 300 kg
# - As repetições devem estar entre 1 e 50

# Requisitos Não-Funcionais
# - O registro deve ocorrer em menos de 200ms
# - O sistema deve ser curto e simples de se entender a fim de ser o mais rápido possível
# - O sistema deve ser fácil de modificar para permitir a adição de novos exercícios no futuro

# ====================================
# CONVERSOR DE TEMPERATURA
# Exercício - Engenharia de Software
# ====================================
import time

print("🏋️ GymTrack — Validador de Treino")
print("=" * 40)

# --- DADOS DO TREINO (mude os valores para testar!) ---
exercicio = "Supino Reto"
peso_kg   = 80
repeticoes = 10

# -------------------------------------------------------
# RF01 — O sistema deve validar o nome do exercício
# (não pode ser vazio)
# -------------------------------------------------------
if exercicio != "":
    print("✅ Nome do exercício válido: " + exercicio)
else:
    print("❌ Nome do exercício inválido (não pode ser vazio).")
# -------------------------------------------------------
# RF02 — O peso deve estar entre 1 e 300 kg
# -------------------------------------------------------
if 1 <= peso_kg <= 300:
    print("✅ Peso válido: " + str(peso_kg) + "kg")
else:
    print("❌ Peso inválido (deve estar entre 1 e 300 kg).")
# -------------------------------------------------------
# RF03 — As repetições devem estar entre 1 e 50
# -------------------------------------------------------
if 1 <= repeticoes <= 50:
    print("✅ Repetições válidas: " + str(repeticoes))
else:
    print("❌ Repetições inválidas (deve estar entre 1 e 50).")
# -------------------------------------------------------
# RNF01 — O registro deve ocorrer em menos de 200ms
# -------------------------------------------------------
inicio = time.time()
time.sleep(0.05)
print(f"✅ Série registrada: {exercicio} | {peso_kg}kg x {repeticoes} reps")
fim = time.time()
tempo_ms = (fim - inicio) * 1000
if tempo_ms < 200:
    print(f"✅Tempo de registro: {tempo_ms:.0f}ms ← dentro do limite!")
else:
    print(f"❌Lento demais: {tempo_ms:.0f}ms ← limite é 200ms")

# REFLEXÃO:
# 1. Qual a diferença entre RF e RNF que você percebeu na prática?
# - RF descrevem tarefas que o sistema deve fazer, enquanto RNF são requisitos que o sistema deve possuir.
# 2. O que aconteceria se esquecêssemos o RNF de performance?
# - O sistema poderia ficar lento ou sofrer de outras falhas a longo prazo.
# 3. Cite 1 RNF que o GymTrack deveria ter mas que você não implementou
# -  Compatibilidade com diferentes dispositivos.  
