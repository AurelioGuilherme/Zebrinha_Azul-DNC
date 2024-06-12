import streamlit as st

def view():
    st.write('Para a extração de dados climáticos e de rotas foi utilizada a bibliotéca `requests`')

    st.subheader('Observações.')
    st.write('''
             - Não consegui obter dados históricos tanto de clima quanto de informações de rota/trânsito. 
             Por este motivo, decidi por fazer uma aplicação de cadastro.
             
             - O OpenWeatherMap exibia a mensagem que a chave era inválida ao fazer uma requisição de dados históricos.

             - Poderia obter dados climáticos por cada "passo" da rota, mas isso poderia incluir custos fora do freetier.

             - Outra opção que poderia ser abordada seria a obtenção de informações de tráfego, como congestionamento e acidentes, 
             mas também foi descartada por ter a possibilidade de gerar custos adicionais.

             ''')
    st.write('---')
    st.write(''' **`extracao_dados_climaticos`**
             
             A função extrai dados climáticos para uma dada latitude e longitude utilizando a API do OpenWeatherMap.''')
    
    st.write('[Documentação da API](https://openweathermap.org/api)')

    st.code('''
            CHAVE = '123456789' # Estou incluindo uma chave diferente por motivos de segurança.
            def extracao_dados_climaticos(lat, lon):
                URL_CLIMA = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={CHAVE}'
                r = requests.get(URL_CLIMA).json()
                return r
            ''', language='python')
    
    st.write('''
             **Parâmetros:**

            - `lat` (float): Latitude da localização desejada.
            - `lon` (float): Longitude da localização desejada.
             
            **Retorno:**
            - `r` (dict): Dados climáticos retornados pela API em formato JSON.''')
    
    st.write('---')

    st.write('''
             **`extracao_dados_de_trafico`**
             
            A função extrai dados de tráfego entre duas cidades utilizando a API do Google Maps Directions.''')
    
    st.write('[Documentação da API](https://developers.google.com/maps/documentation/directions/overview)')

    st.code('''
            
            CHAVE = 123456789 # Estou incluindo uma chave diferente por motivos de segurança.
            def extracao_dados_de_trafico(cidade_origem, cidade_destino):
                URL_TRANSITO = f"https://maps.googleapis.com/maps/api/directions/json?origin={cidade_origem}&destination={cidade_destino}&key={CHAVE}"
                r = requests.get(URL_TRANSITO)

                if r.status_code == 200:
                    data = r.json()
                    if data['status'] == 'OK':
                        return data
                    else:
                        st.error(f"Erro na resposta da API: {data['status']}")
            ''')
    st.write('''
             **Parâmetros:**

            - `cidade_origem` (str): Nome da cidade de origem.
            - `cidade_destino` (str): Nome da cidade de destino.
             
            **Retorno:**

            - `data` (dict): Dados de tráfego retornados pela API em formato JSON, se a resposta for bem-sucedida e o status for 'OK'.
            Exibe uma mensagem de erro no Streamlit se a resposta da API não for bem-sucedida.

            ''')
