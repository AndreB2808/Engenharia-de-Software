class Plataforma:

    def __init__(self, nome, pais):
        self.nome = nome
        self.pais = pais
        self.catalogos = []

    def adicionar_catalogo(self, catalogo):
        self.catalogos.append(catalogo)


class Catalogo:

    def __init__(self, titulo, qtdFilmes):
        self.titulo = titulo
        self.qtdFilmes = qtdFilmes
        self.filmes = []

    def add_filme(self, filme):
        self.filmes.append(filme)
        self.qtdFilmes += 1

    def listar_filmes(self):
        print(f"\n🎬 Catálogo: {self.titulo}")

        for filme in self.filmes:
            print(f"- {filme.titulo} ({filme.genero}) - {filme.duracao} min")


class Filme:

    def __init__(self, titulo, duracao, genero):
        self.titulo = titulo
        self.duracao = duracao
        self.genero = genero


class Avaliacao:

    def __init__(self, nota, comentario):
        self.nota = nota
        self.comentario = comentario
        self.filme = None


class Usuario:

    def __init__(self, nome, email, plano):
        self.nome = nome
        self.email = email
        self.plano = plano
        self.avaliacoes = []

    def avaliar(self, filme, avaliacao):
        avaliacao.filme = filme
        self.avaliacoes.append(avaliacao)

        print(f'\n⭐ {self.nome} avaliou "{filme.titulo}" com nota {avaliacao.nota}')

    def ver_avaliacoes(self):
        print(f"\n📋 Avaliações de {self.nome}:")

        if not self.avaliacoes:
            print("Nenhuma avaliação encontrada.")
            return

        for avaliacao in self.avaliacoes:
            print(
                f"- {avaliacao.filme.titulo}: "
                f"{avaliacao.nota}/10 "
                f"--> {avaliacao.comentario}"
            )


# Testes

netflix = Plataforma("Netplix", "BR")
catalogo = Catalogo("Filmes em Destaque", 0)
filme1 = Filme("Oppenheimer", 180, "Drama")
filme2 = Filme("Barbie", 114, "Comédia")
catalogo.add_filme(filme1)
catalogo.add_filme(filme2)
netflix.adicionar_catalogo(catalogo)
usuario = Usuario("Ana", "ana@email.com", "Premium")
avaliacao = Avaliacao(9.5, "Incrível! Assisti duas vezes")
usuario.avaliar(filme1, avaliacao)
catalogo.listar_filmes()
usuario.ver_avaliacoes()
