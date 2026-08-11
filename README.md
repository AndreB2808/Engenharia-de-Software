# Projeto Servatio 🪙
### Do latim "Preservação" / "Guardando"​

**TEMA: Aplicativo de planejamento financeiro e construção de patrimônio para jovens (controle de gastos, metas e investimentos)**



## ⚙️ Descrição do Problema
A

## 💡 Proposta
B

## 🖥️ Tecnologias Necessárias
C

## 🗂️ Estrutura do Projeto
```
    Engenharia-De-Software/tree/Projeto-GetLab/
    ├── src/
    │   ├── auth/
    │   │   ├── cadastro.py
    │   │   └── login.py
    │   ├── data/
    │   │   ├── usuarios.json
    │   │   └── reservas.json
    │   ├── models/
    │   │   └── reserva_model.py
    │   ├── views/
    │   │   └── interface_view.py
    │   ├── main.py     
    ├── README.md
    └── requirements.txt
```

## 🔌 Como Executar
### Pré-requisitos
    - Python 3
    - Steamlit (caso esteja no Linux é necessário instalar dentro de uma venv) 
 Primeiramente é necessário baixar todos os arquivos do projeto. Após a instalação, e dentro de um programa como Visual Studio Code, abra a pasta principal que contêm todos os arquivos. Depois, abra um terminal novo e digite "pip install -r requirements.txt" para instalar as dependências requisitadas (neste caso sendo apenas o "Streamlit"), e então execute o projeto utilizando o comando "streamlit run src/app.py", que abrirá uma guia no navegador da aplicação, sendo possível cadastrar um usuário, fazer login e utilizar as funcionalidades do sistema diretamente pela interface visual.

## 🪢 Funcionalidades Implementadas

- ✔ Cadastro de usuários com RM e senha
- ✔ Login de usuários cadastrados
- ✔ Listagem de todas as salas com indicação de status (Disponível / Reservada)
- ✔ Funcionalidade de reservar sala e armazenar nos dados
- ✔ Bloqueio de múltiplas reservas por usuário
- ✔ Bloqueio de reserva em salas já ocupadas
- ✔ Consulta da reserva ativa do usuário
- ✔ Cancelamento de reserva com confirmação do usuário
- ✔ Persistência de dados utilizando um arquivo JSON ("usuarios.json" e "reservas.json")
- ✔ Tratamento de erros ou ausência do arquivo JSON
- ✔ Interface prática via Streamlit
- ✔ Alternância entre tema Light/Dark
- ✔ Exportação para formato csv das reservas ativas
- ✕ Validação de antecedência para cancelamento de reserva
- ✕ Validação de RM com base no banco de dados da FIAP
- ✕ Criptografia dos dados cadastrados

## ⭐ Diferencial
 1. Tema Light/Dark
 Foi escolhida a implementação de uma opção de escolher entre tema claro e escuro para a interface, justamente pela implementação da interface básica. A alternância de tema melhora a experiência do usuário, principalmente em diferentes condições de iluminação, reduzindo fadiga visual além de vários usuário optarem pela utilização de apenas um dos temas, e tornando o sistema mais acessível, 
 
 2. Exportação de reservas para .csv 
 Além da mudança de tema, como bônus, há uma opção de baixar em formato csv a lista atual de reservas. A exportação em csv permite que os dados não fiquem restritos apenas na aplicação, com usuários podendo organizar, compartilhar ou analisar informações de reservas da forma que acharem mais apropriado.

## 📹 Demonstração
- Exemplo de cadastro e login
![](gifs/gif1.gif)
- Processo de reserva de sala
![](gifs/gif2.gif)
- Cancelamento de reserva
![](gifs/gif3.gif)
- Demonstração do tema Light/Dark
  
![](gifs/LD1.gif)
![](gifs/LD2.gif)

## 📑 Documentos (Miro, repositório, vídeo)
▶️ Quadro no Miro - https://miro.com/app/board/uXjVGrmeQUI=/?share_link_id=820200413870

▶️ Caminho do repositório atual - https://github.com/AndreB2808/Engenharia-de-Software/tree/Projeto-GetLab
