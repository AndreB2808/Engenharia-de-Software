# ============================================================
# 🚀 SRS em Python — Rode no Google Colab!
# Aula 04 — Engenharia de Software · FIAP
# ============================================================
from dataclasses import dataclass, field
from typing import List
from enum import Enum

class Prioridade(Enum):
    ALTA = "Alta"
    MEDIA = "Média"
    BAIXA = "Baixa"

@dataclass
class RequisitoFuncional:
    id: str
    nome: str
    descricao: str
    prioridade: Prioridade
    ator: str
    pre_condicao: str
    pos_condicao: str

@dataclass
class RequisitoNaoFuncional:
    id: str
    categoria: str  # Desempenho, Segurança, Usabilidade...
    descricao: str
    criterio_aceitacao: str
@dataclass
class SRS:
    projeto: str
    versao: str
    descricao: str
    resultads : str
    requisitos_funcionais: List[RequisitoFuncional] = field(default_factory=list)
    requisitos_nao_funcionais: List[RequisitoNaoFuncional] = field(default_factory=list)

    def adicionar_rf(self, req: RequisitoFuncional):
        self.requisitos_funcionais.append(req)
        print(f"✅ RF '{req.id}' adicionado!")

    def adicionar_rnf(self, req: RequisitoNaoFuncional):
        self.requisitos_nao_funcionais.append(req)
        print(f"✅ RNF '{req.id}' adicionado!")

    def relatorio(self):
        print(f"\n{'='*50}")
        print(f"📋 SRS — {self.projeto} v{self.versao}")
        print(f"{'='*50}")
        print(f"📝 {self.descricao}\n")

        print(f"🔧 REQUISITOS FUNCIONAIS ({len(self.requisitos_funcionais)})")
        for rf in self.requisitos_funcionais:
            print(f"  [{rf.id}] {rf.nome} — Prioridade: {rf.prioridade.value}")
            print(f"       Ator: {rf.ator}")
            print(f"       📌 {rf.descricao}\n")

        print(f"⚡ REQUISITOS NÃO-FUNCIONAIS ({len(self.requisitos_nao_funcionais)})")
        for rnf in self.requisitos_nao_funcionais:
            print(f"  [{rnf.id}] {rnf.categoria}")
            print(f"       📌 {rnf.descricao}")
            print(f"       ✔️  Critério: {rnf.criterio_aceitacao}\n")
    
   # def validar_requisito(rf: RequisitoFuncional) -> dict:
    
   # resultados = {}
    
    # Dica 1: len(rf.descricao) > 20
    # Dica 2: rf.pre_condicao != ""
    # Dica 3: any(char.isdigit() for char in rf.descricao)
    
   # return resultados

# ---- Criando o SRS do App de Delivery ----
srs = SRS(
    projeto="App de Delivery — Módulo Rastreamento",
    versao="1.0",
    descricao="Sistema de rastreamento em tempo real de entregadores"
)

srs.adicionar_rf(RequisitoFuncional(
    id="RF-001",
    nome="Rastreamento em Tempo Real",
    descricao="Exibir posição do entregador no mapa atualizada a cada 3 segundos",
    prioridade=Prioridade.ALTA,
    ator="Cliente",
    pre_condicao="Pedido com status 'Em rota'",
    pos_condicao="Cliente visualiza localização atual do entregador"
))

srs.adicionar_rf(RequisitoFuncional(
    id="RF-002",
    nome="Notificação de Status",
    descricao="Enviar push notification ao cliente quando status do pedido mudar",
    prioridade=Prioridade.ALTA,
    ator="Sistema",
    pre_condicao="Cliente com notificações habilitadas",
    pos_condicao="Cliente notificado sobre mudança de status"
))

srs.adicionar_rf(RequisitoFuncional(
    id="RF-003",
    nome="Avaliação do Pedido",
    descricao="Atualizar avaliação da loja com base na avaliação do cliente sobre o pedido e entrega",
    prioridade=Prioridade.MEDIA,
    ator="Cliente",
    pre_condicao="Último pedido concluído recentemente",
    pos_condicao="Cliente realiza avaliação e altera a pontuação da loja e entregador"
))

srs.adicionar_rf(RequisitoFuncional(
    id="RF-004",
    nome="Atualização do Pedido",
    descricao="Atualizar o status do pedido para o sistema",
    prioridade=Prioridade.ALTA,
    ator="Restaurante",
    pre_condicao="Restaurante seleciona opção de atualizar status do pedido",
    pos_condicao="Sistema atualizado com o status atual do pedido"
))

srs.adicionar_rf(RequisitoFuncional(
    id="RF-005",
    nome="Recomendação de restaurantes",
    descricao="Recomendar restaurantes para o cliente com base nos últimos pedidos",
    prioridade=Prioridade.BAIXA,
    ator="Sistema",
    pre_condicao="Cliente acessa a página inicial da aplicação",
    pos_condicao="Sistema mostra restaurantes com gostos similares aos últimos pedidos realizados"
))

srs.adicionar_rnf(RequisitoNaoFuncional(
    id="RNF-001",
    categoria="Desempenho",
    descricao="O sistema deve suportar 50.000 usuários simultâneos.",
    criterio_aceitacao="Teste de carga com JMeter: 50k req/s com latência < 500ms"
))

srs.adicionar_rnf(RequisitoNaoFuncional(
    id="RNF-002",
    categoria="Segurança",
    descricao="Dados de localização devem ser criptografados em trânsito.",
    criterio_aceitacao="Uso de TLS 1.3 validado por ferramenta de auditoria"
))

srs.adicionar_rnf(RequisitoNaoFuncional(
    id="RNF-003",
    categoria="Interface",
    descricao="A interface deve ser intuitiva com o usuário podendo realizar facilmente um pedido.",
    criterio_aceitacao="Um pedido deve poder ser realizado em menos de 30 segundos"
))

srs.adicionar_rnf(RequisitoNaoFuncional(
    id="RNF-004",
    categoria="Otimização",
    descricao="A aplicação deve ter um tempo de resposta curto independente do dispositivo sendo utilizado.",
    criterio_aceitacao="A interface deve responder ao cliente em no máximo 5 segundos"
))

srs.relatorio()

