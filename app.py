from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = 'chave-secreta-simples'

DATA_FILE = 'data.json'
ADMIN_PASSWORD = 'admin123'

# -------------------------------
# Funções auxiliares
# -------------------------------
def carregar_dados():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# -------------------------------
# Rotas públicas
# -------------------------------
@app.route('/')
def index():
    dados = carregar_dados()
    return render_template('index.html', opcoes=dados)

@app.route('/redirecionar')
def redirecionar():
    escolha = request.args.get('opcao')
    dados = carregar_dados()
    
    if escolha not in dados:
        return redirect('/')

    atendente = dados[escolha]
    mensagem = atendente['mensagem'].replace(' ', '+')
    link = f"https://wa.me/{atendente['whatsapp']}?text={mensagem}"

    return redirect(link)

# -------------------------------
# Login admin
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

# -------------------------------
# Painel Administrativo
# -------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    dados = carregar_dados()

    if request.method == 'POST':
        acao = request.form.get('acao')

        # -----------------------------
        # CADASTRAR ATENDENTE
        # -----------------------------
        if acao == 'adicionar_atendente':
            nome = request.form['nome']
            whatsapp = request.form['whatsapp']

            dados[nome] = {
                'nome': nome,
                'whatsapp': whatsapp,
                'mensagem': f"Olá {nome}, tudo bem?"
            }

            salvar_dados(dados)

        # -----------------------------
        # CADASTRAR SERVIÇO
        # -----------------------------
        elif acao == 'adicionar_servico':
            servico = request.form['pergunta']
            atendente_nome = request.form['nome']
            mensagem = request.form['mensagem']

            if atendente_nome not in dados:
                return "Erro: atendente não existe", 400
            
            dados[servico] = {
                'nome': atendente_nome,
                'whatsapp': dados[atendente_nome]['whatsapp'],
                'mensagem': mensagem
            }

            salvar_dados(dados)

        # -----------------------------
        # EDITAR SERVIÇO
        # -----------------------------
        elif acao == 'editar':
            servico_original = request.form['pergunta_original']
            novo_servico = request.form['nova_pergunta']
            nome = request.form['nome']
            whatsapp = request.form['whatsapp']
            mensagem = request.form['mensagem']

            # Remove chave antiga se renomeou o serviço
            if novo_servico != servico_original:
                dados.pop(servico_original, None)

            dados[novo_servico] = {
                "nome": nome,
                "whatsapp": whatsapp,
                "mensagem": mensagem
            }

            salvar_dados(dados)

        # -----------------------------
        # REMOVER SERVIÇO
        # -----------------------------
        elif acao == 'remover':
            servico = request.form['pergunta']
            dados.pop(servico, None)
            salvar_dados(dados)

        return redirect(url_for('admin'))

    return render_template('admin.html', opcoes=dados)

# -------------------------------
# Iniciar servidor
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
