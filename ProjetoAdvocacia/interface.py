from flask import Flask, render_template, request, session, redirect, url_for

import os
from app import *
from word import *

app = Flask(__name__)
app.secret_key = 'key123'

@app.route('/')
def index():
    arquivos_armazenados = listarDiretorio()
    return render_template('index.html',arquivos_armazenados=arquivos_armazenados)

@app.route('/navegar', methods=['GET', 'POST'])
def navegar():
    menu = request.form['menu']
    if menu == 'home':
        return index()

@app.route('/fechar_notificacao', methods=['GET', 'POST'])
def fechar_notificacao():
    #notificacao = request.form['notificacao']
    session.pop('notificacao', None)
    return index()

@app.route('/buscar_valores', methods=['GET', 'POST'])
def buscar_valores():
    arquivo_selecionado = request.form['arquivo_selecionado']
    #print(arquivo_selecionado[:8])
    if arquivo_selecionado[:8]=='excluir-':
        resposta = apagar_arquivo(arquivo_selecionado[8:])
        session['notificacao'] = resposta
        return index()
    tipo = arquivo_selecionado.split('.')
    tipo = tipo[1]
    #print(tipo)
    return render_template('index.html',arquivo_selecionado=arquivo_selecionado, tipo=tipo)

@app.route('/encontrar_valores', methods=['GET', 'POST'])
def encontrar_valores():
    palavra_chave = request.form['palavra_chave']
    arquivo_selecionado = request.form['arquivo_selecionado']
    tipo = arquivo_selecionado.split('.')
    tipo = tipo[1]
    #print(tipo)
    if tipo=='pdf':
        # Buscar no pdf
        total_real = execucao(palavra_chave,arquivo_selecionado)
    elif tipo=='docx':
        caminho_arquivo_word = 'static/arquivos/'+arquivo_selecionado
        palavra_chave = [palavra_chave]
        dados = encontrar_e_armazenar_linhas(caminho_arquivo_word, palavra_chave)
        print(dados[1])
        valores = converter_valores_reais(dados[1])
        total = somar_valores(valores)
        total_real = formatar_valor_real(total)
    return render_template('index.html', total=total_real, palavra_chave=palavra_chave[0], arquivo_selecionado=arquivo_selecionado)

UPLOAD_FOLDER_SLOT = 'static/arquivos'
app.config['UPLOAD_FOLDER_SLOT'] = UPLOAD_FOLDER_SLOT
#app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/uploadDrop', methods=['GET', 'POST'])
def uploadDrop():
    # Verifica se o arquivo está presente no request
    if 'file' not in request.files:
        return render_template('index.html')
    file = request.files['file']
    if request.method == 'POST':
        if 'file' in request.files:
            arquivo = request.files['file']
            if arquivo.filename != '':
                print("Entrou aqui",arquivo.filename)
                # Um arquivo foi selecionado no campo de entrada 'arquivo'
                # Salva o arquivo no diretório de upload
                file.save(os.path.join(app.config['UPLOAD_FOLDER_SLOT'], file.filename))
                session['arquivo_selecionado'] = arquivo.filename
                return render_template('index.html', arquivo_selecionado=arquivo.filename)
    # Verifica se o arquivo possui um nome
    if file.filename == '':
        return index()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
