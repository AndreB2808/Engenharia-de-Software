class Livro:

    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponivel = True

    def __repr__(self):
        status = "✅" if self.disponivel else "❌"
        return f"{status} {self.titulo} — {self.autor}"


class Biblioteca:

    def __init__(self):
        self.catalogo = []
        self.emprestimos = []

    def cadastrar_livro(self, titulo, autor):
        self.catalogo.append(Livro(titulo, autor))

    def listar_catalogo(self):
        print("\n📚 Catálogo disponível:")
        for livro in self.catalogo:
            print(f"  {livro}")

    def buscar_livro(self, termo):
        print(f"\n🔍 Buscando livro: '{termo}'")
        encontrado = False

        for livro in self.catalogo:
            if termo.lower() in livro.titulo.lower():
                print(f"  {livro}")
                encontrado = True

        if not encontrado:
            print("  ❌ Nenhum livro encontrado.")

    def emprestar_livro(self, titulo, leitor):
        print("\n📌 Empréstimo:")

        livro_encontrado = None

        for livro in self.catalogo:
            if livro.titulo == titulo:
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            print("❌ Livro não encontrado no catálogo.")
            return

        if not livro_encontrado.disponivel:
            print(f"⚠️ '{titulo}' já está emprestado!")
            return

        livro_encontrado.disponivel = False
        self.emprestimos.append({
            "leitor": leitor,
            "livro": livro_encontrado
        })

        print(f"✅ '{titulo}' emprestado para {leitor}!")

    def devolver_livro(self, titulo, leitor):
        print("\n🔄 Devolução:")

        registro = None

        for emp in self.emprestimos:
            if emp["leitor"] == leitor and emp["livro"].titulo == titulo:
                registro = emp
                break

        if registro is None:
            print("❌ Nenhum empréstimo encontrado para este leitor e livro.")
            return

        registro["livro"].disponivel = True
        self.emprestimos.remove(registro)

        print(f"✅ '{titulo}' devolvido por {leitor}!")

        atraso = input("Houve atraso na devolução? (s/n): ").lower()
        if atraso == "s":
            print("\n📋 Multa aplicada!")

    def listar_emprestimos(self):
        print("\n📋 Empréstimos ativos:")

        if not self.emprestimos:
            print("  Nenhum empréstimo ativo.")
            return

        for emp in self.emprestimos:
            print(f"  📖 {emp['livro'].titulo} — {emp['leitor']}")


# 🧪 TESTES

bib = Biblioteca()

bib.cadastrar_livro("Clean Code", "Robert C. Martin")
bib.cadastrar_livro("The Pragmatic Programmer", "Hunt & Thomas")
bib.cadastrar_livro("Design Patterns", "Gang of Four")

bib.listar_catalogo()

bib.buscar_livro("clean")

bib.emprestar_livro("Clean Code", "Ana Silva")
bib.emprestar_livro("Design Patterns", "Ana Silva")

bib.devolver_livro("Clean Code", "Ana Silva")

bib.listar_catalogo()
bib.listar_emprestimos()
bib.devolver_livro("Design Patterns", "Ana Silva")
bib.listar_emprestimos()