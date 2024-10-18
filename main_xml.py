import os
import json
import xml.etree.ElementTree as ET
import logging
import sqlite3
from datetime import datetime

# Setup logging
logging.basicConfig(filename='process.log', level=logging.INFO, 
                    format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# SQLite Initialization
def init_db(db_name="orders.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS raw_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        xml_content TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS processed_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        json_content TEXT
    )''')
    
    conn.commit()
    return conn

# Store raw XML data in the raw_data table
def store_raw_data(conn, filename, xml_content):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO raw_data (filename, xml_content) 
    VALUES (?, ?)''', (filename, xml_content))
    conn.commit()

# Store processed JSON data in the processed_data table
def store_processed_data(conn, filename, json_content):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO processed_data (filename, json_content) 
    VALUES (?, ?)''', (filename, json_content))
    conn.commit()

#extracting xml data and converting into json
def xml_to_json(xml_file, retries=3):
    for attempt in range(1, retries + 1):  #for retries data 
        try:
            # Parse the XML file
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Extracting data order_ID, Customer and Products
            order_data = {
                "OrderID": root.find('OrderID').text,
                "Customer": {
                    "CustomerID": root.find('Customer/CustomerID').text,
                    "Name": root.find('Customer/Name').text
                },
                "Products": []
            }

            # Loop through all products
            for product in root.findall('Products/Product'):
                product_data = {
                    "ProductID": product.find('ProductID').text,
                    "Name": product.find('Name').text,
                    "Quantity": product.find('Quantity').text,
                    "Price": product.find('Price').text
                }
                order_data["Products"].append(product_data)

            # Convert to JSON
            json_data = json.dumps(order_data, indent=4)
            return json_data

        except ET.ParseError as e:           #for errors like unclosed tags, invalid charaters and other syntax error
            logging.error(f"Parsing error in {xml_file} - {e}")
        except AttributeError as e:
            logging.error(f"Missing element in {xml_file} - {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred with {xml_file} - {e}")
    
        finally:
            # This block will always run, regardless of errors
            print(f"Processing of file {xml_file} completed.")

        if attempt == retries:
            logging.error(f"Failed to process {xml_file} after {retries} attempts.")    

    return None

def process_files():
    conn = init_db()  # Initialize the database connection
    #variable for file path
    xml_folder = 'C:\\Users\\sandh\\OneDrive\\Desktop\\VS Code\\python\\H2N_DEV_Interview\\xml-files-base'
    output_folder = './json-output/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_folder, xml_file)
            logging.info(f"Processing {xml_file}")

            # Store raw XML in the database
            with open(xml_path, 'r') as file:
                xml_content = file.read()
                store_raw_data(conn, xml_file, xml_content)

            json_data = xml_to_json(xml_path)
            if json_data:
                output_file = os.path.join(output_folder, xml_file.replace('.xml', '.json'))
                with open(output_file, 'w') as f:
                    f.write(json_data)

                 # Store processed JSON in the database
                store_processed_data(conn, xml_file, output_file)    
                logging.info(f"Processed {xml_file} successfully.")
            else:
                logging.warning(f"Skipping {xml_file} due to errors.")

    conn.close()  # Close the database connection when processing is done        

if __name__ == "__main__":
    process_files()
