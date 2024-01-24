import sqlite3
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

def buscar_grupos():
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    cursor.execute("SELECT * FROM Grupo ORDER BY nome")
    resultados = cursor.fetchall()
    return resultados
"""
# Conectar ao banco de dados (cria o banco se não existir)
conn = sqlite3.connect('filtros.db')
# Criar um cursor para executar comandos SQL
cursor = conn.cursor()
# Consultar todas as palavras-chave com suas derivações
cursor.execute("SELECT p.id, p.palavra_chave, d.derivacao FROM PalavraChave p LEFT JOIN Derivacao d ON p.id = d.palavra_chave_id")
resultados = cursor.fetchall()
print(resultados)

# Exibir os resultados
print("Palavras-Chave e Derivações:")
for resultado in resultados:
    print(f"ID: {resultado[0]}, Palavra-chave: {resultado[1]}, Derivação: {resultado[2]}")
"""
# Fechar a conexão
#conn.close()