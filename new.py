import xml.etree.ElementTree as ET
import requests
import hashlib
import random
import string
import mysql.connector
from http.cookiejar import CookieJar
from datetime import datetime, timedelta
import time
import json

cookieJar = CookieJar() 
username = "iE6svatdsq6SjsaqxM7ESGz1"
password = "D2odQ7u73fjmeypyEiDmaBgo"
RetsUrl = "https://data.crea.ca"
auth_url = "https://data.crea.ca/Login.svc/Login"

global_date = None

def lambda_handler(event, context):
    global global_date
    
    request_body = json.loads(event['body'])
    date_input = request_body.get('date')
    
    global_date = date_input
    
    print("Received date input:", global_date)
    
    return {
        "statusCode": 200
    }
def parse_tab_separated_data(data):
    # Split the tab-separated data into individual fields
    fields = data.split("\t")
    return fields

def add_columns_to_table(columns, cursor):
    for column in columns:
        try:
            cursor.execute(f"ALTER TABLE new_property_listings ADD COLUMN `{column}` VARCHAR(255)")
            print(f"Column '{column}' added to the table.")
        except mysql.connector.Error as err:
            if err.errno == 1060:  # Error code for duplicate column name
                print(f"Column '{column}' already exists.")
            else:
                print(f"Error adding column '{column}': {err}")

def Compact_SearchTransaction():
    RetsUrl = "https://data.crea.ca"
    SearchType = "Property" 
    Class = "Property" 
    QueryType = "DMQL2" 
    today = datetime.now()
    two_days_ago = today - timedelta(days=2)
    date_time_format = "%Y-%m-%dT%H:%M:%SZ"
    two_days_ago_str = two_days_ago.strftime(date_time_format)
    Query = f"(LastUpdated={two_days_ago_str})"

    session_id = auth_response.cookies.get('X-SESSIONID')
    asp_session_id = auth_response.cookies.get('ASP.NET_SessionId')
    request_arguments = f"?Format=COMPACT&SearchType={SearchType}&Class={Class}&QueryType={QueryType}&Query={Query}&Count=1&Limit=100&Offset=1&Culture=en-CA"
    search_service = RetsUrl + "/Search.svc/Search" + request_arguments
    print("URL:", search_service)
    
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
        if response.status_code == 200 and Query != "(ID=*)":
            with open('Compactdata.xml', 'wb') as xmlfile:
                xmlfile.write(response.content)

            print("XML data saved to Compactdata.xml.")

            tree = ET.parse('Compactdata.xml')
            root = tree.getroot()
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ddf'  # Change to your database name
            )
            cursor = db.cursor()

            # Extract column names from the XML
            columns_data = root.find('.//COLUMNS').text.strip()
            columns = columns_data.split("\t")
            print("Columns:", columns)

            # Add columns to the table if they don't exist
            add_columns_to_table(columns, cursor)

            for data_element in root.findall('.//DATA'):
                data = data_element.text.strip()
                if data:
                    fields = parse_tab_separated_data(data)
                    print("Data Fields:", fields)

                    if len(fields) == len(columns):
                        placeholders = ', '.join(['%s'] * len(fields))
                        sql_insert = f"INSERT INTO new_property_listings ({', '.join(columns)}) VALUES ({placeholders})"
                        print("SQL Query:", sql_insert)  # Print the SQL query
                        cursor.execute(sql_insert, fields)
                    else:
                        print("Column count doesn't match value count.")
                        continue

            db.commit()
            cursor.close()
            db.close()
            print("Data inserted successfully.")
    except Exception as ex:
        print("Error:", ex)


def update_database_with_xml_data(id):
    SearchType = "Property" 
    Class = "Property" 
    QueryType = "DMQL2" 
    Query = f"(Id={id})"
    Count = 1
    Culture = "en-CA" 
    Format = "STANDARD-XML" 
    request_arguments = "?Format=" + Format + "&SearchType=" + SearchType + "&Class=" + Class + "&QueryType=" + QueryType + "&Query=" + Query + "&Count=" + str(Count) + "&Culture=" + Culture
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
            with open('specificId.xml', 'wb') as xmlfile:
                xmlfile.write(response.content)

            print("XML data saved to specificId.xml.")

            tree = ET.parse('specificId.xml')
            root = tree.getroot()

            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ddf'
            )
            cursor = db.cursor()

            for property_detail in root.findall('.//{urn:CREA.Search.Property}PropertyDetails'):
                update_database_row(property_detail, cursor)

            db.commit()
            cursor.close()
            db.close()

    except Exception as ex:
        print("Error:", ex)

def update_database_row(table_element, cursor):
    table_name = 'new_property_listings'

    data = {}
    for element in table_element.iter():
        if get_local_name(element.tag) == 'PropertyDetails':
            # Extract ID attribute from PropertyDetails element
            data['ID'] = element.get('ID').strip() if element.get('ID') else None
        else:
            data[get_local_name(element.tag)] = element.text.strip() if element.text else None

    data = {key: value[:255] if value and len(value) > 255 else value for key, value in data.items()}

    if 'ID' in data:
        placeholders = ', '.join(['%s'] * len(data))
        replace_query = f"REPLACE INTO `{table_name}` ({', '.join([f'`{column}`' for column in data.keys()])}) VALUES ({placeholders})"

        values = [data[column] for column in data]
        try:
            check_query = f"SELECT ID FROM `{table_name}` WHERE ID = %s"
            cursor.execute(check_query, (data['ID'],))
            existing_row = cursor.fetchone()

            if existing_row:
                update_query = f"UPDATE `{table_name}` SET {', '.join([f'`{column}`=%s' for column in data.keys()])} WHERE ID = %s"
                cursor.execute(update_query, values + [data['ID']])
                print(f"Row with ID {data['ID']} updated in {table_name} table.")
            else:
                cursor.execute(replace_query, values)
                print(f"Row with ID {data['ID']} inserted into {table_name} table.")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Warning: {e}")

    print(f"All available data processed for {table_name} table.")

