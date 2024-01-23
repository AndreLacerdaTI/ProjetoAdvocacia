import sqlite3
"""
# Criar a tabela 'PalavraChave' se ainda não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PalavraChave (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palavra_chave TEXT NOT NULL
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

def buscar_filtros():
    # Conectar ao banco de dados (cria o banco se não existir)
    conn = sqlite3.connect('filtros.db')
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Consultar todas as palavras-chave com suas derivações
    cursor.execute("SELECT p.id, p.palavra_chave, d.derivacao FROM PalavraChave p LEFT JOIN Derivacao d ON p.id = d.palavra_chave_id ORDER BY p.palavra_chave")
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