# Sobre o Projeto

O Scrapinpy.py é uma ferramenta projetada para extrair informações específicas, conhecidas como normativos, disponíveis no site gov.br dentro da sessão do diario oficial da união. Esses normativos são documentos ou regulamentos oficiais que contêm diretrizes, regras e informações relevantes para uma variedade de áreas. O objetivo principal do Scrapinpy.py é coletar esses normativos automaticamente e organizá-los em arquivos CSV, um formato de planilha amplamente utilizado. Isso facilita a coleta e análise de dados desses documentos, tornando o processo mais acessível e eficiente, mesmo para aqueles que não são especialistas em tecnologia ou regulamentações governamentais.

## Arquitetura

O sistema é construído seguindo algumas boas práticas, como a ideia de cada parte fazer uma coisa só (Responsabilidade Única). Ele usa um jeito específico de organizar suas partes, chamado de paradigma funcional, para fazer as coisas acontecerem. Além disso, as diferentes partes do sistema estão organizadas em camadas para tornar tudo mais organizado.

### Scraping
A camada scraping é responsável por armazenar os módulos específicos para scraping. Os módulos armazenados, por sua vez, utilizam bibliotecas externas para extrair informações relevantes das páginas da web, seguindo princípios funcionais para manipulação de dados.

### Queue
A camada queue é responsável por armazenar os módulos específicos para criação e processamento de filas (queues). Este módulo, por sua vez, utiliza as camadas de scraping para otimizar o processamento de dados e estruturação de dados.

### Worker
A camada worker é responsável por armazenar os módulos específicos para workers. Os módulos armazenados, por sua vez, utilizam a camada de queue e scraping para a organização das informações coletadas no processo de scraping.

## Processo de Raspagem de Dados

Por meio do módulo `main`, é processada uma série de funções responsáveis por obter de forma eficiente os dados necessários. Isso é feito por meio da função `get_amount_normative`, onde obtemos a quantidade total de normativos, uma informação crucial para calcular o número de páginas a serem processadas. A função `get_amount_pages` realiza esse cálculo, facilitando a subsequente geração das URLs de cada página de normativos por meio da função `get_all_urls_pages`. O componente central, a função `worker`, é encarregado da raspagem de dados de uma página específica, coletando as informações relevantes. Por fim, a função `process_queue` é essencial para realizar operações pós-raspagem na fila de normativos, finalizando o processo de maneira ordenada.

### Criação do JSON e CSV Estruturado

Após a conclusão do processo de raspagem de dados e a coleta das informações de normativos através das funções mencionadas, a função principal `main()` adiciona os resultados em uma estrutura de dados chamada `content_from_normative`. Essa estrutura contém as informações processadas de cada normativo, sendo então convertida em um arquivo JSON denominado 'normatives.json' utilizando a biblioteca json.


### Criação do json e csv estrutarado 

