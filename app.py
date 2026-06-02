from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo_super_seguro"  # Chave para criptografar as sessões

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabelas se não existirem
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            data TEXT NOT NULL,
            pessoas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        senha = request.form["senha"].strip()

        if usuario == "" or senha == "":
            flash("Preencha os campos corretamente!")
            return redirect(url_for("cadastro"))

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            conn.commit()
            flash("Cadastro realizado com sucesso!")
        except sqlite3.IntegrityError:
            flash("Usuário já existe!")
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        senha = request.form["senha"].strip()

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha)).fetchone()
        conn.close()

        if user:
            # --- SISTEMA DE FUNÇÕES (USER / ADMIN) ---
            session["logado"] = True
            session["usuario_nome"] = user["usuario"]
            
            # Se o nome do usuário for 'admin', ele ganha o cargo de admin
            if user["usuario"].lower() == "admin":
                session["cargo"] = "admin"
                flash("Bem-vindo ao painel administrativo!")
            else:
                session["cargo"] = "usuario"
                flash("Login realizado com sucesso!")
                
            return redirect(url_for("restaurante"))
        else:
            flash("Usuário ou senha incorretos!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/restaurante")
def restaurante():
    # Segurança: Se não estiver logado, volta para o login
    if not session.get("logado"):
        flash("Por favor, faça login para acessar o cardápio.")
        return redirect(url_for("login"))
        
    # Passamos o cargo do usuário para o HTML saber se mostra ou não o botão de reservas
    return render_template("restaurante.html", cargo=session.get("cargo"))


@app.route("/fazer-reserva", methods=["POST"])
def fazer_reserva():
    if not session.get("logado"):
        return redirect(url_for("login"))

    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    data = request.form.get("data")
    pessoas = request.form.get("pessoas")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO reservas (nome, telefone, data, pessoas) VALUES (?, ?, ?, ?)",
        (nome, telefone, data, pessoas)
    )
    conn.commit()
    conn.close()

    return "<script>alert('Reserva solicitada com sucesso!'); window.location.href='/restaurante';</script>"


# --- ROTA PROTEGIDA: SÓ O ADMIN ACESSA ---
@app.route("/reservas")
def ver_reservas():
    # Bloqueio de segurança: Se não for admin, barra o acesso imediatamente
    if not session.get("logado") or session.get("cargo") != "admin":
        return "<h1>Acesso Negado!</h1><p>Apenas administradores podem ver as reservas feitas.</p><a href='/restaurante'>Voltar</a>", 403

    conn = get_db_connection()
    lista_reservas = conn.execute("SELECT * FROM reservas ORDER BY data DESC").fetchall()
    conn.close()
    
    return render_template("reservas.html", reservas=lista_reservas)


# Rota de Logout (Sair)
@app.route("/logout")
def logout():
    session.clear() # Limpa todos os dados salvos na sessão
    flash("Você saiu da sua conta.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)