import sqlite3

def criar_conexao():
    
    #Cria uma conexão com o banco de dados SQLite. 
    #Retorna: conn (sqlite3.Connection): Retorna a conexão com o banco de dados, permitindo usar comandos SQL.
    
    conn = sqlite3.connect('Estacio_Trabalho_Gabriel5.db')
    return conn

def criar_tabelas(conn):
    
    #Cria as tabelas 'alunos' e 'notas' no banco de dados se elas não existirem.
    
    sql_criar_tabela_alunos = '''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        curso TEXT
    );
    '''
    # SQL para criar a tabela 'notas'
    sql_criar_tabela_notas = '''
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        nota1 REAL,
        nota2 REAL,
        media REAL,
        FOREIGN KEY (aluno_id) REFERENCES alunos (id)
    );
    '''
    # Executa os comandos SQL para criar as tabelas
    conn.execute(sql_criar_tabela_alunos)
    conn.execute(sql_criar_tabela_notas)

def adicionar_informacoes(conn, nome, idade, curso, nota1, nota2):
    #Adiciona informações de um novo aluno e suas notas ao banco de dados.

    # SQL para inserir um novo aluno
    sql_aluno = ''' INSERT INTO alunos(nome, idade, curso)
                    VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql_aluno, (nome, idade, curso))
    aluno_id = cur.lastrowid  # Obtém o ID do aluno recém-inserido

    # Calcula a média das notas
    media = (nota1 + nota2) / 2

    # SQL para inserir as notas do aluno
    sql_nota = ''' INSERT INTO notas(aluno_id, nota1, nota2, media)
                   VALUES(?,?,?,?) '''
    cur.execute(sql_nota, (aluno_id, nota1, nota2, media))
    conn.commit()  # Salva (commita) as alterações no banco de dados

def excluir_por_id(conn, id):
    
    #Exclui a informação de ambas as tabelas ('alunos' e 'notas') com base no ID.

    cur = conn.cursor()
    cur.execute('DELETE FROM notas WHERE aluno_id=?', (id,))
    cur.execute('DELETE FROM alunos WHERE id=?', (id,))
    conn.commit()

def atualizar_aluno(conn, id, nome, idade, curso):
    #Atualiza os dados de um aluno.
   
    # SQL para atualizar os dados do aluno
    sql = ''' UPDATE alunos
              SET nome = ? ,
                  idade = ? ,
                  curso = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (nome, idade, curso, id))
    conn.commit()

def atualizar_nota(conn, id, aluno_id, nota1, nota2):
    """
    Atualiza as notas de um aluno.

    Parâmetros:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
        id (int): ID do registro de notas a ser atualizado.
        aluno_id (int): ID do aluno.
        nota1 (float): Nova primeira nota.
        nota2 (float): Nova segunda nota.
    """
    # Calcula a média das notas
    media = (nota1 + nota2) / 2

    # SQL para atualizar as notas do aluno
    sql = ''' UPDATE notas
              SET aluno_id = ? ,
                  nota1 = ? ,
                  nota2 = ? ,
                  media = ?
              WHERE id = ?'''
    
    cur = conn.cursor()
    cur.execute(sql, (aluno_id, nota1, nota2, media, id))
    conn.commit()

def consultar_alunos(conn):

    #Consulta e retorna todos os alunos cadastrados.
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos")
    rows = cur.fetchall()
    return rows

def consultar_notas(conn):

    #Consulta e retorna todas as notas cadastradas.

    cur = conn.cursor()
    cur.execute("SELECT id, nota1, nota2, media FROM notas")
    rows = cur.fetchall()
    return rows
    #Retorna: rows (list): Lista de todas as notas.

def consultar_tudo(conn):
    #Consulta e retorna todas as informações de alunos e suas notas.

    cur = conn.cursor()
    cur.execute('''
    SELECT alunos.id, alunos.nome, alunos.idade, alunos.curso, notas.nota1, notas.nota2, notas.media
    FROM alunos
    LEFT JOIN notas ON alunos.id = notas.aluno_id
    ''')
    rows = cur.fetchall()
    return rows
    #Retorna: rows (list): Lista de todas as informações de alunos e suas notas.

def main():
    
    #Função principal que interage com o usuário, dando as opções para o gerenciamento do Banco de dados
    
    database = 'notas_estudantes.db'
    
    conn = criar_conexao()
    
    if conn is not None:
        criar_tabelas(conn)
    
    while True:
        print("\nSistema de Gerenciamento de Notas de Alunos")
        print("1. Adicionar Informações")
        print("2. Visualizar Alunos")
        print("3. Atualizar Aluno")
        print("4. Visualizar Notas")
        print("5. Atualizar Nota")
        print("6. Visualizar Tudo")
        print("7. Excluir por ID")
        print("8. Sair")
        
        escolha = input("Digite sua escolha: ")
        
        if escolha == '1':
            nome = input("Digite o nome: ")
            idade = input("Digite a idade: ")
            curso = input("Digite o curso: ")
            nota1 = float(input("Digite a primeira nota: "))
            nota2 = float(input("Digite a segunda nota: "))
            adicionar_informacoes(conn, nome, idade, curso, nota1, nota2)
        
        elif escolha == '2':
            alunos = consultar_alunos(conn)
            print("\nID | Nome | Idade | Curso")
            print("------------------------")
            for aluno in alunos:
                print(aluno)
        
        elif escolha == '3':
            id = int(input("Digite o ID do aluno a ser atualizado: "))
            nome = input("Digite o novo nome: ")
            idade = input("Digite a nova idade: ")
            curso = input("Digite o novo curso: ")
            atualizar_aluno(conn, id, nome, idade, curso)
        
        elif escolha == '4':
            notas = consultar_notas(conn)
            print("\nID | Nota 1 | Nota 2 | Média")
            print("----------------------------")
            for nota in notas:
                print(nota)
        
        elif escolha == '5':
            id = int(input("Digite o ID da nota a ser atualizada: "))
            aluno_id = int(input("Digite o novo ID do aluno: "))
            nota1 = float(input("Digite a nova primeira nota: "))
            nota2 = float(input("Digite a nova segunda nota: "))
            atualizar_nota(conn, id, aluno_id, nota1, nota2)
        
        elif escolha == '6':
            todas_info = consultar_tudo(conn)
            print("\nID Aluno | Nome | Idade | Curso | Nota 1 | Nota 2 | Média")
            print("----------------------------------------------------------")
            for info in todas_info:
                print(info)
        
        elif escolha == '7':
            id = int(input("Digite o ID a ser excluído: "))
            excluir_por_id(conn, id)
        
        elif escolha == '8':
            conn.close()
            print("Saindo...")
            break
        
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == '__main__':
    main()
