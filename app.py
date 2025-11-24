from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = 'chave-secreta-simples'  # mude se quiser mais segurança

DATA_FILE = 'data.json'
ADMIN_PASSWORD = 'admin123'

# -------------------------------
# Funções auxiliares
# -------------------------------
def carregar_dados():
    """Carrega as opções do arquivo JSON."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
    """Salva as opções no arquivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# -------------------------------
# Rotas públicas
# -------------------------------
@app.route('/')
def index():
    opcoes = carregar_dados()
    return render_template('index.html', opcoes=opcoes)

@app.route('/redirecionar')
def redirecionar():
    escolha = request.args.get('opcao')
    opcoes = carregar_dados()
    
    if escolha not in opcoes:
        return redirect('/')
    
    atendente = opcoes[escolha]
    mensagem = atendente['mensagem'].replace(' ', '+')
    link = f"https://wa.me/{atendente['whatsapp']}?text={mensagem}"
    return redirect(link)

# -------------------------------
# Área admin
# -------------------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', erro='Senha incorreta')
    return render_template('login.html')

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    opcoes = carregar_dados()

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'adicionar':
            pergunta = request.form['pergunta']
            nome = request.form['nome']
            whatsapp = request.form['whatsapp']
            mensagem = request.form['mensagem']

            opcoes[pergunta] = {
                'nome': nome,
                'whatsapp': whatsapp,
                'mensagem': mensagem
            }
            salvar_dados(opcoes)

        elif acao == 'remover':
            pergunta = request.form['pergunta']
            opcoes.pop(pergunta, None)
            salvar_dados(opcoes)

        return redirect(url_for('admin'))

    return render_template('admin.html', opcoes=opcoes)

if __name__ == "__main__":
    app.run(debug=True)

