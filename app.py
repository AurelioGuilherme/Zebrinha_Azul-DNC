import streamlit as st
from streamlit_option_menu import option_menu
from paginas import modelagem_de_banco_de_dados, extracao_via_api, sobre, transformacao_de_dados
import sqlite3


# Opções do menu
MENU_LIST = ['Sobre',
             'Modelagem de Banco de dados',
             'Extração via API',
             'Transformação de dados',
             'Carregamento no Bando de Dados']

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        st.error(e)

# Configurações do Menu
with st.sidebar:
    st.image('Imagens/logo.png', width=100)
    st.sidebar.title('Zebrinha Azul - Case DNC')
    selected = option_menu("",MENU_LIST, default_index=0)




def main():
    
    # Conecta com banco de dados
    conn = create_connection("zebrinha_azul.db")

    # Pagina Sobre
    if selected == 'Sobre':
        sobre.view(conn)

        st.write('''
                    **Melhorias planejas**
                 
                 - Incluir gráficos de barras das 10 cidades mais visitadas
                 - Melhoria na disposição visual das informações de destino e origem
                 - Adicionar gráficos relacionadas ao tempo de viagem e distancia
                 - Incluir a possibilidade de filtrar por estado
                 - Melhoria nas transformações dos dados (tradução de condição climatica, separação do nome da cidade,estado e páis.)
                 - Incluir Box para poder efetuar consultas SQL, dando opção de baixar o resultado em csv ou xlsx.
                                  
                ''')
        

    elif selected == 'Modelagem de Banco de dados':
        st.title('Modelagem de Banco de dados')
        st.write('---')
        modelagem_de_banco_de_dados.view()
        

        

    elif selected == 'Extração via API':
        st.title('Extração via API')
        st.write('---')
        extracao_via_api.view()
        
        


    elif selected == 'Transformação de dados':
        st.title('Transformação de dados')
        st.write('---')        
        transformacao_de_dados.view()
        
     

    elif selected == 'Carregamento no Bando de Dados':
        st.title('Carregamento no Bando de Dados')
        st.write('---')
        sobre.view(conn)

        st.write('# Em construção 😢 ')
        st.write('Nesta página irei incluir os detalhes do carregamento no banco de dados.')

        




#st.write('https://dncgroupbr.notion.site/Engenheiro-de-Dados-d60059a87c874e479390d273b420f063')

if __name__ == '__main__':
    main()