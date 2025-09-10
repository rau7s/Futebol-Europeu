import os
import sqlite3
import pandas as pd

INPUT_DB = "database.sqlite"

# 0 - Verificar se o arquivo existe
if not os.path.exists(INPUT_DB):
    raise FileNotFoundError(f"Ué, não localizamos nada em {INPUT_DB}")
else:
    print("Localizamos o arquivo base.")


# 1 - Abrir conexão com o Banco
with sqlite3.connect(INPUT_DB) as conn: # conn é a conexão com o banco, vamos usar p rodar queries aq no py

    # 1.a Vamos listar todas as tabelas do nosso db
    query_tables = "SELECT name FROM Sqlite_master WHERE type='table' ORDER BY 'name';"
    tables_df = pd.read_sql_query(query_tables, conn) # aqui traz um DF bonitinho com o nome das tabelas
    print("Tabelas do Banco: ")
    print(tables_df.to_string(index=False)) # to_string é para ficar bonitinho msm se tiver mta linha

    """print("Teste semm o to_string")
    print(tables_df)"""

    # 1.b Escolher uma tabela para olhar melhor
    # Vamos começar pela "Match", que tem os jogos
    # Vamos procurar qq nome que case com "Match"
    table_candidates = tables_df["name"].tolist()
    chosen_table = None
    print("Teste: ")
    for i in table_candidates:
        if  'match' in i.lower():
            chosen_table = i.strip()
            print(f'Vamos analisa a tabela {chosen_table}')
            break 
        
    if chosen_table is None:
        chosen_table = table_candidates[0]
        print(f'Não achamos a tabela "Match", então estamos com a primeira tabela da lista, a: {chosen_table}.')

    # 2. Pegar uma pré-visualização da tabela -- vamos usar o limit
    preview_query = f'Select * from"{chosen_table}" LIMIT 5;'
    preview_df = pd.read_sql_query(preview_query, conn)
    print(f"Só uma previa do que é a tabela {chosen_table}, primeiras 5 linhas: ")
    print(preview_df.head().to_string(index=False)) 