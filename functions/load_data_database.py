import sqlite3
import streamlit as st

def insert_city(conn, city_name, latitude, longitude):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cidades (cidade_name, latitude, longitude) VALUES (?, ?, ?)", (city_name, latitude, longitude))
        conn.commit()
        st.success(f"{city_name} inserido com sucesso!")
    except sqlite3.Error as e:
        # A cidade já existe na tabela, não é necessário fazer nada
        pass

def insert_pessoas(conn, NOME):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pessoas (name) VALUES (?)", (NOME,))
        conn.commit()
        st.success(f"{NOME} inserido com sucesso!")
       
    except sqlite3.Error as e:
        pass


def insert_clima(conn, CONDICAO_CLIMATICA):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clima (condicao_climatica) VALUES (?)", (CONDICAO_CLIMATICA,))
        conn.commit()
        st.success(f"{CONDICAO_CLIMATICA} inserido com sucesso!")
       
    except sqlite3.Error as e:
        pass



def insert_viagem(conn, NOME, data, ENDERECO_ORIGEM, ENDERECO_DESTINO, distancia, tempo_viagem):
    try:
        cursor = conn.cursor()
        id_viajante = cursor.execute(f"SELECT id_pessoa FROM pessoas WHERE name = ?", (NOME,)).fetchone()[0]
        id_origem = cursor.execute(f"SELECT id_cidade FROM cidades WHERE cidade_name = ?", (ENDERECO_ORIGEM,)).fetchone()[0]
        id_destino = cursor.execute(f"SELECT id_cidade FROM cidades WHERE cidade_name = ?", (ENDERECO_DESTINO,)).fetchone()[0]

        cursor.execute("""
                       INSERT INTO viagem (id_viajante, data, id_origem, id_destino, distancia, tempo_viagem) 
                       VALUES (?,?,?,?,?,?)                             
                       """,
                       (id_viajante, data, id_origem, id_destino, distancia, tempo_viagem))
        conn.commit()
        st.success("Viagem inserida com sucesso!")
    except sqlite3.Error as e:
         pass


def insert_historico_clima(conn, data, cidade, condicao_climatica, temperatura, sensacao_termica):
    try:
        cursor = conn.cursor()
        id_cidade = cursor.execute(f"SELECT id_cidade FROM cidades WHERE cidade_name = ?", (cidade,)).fetchone()[0]
        id_condicao_climatica = cursor.execute(f"SELECT id_condicao_climatica FROM clima WHERE condicao_climatica = ?", (condicao_climatica,)).fetchone()[0]
        
        cursor.execute("""
                       INSERT INTO historico_clima (data, cidade, condicao_climatica, temperatura, sensacao_termica) 
                       VALUES (?,?,?,?,?)                             
                       """,
                       (data, id_cidade, id_condicao_climatica, temperatura, sensacao_termica))
        conn.commit()
        st.success("Historico climático inserida com sucesso!")
    except sqlite3.Error as e:
         pass