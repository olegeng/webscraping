import glob, lxml
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

data_path = './data/'
logfile = 'logfile.txt'

def logging(message, t_format = '%Y-%h-%d-%H:%M:%S'):
    now = datetime.now()
    timestamp = now.strftime(t_format)
    with open(logfile, 'a') as f:
        f.write(f'{timestamp} --- {message}\n')

logging("ETL Job Started")

def extract_from_csv(path_to_file):
    """"Extracts and return data from CSV files"""
    dataframe = pd.read_csv(path_to_file)
    logging('Extracting from CSV file - Successful')
    return dataframe

def extract_from_json(path_to_file):
    """"Extracts and return data from JSON files"""
    dataframe = pd.read_json(path_to_file, lines=True)
    logging('Extracting from JSON file - Successful')
    return dataframe

def extract_from_xml(path_to_file):
    """"Extracts and return data from XML files"""
    dataframe = pd.read_xml(path_to_file)
    logging('Extracting from XML file - Successful')
    return dataframe

def extract():
    """"Extracts all data from every file by using previous func"""
    logging("Extract phase Started")
    extracted_data = pd.DataFrame(columns = ['car_model','year_of_manufacture','price','fuel'])
    for file in glob.glob('./data/*csv'):
        extracted_csv = extract_from_csv(file)
        extracted_data = extracted_data._append(extracted_csv, ignore_index=True)
    for file in glob.glob('./data/*json'):
        extracted_json = extract_from_json(file)
        extracted_data = extracted_data._append(extracted_json, ignore_index=True)
    for file in glob.glob('./data/*xml'):
        extracted_xml = extract_from_xml(file)
        extracted_data = extracted_data._append(extracted_xml, ignore_index=True)
    logging("Extract phase Ended")
    return extracted_data

def transform(data):
    logging("Transform phase Started")
    petrol_rows = data[data['fuel'] == 'Petrol']
    data.loc[petrol_rows.index, 'price'] += 1000
    data['price'] = round(data['price'], 2)
    logging("Transform phase Ended")
    return data

def load_to_csv(data):
    logging("Load phase Started")
    data.to_csv('cars.csv')
    logging("Load phase Ended")

data = extract()
data=(transform(data))
load_to_csv(data)
logging("ETL Job Ended\n---------------------------------------------")