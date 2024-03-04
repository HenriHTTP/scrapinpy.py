from bs4 import BeautifulSoup
import json
import re
import math
import aiohttp

# url base per page
base_url_page = (
    'https://www.in.gov.br/consulta/-/buscar/dou?q=*&s=todos&exactDate=personalizado&sortType=0&delta=20&'
    'currentPage=1&newPage={}&score=0&id=546046623&'
    'displayDate=1709262000000&publishFrom=01-03-2024&publishTo=01-03-2024'
)


# validation if have problems request on url
async def safe_request(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Erro ao acessar a URL: {e}")
        return None


# this method extract string with all amount normative
async def extract_amount_normative(session, url):
    response_content = await safe_request(session, url)
    if response_content:
        html_from_request = BeautifulSoup(response_content, "html.parser")
        get_amount_normative_from_html = html_from_request.find('p', class_="search-total-label text-default")
        amount_normative = get_amount_normative_from_html.text if get_amount_normative_from_html else None
        return amount_normative
    return None


# this method extrat url value from script in html and returns a list with this value
async def extract_url_titles(session, url):
    response_content = await safe_request(session, url)
    if response_content:
        html_from_request = BeautifulSoup(response_content, "html.parser")
        get_content_from_script = html_from_request.find('script', {
            'id': '_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_params'})
        script_exist = bool(get_content_from_script)
        content_url_titles = []

        if script_exist:
            json_text = get_content_from_script.string
            json_data = json.loads(json_text)
            for item in json_data.get('jsonArray', []):
                if 'urlTitle' in item:
                    content_url_titles.append(item['urlTitle'])
        return content_url_titles
    return None


# method get url normative and return list with all url normative
async def get_url_normative(session, url):
    list_content_url_titles = await extract_url_titles(session, url)
    return list_content_url_titles if list_content_url_titles else None


# method get number pages and return list with all url pages
async def get_all_urls_pages(amount_pages):
    list_all_urls_pages = []
    for url_page in range(1, amount_pages + 1):
        list_all_urls_pages.append(base_url_page.format(url_page))
    return list_all_urls_pages


# method get number from string amount through regular expressions
async def get_amount_normative(session, url):
    amount = await extract_amount_normative(session, url)
    if amount:
        get_amount_from_string = re.findall(r'\b\d+\b', amount)
        return int(get_amount_from_string[0]) if get_amount_from_string else None
    return None


# get amount number pages and returns amount pages
async def get_amount_pages(amount_normative):
    items_per_page = 20
    return math.ceil(amount_normative / items_per_page) if amount_normative else None


# extract content normative and structure normative as a dict
async def get_content_from_normative(session, url):
    response_content = await safe_request(session, url)
    if response_content:
        html_from_response = BeautifulSoup(response_content, "html.parser")
        class_names_css = ['identifica', 'ementa', 'assina', 'cargo', 'orgao-dou-data', 'publicado-dou-data',
                           'dou-paragraph', 'dou-table']
        dict_normative_content = {'conteudo_documento': [], 'anexo_documento': []}

        for class_name in class_names_css:
            html_components = html_from_response.find_all(['p', 'span', 'table'], class_=class_name)
            for component in html_components:
                if class_name == 'identifica':
                    content_value_from_component = component.get_text(strip=True)
                    dict_normative_content['titulo_normativo'] = content_value_from_component
                if class_name == 'ementa':
                    content_value_from_component = component.get_text(strip=True)
                    dict_normative_content['ementa'] = content_value_from_component
                if class_name == 'assina':
                    content_value_from_component = component.get_text(strip=True)
                    dict_normative_content['assinante_documento'] = content_value_from_component
                if class_name == 'cargo':
                    content_value_from_component = component.get_text(strip=True)
                    dict_normative_content['cargo'] = content_value_from_component
                if class_name == 'orgao-dou-data':
                    content_value_from_component = component.get_text(strip=True)
                    dict_normative_content['orgao'] = content_value_from_component
                if class_name == 'publicado-dou-data':
                    content_value_from_component = component.get_text(strip=True)
                    dict_normative_content['data_publicacao'] = content_value_from_component
                dict_normative_content['document_url'] = str(url)
                if class_name == 'dou-paragraph':
                    if component.find_parent('td') is None:
                        content_value_from_component = component.get_text(strip=True)
                        if content_value_from_component != "":
                            dict_normative_content['conteudo_documento'].append(content_value_from_component)

                if class_name == 'dou-table':
                    table_data = await extract_table_data(component)
                    dict_normative_content['anexo_documento'].extend(table_data)

        return dict_normative_content
    return None


# extract content tables and structure as a list
async def extract_table_data(table):
    content_from_tables = []
    rows_table = table.find_all('tr')[1:]
    for row in rows_table:
        cells = row.find_all('td')
        row_content = [cell.text.strip() for cell in cells if cell.text.strip() != ""]
        content_from_tables.extend(row_content)
    return content_from_tables
