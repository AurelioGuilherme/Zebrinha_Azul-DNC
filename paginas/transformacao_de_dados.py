import streamlit as st

def view():
    st.write('''
                As transformações feitas diretamente no input de dados do usuário e nos dados coletados das APIs,
                efetuando validações e conversão no tipo de dados.
             ''')
    st.write('''
                ### Funções
             
                **`transformacao_dados_climaticos(data):`**
             
                Esta função extrai a descrição da condição climática, a temperatura e a sensação térmica dos dados obtidos 
                pela API OpenWeatherMap, convertendo as temperaturas de Kelvin para Celsius e arredondando para duas casas decimais.
                  
             
                **Parâmetros:** 

                - `data`: Dicionário (json) contendo dados climáticos retornados pela API.

                **Retorno:** 
             
                - `CONDICAO_CLIMATICA`:  Descrição da condição climática, 
                - `TEMPERATURA`:  Temperatura em graus Celsius 
                - `SENSACAO_TERMICA`: Sensação térmica em graus Celsius.

                ''')
    with st.expander('**Exibir código**'):
        st.code('''
                    def transformacao_dados_climaticos(data):
                        # Extração da decrição da condição climatica
                        CONDICAO_CLIMATICA = data['weather'][0]['description']

                        # Extração de dados de temperatura e sensação termica - conversão para graus celsius e arredondamento para duas casas
                        ###
                        #data['main']['temp'] -> temperatura em Kelvin
                        #Subtri-se por -273,15 para obter dados em Gráus Celsius
                        ###

                        TEMPERATURA = round((data['main']['temp']) -273.15, 2)
                        SENSACAO_TERMICA = round((data['main']['feels_like']) -273.15, 2)

                        return CONDICAO_CLIMATICA, TEMPERATURA, SENSACAO_TERMICA
                ''', language='python')
    st.write('---')
    
    st.write('''
                **`transformacao_dados_transito(data):`**
             
                Esta função extrai a distância (em metros), o tempo (em minutos), os endereços de origem e destino, e as 
                coordenadas de latitude e longitude de origem e destino a partir do dados obtidos pela API Google Maps Directions.
             
                **Parâmetros:**
             
                - `data`: Dicionário (json) contendo dados de trânsito retornados pela API.
             
                **Retorno:**
             
                - `DISTANCIA`: Distância em metros da rota.
                - `TEMPO`: Tempo em minutos do percurso utilizando carro.
                - `ENDERECO_ORIGEM`: Endereço contendo as informações de nome da cidade estado e país da origem fornecido pelo usuário. 
                - `ENDERECO_DESTINO`: Endereço final contendo as informações de nome da cidade estado e país fornecido pelo usuário
                - `LATITUDE_ORIGEM`: Latidute da cidade de origem
                - `LONGITUDE_ORIGEM`: Longitude da cidade de origem
                - `LATITUDE_DESTINO`: Latidute da cidade de destino final
                - `LONGITUDE_DESTINO`: Longitude da cidade de destino final
             ''')
    with st.expander('**Exibir código**'):
        st.code('''
                    def transformacao_dados_transito(data):
                        # Distancia metros
                        DISTANCIA = data['routes'][0]['legs'][0]['distance']['value']

                        # tempo em minutos
                        TEMPO = data['routes'][0]['legs'][0]['duration']['value']

                        ENDERECO_ORIGEM = data['routes'][0]['legs'][0]['start_address']

                        ENDERECO_DESTINO = data['routes'][0]['legs'][0]['end_address'] 
                        LATITUDE_ORIGEM, LONGITUDE_ORIGEM = data['routes'][0]['legs'][0]['start_location'].values()  
                        LATITUDE_DESTINO, LONGITUDE_DESTINO = data['routes'][0]['legs'][0]['end_location'].values()  

                        return DISTANCIA, TEMPO, ENDERECO_ORIGEM, ENDERECO_DESTINO, LATITUDE_ORIGEM, LONGITUDE_ORIGEM, LATITUDE_DESTINO, LONGITUDE_DESTINO
                ''')
    st.write('---')

    st.write('''
                **`texto_valido(texto):`**
             
                Esta função verifica se a string fornecida contém apenas letras e espaços, usando uma Regex.
             
                **Paramêtros:**
             
                - `texto`: String que será verificada.

                **Retorno:**
             
                - `True` se o texto for válido, caso contrário, `False`.
            ''')
    with st.expander('**Exibir código**'):
        st.code('''
                    def texto_valido(texto):
                        # Regex para verificar se o texto contém apenas letras e espaços
                        return bool(re.match("^[A-Za-zÀ-ÿà-ÿ ]+$", texto))
                ''',language='python')
    st.write('---')

    st.write('''
                **`converter_texto(texto):`**
             
                Esta função remove os acentos do texto e converte todos os caracteres para maiúsculas.
             
              **Paramêtros:**
             
                - `texto`: String que será convertida.

                **Retorno:**
             
                - `texto_maiusculo`: A string convertida sem acentos e em letras maiúsculas.
            ''')
    with st.expander('**Exibir código**'):
        st.code('''
                   def converter_texto(texto):
                       texto_sem_acento = unidecode(texto)
                       texto_maiusculo = texto_sem_acento.upper()
                       return texto_maiusculo
                ''')
        
    st.subheader('Extratégia de transformações e validações')
    st.write('''
                Como a aplicação é um formulário em que o usuário preenche dados com o nome, cidade de origem e destino
             é feita verificação dos dados fornecidos pelo o usuário utilizando a função `texto_valido()`, após isso todos 
             os dados fornecidos são transformados em letras maiusculas e removidos os acentos com a função `converter_texto()`, 
             caso o usuário forneça alguma informação invalida é exibida a mensagem de erro sobre qual campo foi fornecido informações incorretas.

             Ao fornecer todos os dados corretamente, é exibida a mensagem que os dados são validos e é obtida a informação 
             da data atual e armazenada a informação padronizada para ingestão futura no banco de dados.

             Logo após, é feita a requisição na API  com a função `extracao_dados_de_trafico()` e aplicada as transformações
             utilizando a função `transformacao_dados_transito()` para a obtenção dos dados, entre eles a **latitude** e **longitude** que são essenciais 
             para a aplicação.

             Estes dados são fornecidos como parâmetros para a próxima requisição.

             Com estes dados, é feita a segunda requisição na API de dados climáticos com a função
             `extracao_dados_climaticos()`, logo em seguida feitas suas devidas transformações nos dados obtidos com a função 
             `transformacao_dados_climaticos()`. 

            ''')
    
    st.subheader('Transformações possíveis e o porquê de não ter implementado.')
    st.write('''
                As aplicações possuem diversos dados que podem ser melhorados, como por exemplo, extração da informação do estado e país.
             outra transformação úitil, seria do horário atual e previsão de horário de chegada do usuário.

             Outra deficiência seria em questão do nome do usuário ser a única informação preenchida para diferenciar o usuário, a forma 
             mais "correta" seria utilizar informações como o CPF para distinguir cada usuário além da obtenção de mais dados.
            ''')
