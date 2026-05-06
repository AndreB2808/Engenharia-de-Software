def cadastro_usuario(email: str, senha: str, email_ja_existe: bool, confirmou_email: bool) -> str:

    print("▶ Iniciando processo de cadastro...")
    
    print("→ Analisando email fornecido...")
    if email:
        if email_ja_existe:
            print("✗ Email inválido! Outra conta já está associada ao email fornecido!")
            return "⊗ ERRO: Cadastro falhou!"
        else:
            print("→ Email válido!")
    else:
        print("✗ Email inválido! Email inexistente!")
        return "⊗ ERRO: Cadastro falhou!"
    
    print("→ Analisando senha fornecida...")
    if senha:
        print("→ Senha válida!")
    else:
        print("✗ Senha inválida! Verifique novamente os requisitos!")
        return "⊗ ERRO: Cadastro falhou!"
    
    if email and senha and not email_ja_existe:
        print("→ Cadastro concluído! Favor realizar login após confirmação do email")
        print("→ Iniciando login com as informações fornecidas...")
        if confirmou_email:
            print("→ Cadastro concluído! Bem vindo!")
            return "⊗ SUCESSO: Login realizado!"
        else:
            print("✗ Email não verificado! Favor tentar novamente após confirmação!")
            return "⊗ ERRO: Email não verificado!"

# Testes (não apague!)
print(cadastro_usuario("joao@email.com", "senha123", False, True))
print("-------------------------------------------------------------------")
print(cadastro_usuario("email-invalido", "senha123", False, True))
print("-------------------------------------------------------------------")
print(cadastro_usuario("joao@email.com", "senha123", True, True))
print("-------------------------------------------------------------------")
print(cadastro_usuario("gyusamendes@email.com", "senha123", False, False))