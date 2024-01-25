from flask import Flask, render_template, request, session, redirect, url_for, send_file

import os

from app import *
from word import *
from pdf import *
from scripts.banco import *
from lerPDF import *
from converter_word_pdf import *

app = Flask(__name__)
app.secret_key = 'key123'

@app.route('/')
def index():
    session['ultima_tela'] = 'home'
    arquivos_armazenados = listarDiretorio()
    return render_template('index.html',arquivos_armazenados=arquivos_armazenados)

@app.route('/navegar', methods=['GET', 'POST'])
def navegar():
    try:
        menu = request.form['menu']
    except:
        menu = session.get('ultima_tela', 'index')
    if menu == 'home':
        return index()
    if menu == 'filtros':
        return filtros()


@app.route('/fechar_notificacao', methods=['GET', 'POST'])
def fechar_notificacao():
    #notificacao = request.form['notificacao']
    session.pop('notificacao', None)
    ultima_tela = session.get('ultima_tela', 'home')
    print(ultima_tela)
    #return render_template('%s.html'% ultima_tela)
    return navegar()


@app.route('/escolher_arquivo', methods=['GET', 'POST'])
def escolher_arquivo():
    arquivo_selecionado = request.form['arquivo_selecionado']
    #print(arquivo_selecionado[:8])
    if arquivo_selecionado[:8]=='excluir-':
        resposta = apagar_arquivo(arquivo_selecionado[8:])
        session['notificacao'] = resposta
        return index()
    tipo = arquivo_selecionado.split('.')
    tipo = tipo[1]
    #print(tipo)
    if tipo=='docx':
        print('Converter')
        resposta = converter('static/arquivos/'+arquivo_selecionado)
        apagar_arquivo(arquivo_selecionado)
        session['notificacao'] = 'Documento %s foi convertido para PDF !'% arquivo_selecionado
        return index()
    grupos = buscar_grupos()
    return render_template('index.html',arquivo_selecionado=arquivo_selecionado, tipo=tipo,grupos=grupos)

@app.route('/encontrar_valores', methods=['GET', 'POST'])
def encontrar_valores():
    comando = request.form['comando']
    if comando=='todos':
        palavras_chave = buscar_nomes_filtros()
    else:
        palavras_chave_id = []
        # Busca todos os grupos personalizados
        grupo_personalizado = consultar_grupo_personalizado()
        # Recebe o ID herdado da tela anterior
        grupo_id = comando
        # Guarda os ID das palavras-chave em uma lista
        for grupo in grupo_personalizado:
            #print('palavra_id:',grupo[0])
            #print('grupo_id:',grupo[1])
            if int(grupo_id)==grupo[1]:
                palavras_chave_id.append(grupo[0])
        # Busca as palavras pelo ID
        dados = buscar_palavras_grupo_personalizado(palavras_chave_id)
        palavras_chave = []
        # Formata a lista das palavras-chave para a consulta. Ex: palavras-chave = ['nome','nome2']
        for dado in dados:
            palavras_chave.append(dado[1])
    # Receber o nome do arquivo selecionado
    arquivo_selecionado = request.form['arquivo_selecionado']
    # Buscar no pdf
    dados = dados_pdf(arquivo_selecionado,palavras_chave)
    for dado in dados:
        print(dado['palavra_chave'])
        print(dado['total'])
        #print('Somente a primeira posicao: ',dado['informacoes'][0][0])
        print('\n')
        # Formato das informações do dicionario
        '''
        dicionario = {  'palavra_chave':'exemplo',
                        'total':'total',
                        'informacoes': 'dicionario={'pagina':pagina,'valor':valor}'
                        }'''
    return render_template('index.html', arquivo_selecionado=arquivo_selecionado, dados_encontrados=dados)
@app.route('/detalhar_valores', methods=['GET', 'POST'])
def detalhar_valores():
    palavras_chave = request.form['palavras_chave']
    arquivo_selecionado = request.form['arquivo_selecionado']
    dados = dados_pdf(arquivo_selecionado,palavras_chave)
    detalhes = dados[1][0]
    informacoes = {
        'quantidade':len(detalhes),
        'total':dados[0],
        'palavra-chave':palavras_chave
    }
    return render_template('index.html', arquivo_selecionado=arquivo_selecionado, detalhes_valores=True, informacoes=informacoes, detalhes=detalhes)

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

@app.route('/visualizar_pdf', methods=['GET', 'POST'])
def visualizar_pdf():
    arquivo_selecionado = request.form['arquivo_selecionado']
    # Caminho para o arquivo PDF no diretório
    caminho_arquivo = 'static/arquivos/'+arquivo_selecionado  # Substitua pelo caminho real do seu arquivo

    # Verificar se o arquivo existe
    if os.path.exists(caminho_arquivo):
        # Enviar o arquivo como resposta
        return send_file(caminho_arquivo, as_attachment=True)
        #return f'<a href="/static/{caminho_arquivo}" target="_blank">Visualizar PDF</a>'
    else:
        return 'Arquivo não encontrado'

