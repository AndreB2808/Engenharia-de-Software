# Projeto Servatio 🪙
<p align="center">
  <strong>Do latim "Preservação" / "Guardando"</strong>
</p>

<p align="center">
  <img src="media/piglogo.png" width="250">
</p>
​

## ⚙️ Descrição do Problema
Atualmente, muitos jovens que começam a possuir uma renda própria têm dificuldade para organizar seus gastos, estabelecer metas financeiras e separar dinheiro de forma consciente para construir uma reserva ou começar a investir pensando no futuro. A falta de uma visão clara sobre quanto recebem, quanto gastam e quanto podem guardar causa dificuldade no planejamento financeiro e na criação de hábitos de longo prazo. Com isso, surge a proposta do projeto Servatio.

## 💡 Proposta
O serviço Servatio seria uma aplicação voltada para o gerenciamento financeiro de jovens e adultos, permitindo o controle e visualização de receitas e despesas, a criação de metas financeiras e a separação de valores destinados a essas metas. Além disso, o sistema permitirá o acompanhamento de valores destinados a investimentos e disponibilizará diferentes opções de investimento, possibilitando que o usuário acompanhe sua evolução financeira em um único ambiente. O serviço também poderá ser conectado a outros serviços de finalidade monetária escolhidos pelo usuário, permitindo o monitoramento de suas movimentações financeiras sem que seja obrigatória a transferência de fundos diretamente para o Servatio.

## 🖥️ Tecnologias Utilizadas
Para o funcionamento do serviço Servatio, foram implementadas em uma aplicação protótipa realizada no Figma as funcionalidades de gerenciamento de informações financeiras dos usuários, além de dados mockados para fim de simular a interface do aplicativo, com saldo total, barras de progresso de metas e indicadores de investimentos, representando a utilização de um usuário real. Para acessar o protótipo basta chegar ao fim deste documento e acessar o link disponível em "Documentos". Já o ambiente de testes utiliza o Streamlit para a interface visual, além de arquivos JSON para a simulação de cadastro e login de usuário (por meio do arquivo "usuarios.json"), e também para armazenamento de metas financeiras criadas pelo usuário (por meio do arquivo "financeiro.json"), sendo possível criar metas com base nas preferências escolhidas pelo usuário (como data limite, quantidade desjada, etc). Uma meta é considerada concluída quando o valor reservado alcança o objetivo. Ela é considerada fracassada somente quando a data limite já passou e o objetivo ainda não foi atingido.

## 🗂️ Estrutura do Projeto

```
    Engenharia-De-Software/tree/Projeto-Servatio/
    ├── .streamlit/
    │   └── config.toml
    ├── src/
    │   ├── assets/
    │   │   └── logo.png
    │   ├── auth/
    │   │   ├── cadastro.py
    │   │   └── login.py
    │   ├── data/
    │   │   ├── usuarios.json
    │   │   └── financeiro.json
    │   ├── models/
    │   │   └── financeiro_model.py
    │   ├── views/
    │   │   └── interface_view.py
    │   └── main.py
    ├── README.md
    └── requirements.txt
```

## 🔌 Como Executar
### Pré-requisitos
    - Python 3
    - Steamlit (caso esteja no Linux é necessário instalar dentro de uma venv) 
Primeiramente é necessário baixar todos os arquivos do projeto. Após a instalação, e dentro de um programa como Visual Studio Code, abra a pasta principal que contêm todos os arquivos. Depois, abra um terminal novo e digite "pip install -r requirements.txt" para instalar as dependências requisitadas (neste caso sendo apenas o "Streamlit"), e então execute o projeto utilizando o comando "streamlit run src/app.py", que abrirá uma guia no navegador da aplicação, sendo possível cadastrar um usuário, fazer login e utilizar as funcionalidades do sistema diretamente pela interface visual.

## 🪢 Funcionalidades Implementadas

- ✔ Cadastro e login de usuário.
- ✔ Patrimônio total simulado para testes.
- ✔ Exibição dos fundos ainda não associados a metas.
- ✔ Criação de metas com nome, valor, data limite e observação opcional.
- ✔ Reserva de parte do patrimônio para uma meta específica.
- ✔ Progresso individual de cada meta.
- ✔ Identificação automática de metas em andamento, concluídas ou fracassadas.
- ✔ Exclusão de metas, devolvendo seus fundos reservados para os fundos não-alocados.
- ✔ Navegação visual de protótipo com as futuras 
- ✕ Áreas de "Investimentos" e "Serviços conectados"
- ✕ Armazenamento em banco de dados real
- ✕ Visualização de fundos reais
- ✕ Criptografia dos dados cadastrados

## 📹 Mídia
### Vídeo pitch de apresentação
https://github.com/user-attachments/assets/1cf880c7-55fd-47ec-81b5-1ed5537d8cd5

### Navegação do protótipo no Figma + ambiente de teste

## 📑 Documentos
🆔 Protótipo no Figma - https://object-pitch-57581393.figma.site/

✴️ Quadro do Miro - https://miro.com/app/board/uXjVHylqrhk=/?share_link_id=625445522410

▶️ Quadro do Trello (Atualizado) - [https://trello.com/b/MxOp62gb/projeto-servatio-%F0%9F%AA%99](https://trello.com/invite/b/6a7bb5edfeea193e42ea61ec/ATTI5263728a668e956e6c7260d4b3060ab73E54EA04/projeto-servatio-🪙) 
