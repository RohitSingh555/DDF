import requests
import xml.etree.ElementTree as ET
import csv
import hashlib
import random
import string
import mysql.connector

def generate_nonce(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def calculate_digest(username, password, method, uri, realm, nonce, cnonce, nc, qop):
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode()).hexdigest()
    return response

auth_url = "https://data.crea.ca/Login.svc/Login"

username = "CXLHfDVrziCfvwgCuL8nUahC"
password = "mFqMsCSPdnb5WO1gpEEtDCHH"

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

metadata_url = "https://data.crea.ca/Metadata.svc/GetMetadata?Type=METADATA-RESOURCE&Format=COMPACT&ID=*&Culture=en-CA"
print(auth_response.request.headers["Authorization"])
session_id = auth_response.cookies.get('X-SESSIONID')
asp_session_id = auth_response.cookies.get('ASP.NET_SessionId')
response = requests.get(
    metadata_url,
    headers={
        "Authorization": auth_response.request.headers["Authorization"],
        "X-Aspnet-Version": "4.0.30319",
        "X-Powered-By": "ASP.NET",
        "Accept":'text/xml',
        "Request-Context": "appId=cid-v1:0cdb5518-a468-4dcb-9eb7-84c61cd89b7c",
        "Cache-Control": "private",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": f"X-SESSIONID={session_id}; ASP.NET_SessionId={asp_session_id}"
    }
)

print("Response status code:", response.status_code)

with open('metadata.xml', 'wb') as xmlfile:
    xmlfile.write(response.content)

print("XML data saved to metadata.xml.")

tree = ET.parse('metadata.xml')
root=tree.getroot()
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='ddf'
)
cursor = db.cursor()

def process_table(table_element, is_lookup=False):
    table_name = table_element.attrib['Resource']
    columns_element = table_element.find('COLUMNS')

    if columns_element is None:
        print(f"No column data found for {table_name} table.")
        return

    columns = [column.strip() for column in columns_element.text.split()]

    if is_lookup:
        table_name += '_lookup'

    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
    create_table_query += ', '.join([f"`{column.replace(' ', '_')}` VARCHAR(255)" for column in columns])
    create_table_query += ")"

    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully.")

    cursor.execute(f"TRUNCATE TABLE `{table_name}`")

    placeholders = ', '.join(['%s'] * len(columns))

    for data in table_element.findall('DATA'):
        data_parts = data.text.split()
        
        column_values = data_parts[1:-5]
        date_string = ' '.join(data_parts[-5:])  
        
        while len(column_values) < len(columns) - 1:
            column_values.append('-')

        column_values.append(date_string)

        replace_query = f"REPLACE INTO `{table_name}` ({', '.join([f'`{column.replace(' ', '_')}`' for column in columns])}) VALUES ({placeholders})"
        try:
            cursor.execute(replace_query, column_values)
            print(f"{cursor.rowcount} rows replaced in {table_name} table.")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Warning: {e}")

    print(f"All available data replaced in {table_name} table.")

tree = ET.parse('metadata.xml')
root = tree.getroot()

for table in root.findall('.//METADATA-TABLE'):
    process_table(table)

for lookup_table in root.findall('.//METADATA-LOOKUP'):
    process_table(lookup_table, is_lookup=True)

db.commit()
cursor.close()
db.close()

print("Data replaced in MySQL database.")