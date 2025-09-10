import os
import sqlite3
import pandas as pd

INPUT_DB = "database.sqlite"

# 0 - Verificar se o arquivo existe
if not os.path.exists(INPUT_DB): # os.path.exists(INPUT_DB) → retorna True se o arquivo existe.
    raise FileNotFoundError(f"Ué, não localizamos nada em {INPUT_DB}") # se não existir, jogamos o erro
else:
    print("Localizamos o arquivo base.")


# 1 - Abrir conexão com o Banco
"""
    sqlite3.connect(INPUT_DB) abre o banco.
    O with garante que a conexão será fechada automaticamente no fim do bloco.
    conn é nossa variável que representa a conexão.
"""
with sqlite3.connect(INPUT_DB) as conn: # conn é a conexão com o banco, vamos usar p rodar queries aq no py
    

    # 1.a Vamos listar todas as tabelas do nosso db
    query_tables = "SELECT name FROM Sqlite_master WHERE type='table' ORDER BY 'name';" # busca só o nome das tabelas
    tables_df = pd.read_sql_query(query_tables, conn) # aqui traz um DF bonitinho com o nome das tabelas
    # pd.read_sql_query() → executa a query e já transforma o resultado em DF (tables_df).
    print("Tabelas do Banco: ")
    print(tables_df.to_string(index=False)) # to_string é para ficar bonitinho msm se tiver mta linha, tira a coluna de índice do pandas e deixa a saída mais limpa.

    # 1.b Escolher uma tabela para olhar melhor
    # Vamos começar pela "Match", que tem os jogos
    # Vamos procurar qq nome que case com "Match"
    table_candidates = tables_df["name"].tolist()
    chosen_table = None
    print("Teste: ")
    for i in table_candidates:
        if  'team' in i.lower():
            chosen_table = i.strip()
            print(f'Vamos analisa a tabela {chosen_table}')
            break # Para o loop assim que encontrar.
        
    if chosen_table is None:
        chosen_table = table_candidates[0] # Pegamos a coluna "name" (os nomes das tabelas) e transformamos em lista Python (.tolist()).
                                            # Assim conseguimos iterar e procurar a que queremos.
        print(f'Não achamos a tabela "Match", então estamos com a primeira tabela da lista, a: {chosen_table}.')

    # 2. Pegar uma pré-visualização da tabela -- vamos usar o limit
    """
    Então aqui a gente vai criar a query e colocar na variável "preview query", 
    preview_df vamos chamar o pd.read_sql_query para rodar a query acima e conn é a conexão c o banco
    depois só printar com .to_string(index=false) p ficar mais bonito
    """
    preview_query = f'Select * from"{chosen_table}" LIMIT 5;'
    preview_df = pd.read_sql_query(preview_query, conn)
    print(f"Só uma previa do que é a tabela {chosen_table}, primeiras 5 linhas: ")
    print(preview_df.head().to_string(index=False)) 

    # 3. ver as colunas da tabela -- p saber os campos q existem
    """
    PRAGMA table_info("tabela") é um comando específico do SQLite que mostra o esquema (nomes e tipos de colunas).
    """
    pragma_query = f'PRAGMA table_info("{chosen_table}")'
    colunas_df = pd.read_sql_query(pragma_query, conn)
    print(f'Colunas da tabela {chosen_table}')
    print(colunas_df.to_string(index=False))

    # 4. Saber o nº de linhas da tabela
    contar_linhas_query = f'Select count(*) as "total_linhas" from "{chosen_table}"' #  contar_linhas_df['total_linhas'] → pega a coluna total_linhas (série pandas).
    contar_linhas_df = pd.read_sql_query(contar_linhas_query, conn)
    total_linhas = int(contar_linhas_df['total_linhas'].iloc[0]) #  .iloc[0] → pega a primeira linha dessa série (ou seja, o valor da contagem).
    # int(...) → converte para número inteiro (porque vem como numpy.int64).
    print(f'A tabela {chosen_table} tem {total_linhas} linhas')

    # 5. Vamos pegar a tabela de Times
    time = "Barcelona"
    time_query = f'Select * from {chosen_table} where team_long_name like  "%{time}%" Limit 5;'
    time_df = pd.read_sql_query(time_query, conn)
    print(f'Vamos ver se conseguimos achar o {time} no meio da tabela {chosen_table}')
    print(time_df.to_string(index=False))