Após a conclusão do processo de raspagem de dados e a coleta das informações de normativos através das funções mencionadas, a função principal ```main()``` adiciona os resultados em uma estrutura de dados chamada ```content_from_normative```. Essa estrutura contém as informações processadas de cada normativo, é então convertida em um arquivo JSON denominado 'normatives.json' utilizando a biblioteca json.
#### exemplo json 
```json
      {
    "conteudo_documento": [
      "A UNIÃO, por intermédio do MINISTÉRIO DA INTEGRAÇÃO E DO DESENVOLVIMENTO REGIONAL, neste ato representado pelo SECRETÁRIO NACIONAL DE PROTEÇÃO E DEFESA CIVIL, nomeado pela Portaria n. 190, de 1° de janeiro de 2023, publicada no D.O.U, de 2 de janeiro de 2023, Seção 2, Edição Extra B, consoante delegação de competência conferida pela Portaria n. 2.191, de 27 de junho de 2023, publicada no DOU, de 28 de junho de 2023, Seção 1, e tendo em vista o disposto na Lei nº 12.340, de 01 de dezembro de 2010, na Lei nº 12.608, de 10 de abril de 2012, no Decreto nº 11.219, de 5 de outubro de 2022 e no Decreto nº 11.655, de 23 de agosto de 2023, resolve:",
      "Art. 1° Autorizar o empenho e o repasse de recursos ao Município de Xapuri - AC, no valor de R$ 349.765,68 (trezentos e quarenta e nove mil setecentos e sessenta e cinco reais e sessenta e oito centavos), para a execução de ações de resposta, conforme processo n. 59052.022305/2024-95.",
      "Art. 2° Os recursos financeiros serão empenhados a título de Transferência Obrigatória, conforme legislação vigente, observando a classificação orçamentária: PT: 06.182.2318.22BO.6500; GND: 3.3.40.41; Fonte: 3000; UG: 530012.",
      "Art. 3° Considerando a natureza e o volume de ações a serem implementadas, o prazo de execução será de 180 dias, a partir da publicação desta portaria no Diário Oficial da União (DOU).",
      "Art. 4° A utilização, pelo ente beneficiário, dos recursos transferidos está vinculada exclusivamente à execução das ações especificadas no art. 1° desta Portaria.",
      "Art. 5° O proponente deverá apresentar prestação de contas final no prazo de 30 dias a partir do término da vigência, nos termos do art. 32 do Decreto nº 11.655, de 23 de agosto de 2023.",
      "Art. 6° Esta Portaria entra em vigor na data de sua publicação."
    ],
    "anexo_documento": [],
    "titulo_normativo": "PORTARIA Nº 736, DE 1º DE MARÇO DE 2024",
    "document_url": "https://www.in.gov.br/web/dou/-/portaria-n-736-de-1-de-marco-de-2024-546047771",
    "ementa": "Autoriza o empenho e a transferência de recursos ao Município de Xapuri - AC, para execução de ações de Defesa Civil.",
    "assinante_documento": "WOLNEI WOLFF BARREIROS",
    "orgao": "Ministério da Integração e do Desenvolvimento Regional/Secretaria Nacional de Proteção e Defesa Civil",
    "data_publicacao": "01/03/2024"
  },
```
Após a criação do JSON é chamada a função ```convert_json_to_csv``` responsavel por a criação do arquivo CSV. Ela utiliza a biblioteca pandas para carregar o arquivo JSON e convertê-lo em um DataFrame, uma estrutura tabular eficiente. Posteriormente, o DataFrame é exportado para um arquivo CSV chamado 'normatives.csv'. Essa abordagem oferece uma maneira organizada e estruturada de armazenar dados, tornando-os facilmente acessíveis para análises posteriores. 

## Requisitos de Ambiente

Os requisitos do projeto estão devidamente especificados no arquivo `requirements.txt`. Este arquivo contém todas as bibliotecas necessárias, incluindo suas versões específicas, garantindo que o ambiente do projeto seja reproduzível e consistente. Durante a execução do projeto, é recomendado utilizar uma ferramenta de gerenciamento de ambientes virtuais, como o virtualenv, para isolar as dependências do projeto de outros ambientes Python.

## Licença 

O projeto Scrapinpy.py utiliza a Licença MIT, uma licença de software aberta e permissiva que oferece aos desenvolvedores uma grande liberdade para utilizar, modificar e distribuir o código fonte.

## Desempenho

O projeto utiliza estratégias eficientes para otimizar o desempenho na extração de dados e na criação do arquivo CSV utilizando a combinação de threads e processamento assíncrono.

A função `process_queue` dentro do módulo `queue` utiliza uma fila assíncrona para organizar os URLs das normativas a serem processadas. Durante o processamento, é estabelecida uma sessão assíncrona com o `aiohttp.ClientSession`, onde um semáforo limita o número de requisições simultâneas para 15, visando evitar possíveis bloqueios ou sobrecargas no servidor. Esse método assíncrono proporciona um ganho significativo de desempenho, permitindo a recuperação eficiente dos dados de múltiplas páginas de normativas de forma paralela.

A função `process_normative_queue` é responsável por processar os itens da fila. Utilizando uma fila convencional (Queue), os itens são retirados da fila e processados em paralelo por várias threads. A função `convert_json_to_csv` inicia um número determinado de threads (no exemplo, 4), cada uma processando os itens da fila. Essa abordagem aproveita a concorrência proporcionada pelas threads para acelerar o processamento dos dados.

O tempo para o processamento total do programa é de aproximadamente 550 segundos, sendo processados 4432 normativos.

## Tratamento de Exceções

O tratamento de exceções é usado para assegurar a confiabilidade durante a extração de informações do Diário Oficial da União (DOU) por meio de funções como a  `safe_request` dentro do módulo `normative_scraping`. Essa função é responsável por criar um bloco try-except ao realizar requisições HTTP assíncronas, lidando com possíveis erros de conexão ou resposta do servidor. As funções de extração de informações, como `extract_amount_normative` e `get_content_from_normative`, garantem que, em caso de falha na requisição ou ausência de informações, elas retornem None, minimizando impactos decorrentes de falhas e promovendo a confiabilidade do processo de scraping.



