# ============================================================
# 🏛️ SISTEMA DE BIBLIOTECA DIGITAL — Biblioteca FIAP
# ============================================================

# ----------------------------
# 📦 DADOS DO SISTEMA
# ----------------------------
catalogo = [
    {"titulo": "Clean Code", "autor": "Robert C. Martin", "disponivel": True},
    {"titulo": "The Pragmatic Programmer", "autor": "Hunt & Thomas", "disponivel": True},
    {"titulo": "Design Patterns", "autor": "Gang of Four", "disponivel": True},
]

emprestimos = []

# ============================================================
# UC-01: LISTAR CATÁLOGO
# ============================================================

print("📚 Catálogo disponível:")
for livro in catalogo:
    status = "✅" if livro["disponivel"] else "❌"
    print(f"  {status} {livro['titulo']} — {livro['autor']}")

# ============================================================
# UC-02: BUSCAR LIVRO
# ============================================================

print("\n🔍 Buscando livro...")

busca = "clean"

for livro in catalogo:
    if busca.lower() in livro["titulo"].lower():
        status = "✅" if livro["disponivel"] else "❌"
        print(f"  {status} {livro['titulo']} — {livro['autor']}")

# ============================================================
# UC-03: EMPRESTAR LIVRO
# ============================================================

print("\n📌 Empréstimo:")

leitor = "Ana Silva"
titulo = "Clean Code"

livro_encontrado = None

for livro in catalogo:
    if livro["titulo"] == titulo:
        livro_encontrado = livro
        break

if livro_encontrado is None:
    print("❌ Livro não encontrado no catálogo.")

elif livro_encontrado["disponivel"] == False:
    print(f"⚠️ '{titulo}' já está emprestado!")

else:
    livro_encontrado["disponivel"] = False
    emprestimos.append({"leitor": leitor, "livro": titulo})
    print(f"✅ '{titulo}' emprestado para {leitor}!")

# ============================================================
# UC-04: DEVOLVER LIVRO
# ============================================================

print("\n🔄 Devolução:")

leitor_devolvendo = "Ana Silva"
titulo_devolvendo = "Clean Code"

registro = None

for emp in emprestimos:
    if emp["leitor"] == leitor_devolvendo and emp["livro"] == titulo_devolvendo:
        registro = emp
        break

if registro is None:
    print("❌ Nenhum empréstimo encontrado para este leitor e livro.")

else:
    for livro in catalogo:
        if livro["titulo"] == titulo_devolvendo:
            livro["disponivel"] = True
            break

    emprestimos.remove(registro)
    print(f"✅ '{titulo_devolvendo}' devolvido por {leitor_devolvendo}!")

    atraso = input("Houve atraso na devolução? (s/n): ").lower()
    if atraso == "s":
        print("📋 Multa aplicada!")

# ============================================================
# 🔎 ESTADO FINAL
# ============================================================

print("\n📖 Catálogo após operações:")
for livro in catalogo:
    status = "✅" if livro["disponivel"] else "❌"
    print(f"  {status} {livro['titulo']}")

print(f"\n📋 Empréstimos ativos: {emprestimos}")

# ============================================================
# 🚀 DESAFIO EXTRA — versão OOP
# ============================================================

class Livro:

    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponivel = True

    def __repr__(self):
        status = "✅" if self.disponivel else "❌"
        return f"[{status}] {self.titulo} — {self.autor}"


class Biblioteca:

    def __init__(self):
        self.catalogo = []
        self.emprestimos = {}

    def cadastrar(self, titulo, autor):
        self.catalogo.append(Livro(titulo, autor))
        print(f"📚 '{titulo}' cadastrado!")

    def listar(self):
        print("\n📖 Catálogo:")
        for livro in self.catalogo:
            print(f"  {livro}")

    def emprestar(self, titulo, leitor):

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

        if leitor not in self.emprestimos:
            self.emprestimos[leitor] = []

        self.emprestimos[leitor].append(livro_encontrado)

        print(f"✅ '{titulo}' emprestado para {leitor}!")

    def devolver(self, titulo, leitor):

        if leitor not in self.emprestimos:
            print("❌ Este leitor não possui empréstimos.")
            return

        livro_encontrado = None

        for livro in self.emprestimos[leitor]:
            if livro.titulo == titulo:
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            print("❌ Este livro não está registrado para este leitor.")
            return

        livro_encontrado.disponivel = True
        self.emprestimos[leitor].remove(livro_encontrado)

        if len(self.emprestimos[leitor]) == 0:
            del self.emprestimos[leitor]

        print(f"✅ '{titulo}' devolvido por {leitor}!")

        atraso = input("Houve atraso na devolução? (s/n): ").lower()
        if atraso == "s":
            print("📋 Multa aplicada!")


# ============================================================
# TESTE DA VERSÃO OOP
# ============================================================

bib = Biblioteca()

bib.cadastrar("Clean Code", "Robert C. Martin")
bib.cadastrar("Design Patterns", "Gang of Four")

bib.listar()

bib.emprestar("Clean Code", "Ana Silva")

bib.listar()

bib.devolver("Clean Code", "Ana Silva")

bib.listar()