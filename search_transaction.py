import xml.etree.ElementTree as ET
import requests
import hashlib
import random
import string
import mysql.connector
from http.cookiejar import CookieJar
from datetime import datetime, timedelta

cookieJar = CookieJar() 
username = "iE6svatdsq6SjsaqxM7ESGz1"
password = "D2odQ7u73fjmeypyEiDmaBgo"
RetsUrl = "https://data.crea.ca"
auth_url = "https://data.crea.ca/Login.svc/Login"

def generate_nonce(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def calculate_digest(username, password, method, uri, realm, nonce, cnonce, nc, qop):
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode()).hexdigest()
    return response

def get_local_name(tag):
    if '}' in tag:
        return tag.split('}')[1]
    else:
        return tag

def SearchTransaction(RetsUrl, SearchType, Class, QueryType, Query, Count=1, Limit="100", Offset=1, Culture="en-CA", Format="STANDARD-XML"):
    request_arguments = "?Format=" + Format + "&SearchType=" + SearchType + "&Class=" + Class + "&QueryType=" + QueryType + "&Query=" + Query + "&Count=" + str(Count) + "&Limit=" + str(Limit) + "&Offset=" + str(Offset) + "&Culture=" + Culture
    search_service = RetsUrl + "/Search.svc/Search" + request_arguments

    print("URL:", search_service) 

    session_id = auth_response.cookies.get('X-SESSIONID')
    asp_session_id = auth_response.cookies.get('ASP.NET_SessionId')

    try:
        response = requests.get(
            search_service,
            headers={
                "Authorization": auth_response.request.headers["Authorization"],
                "X-Aspnet-Version": "4.0.30319",
                "X-Powered-By": "ASP.NET",
                "Accept": "text/xml",
                "Cache-Control": "private",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Cookie": f"X-SESSIONID={session_id}; ASP.NET_SessionId={asp_session_id}"
            },
            cookies=cookieJar
        )

        print("Response status code:", response.status_code)

        if response.status_code == 200 and Query != "(ID=*)":
            with open('metadata.xml', 'wb') as xmlfile:
                xmlfile.write(response.content)

            print("XML data saved to metadata.xml.")

            tree = ET.parse('metadata.xml')
            root = tree.getroot()

            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ddf'
            )
            cursor = db.cursor()

            create_table(cursor, root)  

            for property_detail in root.findall('.//{urn:CREA.Search.Property}PropertyDetails'):
                process_table(property_detail, cursor)

            db.commit()
            cursor.close()
            db.close()

    except Exception as ex:
        print("Error:", ex)

def create_table(cursor, root):
    table_name = 'property_listings_2'
    column_names = set()

    def collect_columns(element):
        if element.tag != 'PropertyDetails':
            column_names.add(get_local_name(element.tag))
            for child in element:
                if child.tag != 'PropertyDetails':
                    if child.tag == 'AgentDetails':
                        for sub_child in child:
                            if sub_child.tag != 'PropertyDetails':
                                column_names.add(get_local_name(sub_child.tag))
                    else:
                        collect_columns(child)

    for property_detail in root.findall('.//{urn:CREA.Search.Property}PropertyDetails'):
        collect_columns(property_detail)

    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
    create_table_query += '`ID` VARCHAR(255), ' 
    create_table_query += ', '.join([f"`{column.replace(' ', '_')}` TEXT" for column in column_names])
    create_table_query += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
    print(create_table_query)
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully.")

def process_table(table_element, cursor):
    table_name = 'property_listings_2'

    data = {}
    for element in table_element.iter():
        if element.tag != 'PropertyDetails':
            if get_local_name(element.tag) == 'ListingID':
                data['ID'] = element.text.strip().replace('DEMO', '') if element.text else None
            else:
                data[get_local_name(element.tag)] = element.text.strip() if element.text else None  

    data = {key: value for key, value in data.items() if value is not None}

    for column, value in data.items():
        if value and len(value) > 255:
            data[column] = value[:250]

    if 'ID' in data:
        placeholders = ', '.join(['%s'] * len(data))
        replace_query = f"REPLACE INTO `{table_name}` ({', '.join([f'`{column}`' for column in data.keys()])}) VALUES ({placeholders})"

        values = [data[column] for column in data]
        try:
            check_query = f"SELECT ID FROM `{table_name}` WHERE ID = %s"
            cursor.execute(check_query, (data['ID'],))
            existing_row = cursor.fetchone()

            if not existing_row:
                cursor.execute(replace_query, values)
                print(f"{cursor.rowcount} rows replaced in {table_name} table.")
            else:
                print("ID already exists. Skipping insertion.")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Warning: {e}")

    print(f"All available data replaced in {table_name} table.")


response = requests.get(auth_url)
if response.status_code != 401:
    print("Error: Initial request did not return expected 401 Unauthorized status code.")
    exit()

nonce = response.headers.get('WWW-Authenticate').split('nonce="')[1].split('"')[0]

cnonce = generate_nonce()

auth_response = requests.get(
    auth_url,
    headers={
        "Authorization": f'Digest username="{username}", realm="CREA.Distribution", nonce="{nonce}", uri="/Login.svc/Login", response="{calculate_digest(username, password, "GET", "/Login.svc/Login", "CREA.Distribution", nonce, cnonce, "00000003", "auth")},nc=00000003, qop="auth", cnonce="{cnonce}"'
    }
)

print(auth_response.content)
if auth_response.status_code != 200:
    print("Error: Authentication failed.")
    exit()

print("Authentication successful!")

SearchType = "Property" 
Class = "Property" 
QueryType = "DMQL2" 
today = datetime.now()
two_days_ago = today - timedelta(days=2)
date_time_format = "%Y-%m-%dT%H:%M:%SZ"
two_days_ago_str = two_days_ago.strftime(date_time_format)
Query = f"(LastUpdated={two_days_ago_str})"
Count = 1 
Limit = "100" 
Offset = 100 
Culture = "en-CA" 
Format = "STANDARD-XML" 
SearchTransaction(RetsUrl,str(SearchType), str(Class), str(QueryType),Query, Count=Count, Limit=str(Limit), Offset=Offset, Culture=str(Culture), Format=str(Format))

tree = ET.parse('metadata.xml')
root = tree.getroot()
total_pages = root.find('.//{urn:CREA.Search.Property}TotalPages').text
total_pages= int(total_pages)
def run_search_transactions(total_pages):
    
    for i in range(1, total_pages + 1):
        Offset = (i - 1) * 100 + 1
        
        SearchTransaction(RetsUrl, str(SearchType), str(Class), str(QueryType), Query, Count=Count, Limit=str(Limit), Offset=Offset, Culture=str(Culture), Format=str(Format))

run_search_transactions(total_pages)