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
def home():
    session['ultima_tela'] = 'home'
    return render_template('home.html')

@app.route('/index')
def index():
    session['ultima_tela'] = 'index'
    arquivos_armazenados = listarDiretorio()
    return render_template('index.html',arquivos_armazenados=arquivos_armazenados)

@app.route('/navegar', methods=['GET', 'POST'])
def navegar():
    try:
        menu = request.form['menu']
    except:
        menu = session.get('ultima_tela', 'index')
    if menu == 'home':
        return home()
    if menu == 'index':
        return index()
    if menu == 'filtros':
        return filtros()
    if menu == 'login':
        return login()


@app.route('/fechar_notificacao', methods=['GET', 'POST'])
def fechar_notificacao():
    #notificacao = request.form['notificacao']
    session.pop('notificacao', None)
    ultima_tela = session.get('ultima_tela', 'home')
    print(ultima_tela)
    #return render_template('%s.html'% ultima_tela)
    return navegar()

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        print('Login')
        print(username,password)
        return index()
    except:
        return render_template('home.html',login=True)

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
    if tipo!='pdf':
        apagar_arquivo(arquivo_selecionado)
        session['notificacao'] = 'Tipo de arquivo inválido. Selecione arquivos com extensão .pdf ou .docx'
        return render_template('index.html')
    grupos = buscar_grupos()
    return render_template('index.html',arquivo_selecionado=arquivo_selecionado, tipo=tipo,grupos=grupos)


@app.route('/parametro_filtros', methods=['GET', 'POST'])
def parametro_filtros():
    arquivo_selecionado = request.form['arquivo_selecionado']
    filtros_encontrados = request.form['filtros_encontrados']
    
    lista = formatar_string_lista(filtros_encontrados)

    palavras_selecionadas = []
    # Verifica se existe checkbox marcado com os nomes dos filtros
    for checkbox_name in lista:
        try:
            filtro_check = request.form[checkbox_name]
            palavras_selecionadas.append(filtro_check)
        except:
            pass
    parametro = buscar_titulo(arquivo_selecionado, palavras_selecionadas)
    palavras_chave = buscar_nomes_filtros()
    dados = dados_pdf(arquivo_selecionado,palavras_chave, parametro)
    # Formata os dados em um dicionario
    dados_encontrados = dicionario_orgao_palavra(dados)
    return render_template('index.html', arquivo_selecionado=arquivo_selecionado, dados_encontrados=dados_encontrados)

@app.route('/encontrar_valores', methods=['GET', 'POST'])
def encontrar_valores():
    # Receber o nome do arquivo selecionado
    arquivo_selecionado = request.form['arquivo_selecionado']

    comando = request.form['comando']

    if comando=='todos':
        palavras_chave = buscar_nomes_filtros()
    elif comando=='encontrar':
        filtros_encontrados = buscar_valores_repetidos(arquivo_selecionado)
        return render_template('index.html', orgaos_encontrados_automatico=True, filtros_encontrados=filtros_encontrados, arquivo_selecionado=arquivo_selecionado)
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

    # Buscar no pdf
    dados = dados_pdf(arquivo_selecionado,palavras_chave,'parametros')
    if dados==[]:
        session['notificacao'] = 'Não encontramos nenhuma referência com os filtros selecionados!'
        return render_template('index.html', arquivo_selecionado=arquivo_selecionado)
    if dados[-1]==[]:
        print('Ultima posicao vazia, removendo')
        dados.pop(-1)
    palavras_chave_listadas = []
    orgaos_listados = []
    dados_encontrados = []
    for palavra in dados:
        #palavra = [{'pagina': 1, 'valor': '30.000,00', 'orgao': 'CHEFIA DE GABINETE', 'palavra_chave': 'Material de Consumo'}]
        for dado in palavra:
            if dado['orgao'] not in orgaos_listados and dado['palavra_chave'] not in palavras_chave_listadas:
                #print(dado['orgao']+' E '+dado['palavra_chave']+' E '+dado['valor'])
                orgao_palavra = {'orgao':dado['orgao'],
                                     'palavra_chave':dado['palavra_chave'],
                                     }
                
                dados_encontrados.append(orgao_palavra)
                # Adiciona os às listadas para que não se repitam 
                palavras_chave_listadas.append(dado['palavra_chave'])
                orgaos_listados.append(dado['orgao'])
                # Zera a lista para inciar uma nova busca em outro orgao
            palavras_chave_listadas = []
        orgaos_listados = []

    return render_template('index.html', arquivo_selecionado=arquivo_selecionado, dados_encontrados=dados_encontrados)
