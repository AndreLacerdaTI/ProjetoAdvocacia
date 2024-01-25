import sqlite3

# Criação do Banco

"""
# Conectar ao banco de dados (cria o banco se não existir)
conn = sqlite3.connect('filtros.db')
# Criar um cursor para executar comandos SQL
cursor = conn.cursor()
# Criar a tabela 'PalavraChave' se ainda não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PalavraChave (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palavra_chave TEXT UNIQUE
    )
''')

# Criar a tabela 'Derivacao' se ainda não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Derivacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palavra_chave_id INTEGER,
        derivacao TEXT,
        FOREIGN KEY (palavra_chave_id) REFERENCES PalavraChave(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Grupo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT
    )
''')

# Criar tabela de junção para mapear a relação muitos-para-muitos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS GrupoPersonalizado (
        palavra_chave_id INTEGER,
        grupo_id INTEGER,
        FOREIGN KEY (palavra_chave_id) REFERENCES PalavraChave(id),
        FOREIGN KEY (grupo_id) REFERENCES Grupo(id),
        PRIMARY KEY (palavra_chave_id, grupo_id)
    )
''')

# Exemplo de inserção de dados
cursor.execute("INSERT INTO PalavraChave (palavra_chave) VALUES (?)", ('Python',))
cursor.execute("INSERT INTO Derivacao (palavra_chave_id, derivacao) VALUES (?, ?)",
               (1, 'Programação em Python'))

cursor.execute("INSERT INTO PalavraChave (palavra_chave) VALUES (?)", ('SQL',))
cursor.execute("INSERT INTO Derivacao (palavra_chave_id, derivacao) VALUES (?, ?)",
               (2, 'Structured Query Language'))

# Salvar (commit) as alterações no banco de dados
conn.commit()
"""

# Ações Back-end no banco

def salvar_grupo_personalizado(lista_palavras, grupo_id):
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    for id in lista_palavras:
        cursor.execute('INSERT INTO GrupoPersonalizado (palavra_chave_id, grupo_id) VALUES (?, ?)', (id,grupo_id))
        conn.commit()
    return 'Grupo adicionado com sucesso!'

def salvar_novo_grupo(nome, descricao):
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    try:
        cursor.execute("INSERT INTO Grupo (nome, descricao) VALUES (?, ?)", (nome, descricao))
        grupo_id = cursor.lastrowid
        conn.commit()
        return grupo_id
    except:
        return 'erro'

def detalhar_filtro(id):
    # Conectar ao banco de dados (cria o banco se não existir)
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    cursor.execute("SELECT informacoes FROM PalavraChave WHERE id = ?", (id,))
    resultados = cursor.fetchall()
    return resultados

def adicionar_palavra_chave(palavra_chave):
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    try:
        cursor.execute("INSERT INTO PalavraChave (palavra_chave) VALUES (?)", (palavra_chave,))
        conn.commit()
        return 'Palavra-chave "%s" adicionada com sucesso!' % palavra_chave
    except:
        return 'Erro ao salvar palavra-chave "%s"!' % palavra_chave

def buscar_filtros():
    # Conectar ao banco de dados (cria o banco se não existir)
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    cursor.execute("SELECT p.id, p.palavra_chave, d.derivacao FROM PalavraChave p LEFT JOIN Derivacao d ON p.id = d.palavra_chave_id ORDER BY p.palavra_chave")
    resultados = cursor.fetchall()
    return resultados

def buscar_nomes_filtros():
    # Conectar ao banco de dados (cria o banco se não existir)
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    cursor.execute("SELECT palavra_chave FROM PalavraChave")
    resultados = cursor.fetchall()
    lista = []
    for linha in resultados:
        lista_resultante = list(linha)
        lista.append(lista_resultante[0])
    print(lista)
    return lista

def buscar_grupos():
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todos os grupos
    cursor.execute("SELECT * FROM Grupo ORDER BY nome")
    resultados = cursor.fetchall()
    return resultados

def buscar_grupo(id):
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar grupo especifico
    cursor.execute("SELECT * FROM Grupo WHERE id = ?", (id,))
    resultados = cursor.fetchall()
    print(resultados[0])
    return resultados[0]

def alterar_grupo_personalizado(lista_palavras, grupo_id):
    print(lista_palavras, grupo_id)
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    for id in lista_palavras:
        #cursor.execute('INSERT INTO GrupoPersonalizado (palavra_chave_id, grupo_id) VALUES (?, ?)', (id,grupo_id))
        #cursor.execute('UPDATE Grupo SET nome = ?, descricao = ? WHERE id = ?', (nome, descricao, grupo_id))
        conn.commit()
    return 'Grupo adicionado com sucesso!'
    '''
    for id_palavra in palavras_chave_id:
        apagar_grupo_personalizado(id_palavra, grupo_id)
    '''

def salvar_alteracao_grupo(grupo_id, nome, descricao):
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    try:
        cursor.execute('UPDATE Grupo SET nome = ?, descricao = ? WHERE id = ?', (nome, descricao, grupo_id))
        conn.commit()
        return grupo_id
    except:
        return 'erro'

def consultar_grupo_personalizado():
    # Conectar ao banco de dados SQLite
    conexao = sqlite3.connect('filtros.db')
    cursor = conexao.cursor()

    # Executar uma consulta SELECT na tabela GrupoPersonalizado
    cursor.execute('SELECT * FROM GrupoPersonalizado')

    # Obter todos os resultados da consulta
    resultados = cursor.fetchall()

    # Fechar a conexão
    conexao.close()
    return resultados
def apagar_grupo_personalizado(palavra_chave_id, grupo_id):
    # Conectar ao banco de dados SQLite
    conexao = sqlite3.connect('filtros.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM GrupoPersonalizado WHERE palavra_chave_id = ? AND grupo_id = ?', (palavra_chave_id, grupo_id))
    conexao.commit()

def buscar_palavras_grupo_personalizado(palavras_chave_id):
    print(palavras_chave_id)
    conexao = sqlite3.connect('filtros.db')
    cursor = conexao.cursor()
    consulta_sql = 'SELECT * FROM PalavraChave WHERE id IN ({})'.format(','.join('?' for _ in palavras_chave_id))
    # Executar a consulta SQL com a lista como parâmetro
    cursor.execute(consulta_sql, palavras_chave_id)
    #cursor.execute('SELECT * FROM PalavraChave WHERE id IN ({})'.format(','.join('?' for _ in palavras_chave_id)))
    resultados = cursor.fetchall()
    return resultados

# Fechar a conexão
#conn.close()