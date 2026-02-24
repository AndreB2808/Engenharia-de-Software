# Requisitos Fundamentais
# - Converter a temperatura de Celsius para Fahrenheit e vice-versa.
# - Possibilidade de alterar a temperatura a ser convertida sem necessidade reinicialização.
# - Mostrar o resultado da conversão de forma clara e precisa.

# Requisitos Não-Funcionais
# - Livre de
# - Interface de texto simples e compreensível

# ====================================
# CONVERSOR DE TEMPERATURA
# Exercício - Engenharia de Software
# ====================================
import time


def celsius_para_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_para_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def pedir_numero(prompt):
    while True:
        valor = input(prompt).strip()
        try:
            return float(valor)
        except ValueError:
            print("Entrada inválida. Digite apenas números.")

print("="*40)
print("  CONVERSOR DE TEMPERATURA")
print("="*40)

while True:
    print("Escolha para qual escala deseja converter:")
    print("1. Celsius → Fahrenheit")
    print("2. Fahrenheit → Celsius")
    opcao = input("Digite a opção (1 ou 2): ")

    if opcao == '1':
        temp_celsius = pedir_numero("Digite a temperatura em Celsius: ")
        resultado = celsius_para_fahrenheit(temp_celsius)
        print(f"{temp_celsius}°C é igual a {resultado:.2f}°F")
    elif opcao == '2':
        temp_fahrenheit = pedir_numero("Digite a temperatura em Fahrenheit: ")
        resultado = fahrenheit_para_celsius(temp_fahrenheit)
        print(f"{temp_fahrenheit}°F é igual a {resultado:.2f}°C")
    else:
        print("Opção inválida. Por favor, escolha 1 ou 2.\n")
        continue

    continuar = input("Deseja fazer outra conversão? (s/n): ").strip().lower()
    if continuar != 's':
        print("Programa encerrado.")
        time.sleep(1.5)
        break