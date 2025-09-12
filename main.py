import os
import sqlite3
import pandas as pd

INPUT_DB = "database.sqlite"

# 0 - Verificar se o arquivo existe
if not os.path.exists(INPUT_DB):
    raise FileNotFoundError(f"Ué, não localizamos nada em {INPUT_DB}")
else:
    print("Localizamos o arquivo base.")

with sqlite3.connect(INPUT_DB) as conn:
    # 1.a - Listar tabelas
    query_tables = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    tables_df = pd.read_sql_query(query_tables, conn)
    print("Tabelas do Banco:")
    print(tables_df.to_string(index=False))

    # 1.b - Escolher tabela
    def escolher_tabela(conn, termo_busca=None):
        query_tables = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        tables_df = pd.read_sql_query(query_tables, conn)
        table_candidates = tables_df["name"].tolist()

        if termo_busca:
            for t in table_candidates:
                if termo_busca.lower() in t.lower():
                    print(f'Tabela escolhida: {t}')
                    return t
            print(f'Nenhuma tabela encontrada com "{termo_busca}".')

        print("\nTabelas disponíveis:")
        for i, t in enumerate(table_candidates):
            print(f"[{i}] {t}")
        idx = int(input("Digite o número da tabela que deseja usar: "))
        chosen = table_candidates[idx]
        print(f"Tabela escolhida: {chosen}")
        return chosen

    # 2 - Preview da tabela
    def preview_tabela(conn, chosen_table):
        query = f"SELECT * FROM {chosen_table} LIMIT 5;"
        preview_df = pd.read_sql_query(query, conn)
        print(f"\nPrévia da tabela {chosen_table}:")
        print(preview_df.to_string(index=False))

    # 3 - Número de linhas
    def numero_linhas(conn, chosen_table):
        query = f"SELECT COUNT(*) AS numero_linhas FROM {chosen_table}"
        contar_linhas_df = pd.read_sql_query(query, conn)
        numero_linhas = int(contar_linhas_df['numero_linhas'].iloc[0])
        print(f'Na tabela {chosen_table} temos {numero_linhas} linhas.')

    # 4 - Buscar time
    def buscar_time(conn, chosen_table, time_escolhido):
        query = f"""
            SELECT * 
            FROM {chosen_table} 
            WHERE team_long_name LIKE ? 
            LIMIT 5
        """
        df = pd.read_sql_query(query, conn, params=(f"%{time_escolhido}%",))
        if df.empty:
            print(f"Não localizamos o time {time_escolhido} na tabela {chosen_table}.")
            return None
        time_name = df["team_long_name"].iloc[0]
        print(f"Localizamos o time: {time_name}")
        print(df.to_string(index=False))
        return df

    # 5 - Pegar id do time
    def pegar_id_time(conn, table_name, team_name):
        query = f"""
            SELECT team_api_id, team_long_name
            FROM {table_name}
            WHERE team_long_name LIKE ?
            LIMIT 1;
        """
        df = pd.read_sql_query(query, conn, params=(f"%{team_name}%",))
        if df.empty:
            print(f"Não localizamos o {team_name} na tabela {table_name}.")
            return None
        team_id = int(df["team_api_id"].iloc[0])
        print(f"ID do time {df['team_long_name'].iloc[0]}: {team_id}")
        return team_id

    # 6 - Colunas da tabela
    def procurar_colunas_na_tabela(conn, chosen_table):
        query = f'PRAGMA table_info("{chosen_table}")'
        colunas_df = pd.read_sql_query(query, conn)
        print(f"\nColunas da tabela {chosen_table}:")
        print(colunas_df.to_string(index=False))

    def menu(conn):
        while True:
            print("\n=== MENU ===")
            print("[1] Listar tabelas")
            print("[2] Escolher tabela")
            print("[3] Preview da tabela")
            print("[4] Contar linhas")
            print("[5] Buscar time")
            print("[6] Procurar colunas")
            print("[0] Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                query_tables = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
                print(pd.read_sql_query(query_tables, conn).to_string(index=False))

            elif opcao == "2":
                global chosen_table
                chosen_table = escolher_tabela(conn)

            elif opcao == "3":
                preview_tabela(conn, chosen_table)

            elif opcao == "4":
                numero_linhas(conn, chosen_table)

            elif opcao == "5":
                time = input("Digite o nome do time: ")
                buscar_time(conn, chosen_table, time)

            elif opcao == "6":
                procurar_colunas_na_tabela(conn, chosen_table)

            elif opcao == "0":
                print("Saindo...")
                break

            else:
                print("Opção inválida!")

    # ========================
    # FLUXO PRINCIPAL
    # ========================

    with sqlite3.connect(INPUT_DB) as conn:
        menu(conn)