def generate_nonce(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def delete_records_not_matching(xml_ids):
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='ddf'
    )

    cursor = db.cursor()
    
    query = "SELECT ID FROM new_property_listings"
    cursor.execute(query)
    results = cursor.fetchall()

    ids_in_database = set(row[0] for row in results)
    intersection_ids = ids_in_database.intersection(set(xml_ids))
    ids_to_delete = ids_in_database - intersection_ids

    # if ids_to_delete:
    #     delete_query = "DELETE FROM new_property_listings WHERE ID IN (%s)"
    #     placeholders = ', '.join(['%s'] * len(ids_to_delete))
    #     formatted_query = delete_query % placeholders
    #     cursor.execute(formatted_query, tuple(ids_to_delete))
    #     db.commit()
    #     print("Records deleted successfully.")
    # else:
    #     print("No records found for deletion.")
    
    # Extract ID-LastUpdated pairs from XML data
    # xml_property_updates = set()
    tree = ET.parse('all_ids.xml')
    root = tree.getroot()
    # for property_elem in root.findall('.//{urn:CREA.Search.Property}Property'):
    #     property_id = property_elem.attrib.get('ID')
    #     last_updated = property_elem.attrib.get('LastUpdated')
    #     if property_id and last_updated:
    #         xml_property_updates.add((property_id, last_updated))
    xml_property_updates = {
    '26471902': 'Thu, 08 Feb 2024 02:11:33 GMT',
    '25739646': 'Fri, 14 Jul 2023 20:51:14 GMT'
}
    
    different_last_updated_ids = check_different_last_updated(intersection_ids, xml_property_updates)
    print("IDs with different LastUpdated values:", different_last_updated_ids)

    cursor.close()
    db.close()
    return intersection_ids

def check_different_last_updated(intersection_ids, xml_property_updates):
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='ddf'
    )
    cursor = db.cursor()

    ids_with_different_last_updated = set()

    for id in intersection_ids:
        query = f"SELECT LastUpdated FROM new_property_listings WHERE ID = '{id}'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            db_last_updated = result[0]
            xml_last_updated = xml_property_updates.get(id)
            print(xml_last_updated)
            if xml_last_updated is not None and db_last_updated != xml_last_updated:
                ids_with_different_last_updated.add(id)

    cursor.close()
    db.close()
    for id in ids_with_different_last_updated:
        update_database_with_xml_data(id)     

    return ids_with_different_last_updated


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

        # print("Response status code:", response.status_code)

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
    table_name = 'new_property_listings'
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
    # print(create_table_query)
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully.")

def process_table(table_element, cursor):
    table_name = 'new_property_listings'

    data = {}
    for element in table_element.iter():
        if get_local_name(element.tag) == 'PropertyDetails':
            # Extract ID attribute from PropertyDetails element
            data['ID'] = element.get('ID').strip() if element.get('ID') else None
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
                # print(f"{cursor.rowcount} rows replaced in {table_name} table.")
            else:
                print("ID already exists. Skipping insertion.")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Warning: {e}")

    # print(f"All available data replaced in {table_name} table.")


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
Offset = 1 
Culture = "en-CA" 
Format = "STANDARD-XML" 
SearchTransaction(RetsUrl,str(SearchType), str(Class), str(QueryType),Query, Count=Count, Limit=str(Limit), Offset=Offset, Culture=str(Culture), Format=str(Format))
Compact_SearchTransaction()


tree = ET.parse('metadata.xml')
root = tree.getroot()
total_pages = root.find('.//{urn:CREA.Search.Property}TotalPages').text
total_pages= int(total_pages)
# def run_search_transactions(total_pages):
    
#     for i in range(1, total_pages + 1):
#         Offset = (i - 1) * 100 + 1
        
#         SearchTransaction(RetsUrl, str(SearchType), str(Class), str(QueryType), Query, Count=Count, Limit=str(Limit), Offset=Offset, Culture=str(Culture), Format=str(Format))

# run_search_transactions(total_pages)

def SearchTransactionAndCompare(RetsUrl, SearchType, Class, QueryType, Query, Count=1, Limit="100", Offset=1, Culture="en-CA", Format="STANDARD-XML"):
    request_arguments = "?Format=" + Format + "&SearchType=" + SearchType + "&Class=" + Class + "&QueryType=" + QueryType + "&Query=(ID=*)" + "&Count=" + str(Count) + "&Limit=" + str(Limit) + "&Offset=" + str(Offset) + "&Culture=" + Culture
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

        if response.status_code == 200:
            with open('all_ids.xml', 'wb') as xmlfile:
                xmlfile.write(response.content)

            print("XML data saved to metadata.xml.")

            tree = ET.parse('all_ids.xml')
            root = tree.getroot()
            xml_ids = set()
            for property_elem in root.findall('.//{urn:CREA.Search.Property}Property'):
                property_id = property_elem.attrib.get('ID')
                if property_id:
                    xml_ids.add(property_id)
            
            unmatched_ids = []
            # print("These are xml Ids: ",xml_ids)
            if delete_records_not_matching(xml_ids):
                unmatched_ids.append(xml_ids)
    
    except Exception as ex:
        print("Error:", ex)
    
    return unmatched_ids
    
unmatched_ids = SearchTransactionAndCompare(RetsUrl,str(SearchType), str(Class), str(QueryType),Query, Count=Count, Limit=str(Limit), Offset=Offset, Culture=str(Culture), Format=str(Format))
# print(unmatched_ids)