''' ------------------------------------------------------------------------------------------ '''
# Filtros 

@app.route('/filtros', methods=['GET', 'POST'])
def filtros():
    session['ultima_tela'] = 'filtros'
    filtros = buscar_filtros()
    grupos = buscar_grupos()
    return render_template('filtros.html', filtros=filtros, grupos=grupos)
@app.route('/adicionar_palavra', methods=['GET', 'POST'])
def adicionar_palavra():
    palavra_chave = request.form['palavra_chave']
    print('Palavra adicionada',palavra_chave)
    resposta = adicionar_palavra_chave(palavra_chave)
    session['notificacao'] = resposta
    return render_template('filtros.html')

@app.route('/adicionar_grupo', methods=['GET', 'POST'])
def adicionar_grupo():
    return render_template('filtros.html', novo_grupo=True)

@app.route('/editar_grupo', methods=['GET', 'POST'])
def editar_grupo():
    grupo_id = request.form['grupo_id']
    grupo = buscar_grupo(grupo_id)
    print(grupo)
    return render_template('filtros.html', editar_grupo=True, grupo=grupo)

@app.route('/preencher_grupo', methods=['GET', 'POST'])
def preencher_grupo():
    acao = request.form['acao']
    dados_grupo = [request.form['nome'], request.form['descricao']]
    print('dados_grupo',dados_grupo)
    if acao=='cancelar':
        return filtros()
    todosfiltros = buscar_filtros()
    if acao=='alterar':
        grupo_id = request.form['grupo_id']
        dados_grupo.append(grupo_id)
        print(dados_grupo)
        return render_template('filtros.html', preencher_grupo=True, alterar=True,filtros=todosfiltros, dados_grupo=dados_grupo)
    else:
        return render_template('filtros.html', preencher_grupo=True,filtros=todosfiltros, dados_grupo=dados_grupo)

@app.route('/salvar_grupo', methods=['POST'])
def salvar_grupo():
    # Recebe os dados nome, descricao e se for uma alteração o id do grupo ['nome','descricao','grupo_id']
    dados_grupo = request.form['dados_grupo']
    dados_grupo = dados_grupo.replace('[','')
    dados_grupo = dados_grupo.replace(']','')
    dados_grupo = dados_grupo.replace("'",'')
    #print('dados_grupo 2 ',dados_grupo)
    dados = dados_grupo.split(',')
    nome = dados[0]
    descricao = dados[1]
    # Cancelar
    acao = request.form['acao']
    if acao=='cancelar':
        return filtros()
    
    lista_checkbox_id = []
    lista_id = []
    # Buscando todos as palavras chaves cadastradas
    todosfiltros = buscar_filtros()
    # Cria uma lista concatenando o nome '02-11'+ ID de todos os filtros
    for id in todosfiltros:
        lista_checkbox_id.append('02-11-%s'%id[0])
    # Verifica se existe checkbox marcado com os IDs dos filtros
    for checkbox_name in lista_checkbox_id:
        try:
            id_check = request.form[checkbox_name]
            lista_id.append(id_check)
        except:
            pass
    if acao=='salvar':
        salvar_preenchimento_grupo(nome, descricao, lista_id)
    if acao=='alterar':
        grupo_id = dados[2]
        resposta = salvar_alteracao_grupo(grupo_id, nome, descricao)
        # Armazena as palavras que serão adicionadas ao grupo
        novas_palavras_chave = lista_id
        # Separando as palavras que serão excluidas do grupo
        antigas_palavras_chave = []
        grupo_personalizado = consultar_grupo_personalizado()
        for grupo in grupo_personalizado:
            if grupo[1]==int(grupo_id):
                antigas_palavras_chave.append(grupo[0])
        print(antigas_palavras_chave)
        # Apagar entidade fraca antiga
        for palavra_chave_id in antigas_palavras_chave:
            print('apagar palavra_chave_id',palavra_chave_id)
            apagar_grupo_personalizado(palavra_chave_id, grupo_id)
        # salvar na entidade fraca as alterações
        if resposta!='erro':
            alterar_grupo_personalizado(lista_id, grupo_id)

    return render_template('filtros.html')

def salvar_preenchimento_grupo(nome, descricao, lista_palavras):
    # Chama a função para salvar o grupo e ela retorna o id do grupo salvo
    grupo_id = salvar_novo_grupo(nome, descricao)
    if grupo_id=='erro':
        session['notificacao'] = 'Erro ao registrar grupo'
        return render_template('filtros.html')
    # Chama a função para preencher a entidade que relaciona o grupo às palavras-chave
    resposta = salvar_grupo_personalizado(lista_palavras, grupo_id)
    session['notificacao'] = resposta
    return render_template('filtros.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    #app.run('192.168.20.125', port=5001)