@app.route('/detalhar_valores', methods=['GET', 'POST'])
def detalhar_valores():
    # Recebe o orgao e a palavra chave no formato str(orgao-palavra)
    palavras_chave = request.form['palavras_chave']
    # Separamos os valores
    palavras_chave = palavras_chave.split('-')
    orgao = palavras_chave[0]
    palavras_chave = palavras_chave[1]
    arquivo_selecionado = request.form['arquivo_selecionado']
    # Buscando todos os dados
    dados = dados_pdf(arquivo_selecionado,palavras_chave,'Valor Orçado')
    print('retorno \n\n',dados)
    #dados.pop(-1)
    total = 0
    valores = []
    dados_detalhados = []
    # Encontrando os valores
    for palavra in dados:
        for dado in palavra:
            if dado['orgao']==orgao and dado['palavra_chave']==palavras_chave:
                valores.append(dado['valor'])
                detalhes = {'pagina': dado['pagina'],
                            'valor': dado['valor'],
                            'orgao': dado['orgao'],
                            'palavra_chave': dado['palavra_chave']
                            }
                dados_detalhados.append(detalhes)
    
    valores_float = converter_valores(valores)
    for valor in valores_float:
        total = float(valor) + total
    total = formatar_valor_real(total)

    informacoes = {
        'quantidade':len(valores),
        'total':total
    }

    return render_template('index.html', arquivo_selecionado=arquivo_selecionado, detalhes_valores=True, informacoes=informacoes, dados_encontrados=dados_detalhados)

UPLOAD_FOLDER_SLOT = 'static/arquivos'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc'}
app.config['UPLOAD_FOLDER_SLOT'] = UPLOAD_FOLDER_SLOT




@app.route('/uploadDrop', methods=['GET', 'POST'])
def uploadDrop():
    # Verifica se o arquivo está presente no request
    if 'file' not in request.files:
        return render_template('index.html')
    file = request.files['file']
    if file.filename == '':
        session['notificacao'] = 'Nenhum arquivo foi selecionado'
        return index()
    nome_arquivo = file.filename[-5:]
    tipo = nome_arquivo.split('.')
    tipo_arquivo = tipo[1]
    extensoes_validas = ['pdf','docx','doc']
    if tipo_arquivo not in extensoes_validas:
        session['notificacao'] = 'Tipo de arquivo inválido. Selecione arquivos com extensão .pdf ou .docx'
        return index()
    if request.method == 'POST':
        if 'file' in request.files:
            arquivo = request.files['file']
            if arquivo.filename != '':
                # Um arquivo foi selecionado no campo de entrada 'arquivo'
                # Salva o arquivo no diretório de upload
                file.save(os.path.join(app.config['UPLOAD_FOLDER_SLOT'], file.filename))
                session['arquivo_selecionado'] = arquivo.filename
                grupos = buscar_grupos()
                return render_template('index.html', arquivo_selecionado=arquivo.filename, grupos = grupos)
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

@app.route('/editar_palavra', methods=['GET', 'POST'])
def editar_palavra():
    palavra_id = request.form['palavra_id']
    palavra_id = palavra_id.split('-')
    dados = [palavra_id[0],palavra_id[1]]

    return render_template('filtros.html',editar_palavra_chave=True, palavra_chave=dados)

@app.route('/salvar_alteracao_palavra_chave', methods=['GET', 'POST'])
def salvar_alteracao_palavra_chave():
    acao = request.form['acao']
    palavra_id = request.form['palavra_id']
    palavra_chave = request.form['palavra_chave']
    if acao=='cancelar':
        return filtros()
    resposta = salvar_alteracao_palavra(palavra_id, palavra_chave)
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
    print('Antes:',dados_grupo)
    dados = formatar_string_lista(dados_grupo)
    """
    dados_grupo = dados_grupo.replace('[','')
    dados_grupo = dados_grupo.replace(']','')
    dados_grupo = dados_grupo.replace(" '",'')
    dados_grupo = dados_grupo.replace("'",'')
    dados = dados_grupo.split(',')
    """
    print('Depois:',dados)
    nome = dados[0]
    descricao = dados[1]
    print('descricao,',dados)
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
        print('antigas: ',antigas_palavras_chave)
        # Apagar entidade fraca antiga
        for palavra_chave_id in antigas_palavras_chave:
            print('apagar palavra_chave_id',palavra_chave_id)
            apagar_grupo_personalizado(palavra_chave_id, grupo_id)
        # salvar na entidade fraca as alterações
        if resposta!='erro':
            print('testando')
            resposta = alterar_grupo_personalizado(novas_palavras_chave, grupo_id)
            session['notificacao'] = resposta
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
