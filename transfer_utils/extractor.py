import pandas as pd
from datetime import datetime
from logger import *


class DataExtractor():
    
    def __init__(self)->None:
        try:
            self.logger=Logger().get_app_logger()
            self.logger.info('Data extractor object Initialized')
        except:
            pass

    def get_columns_and_rows(self, file_path):
        try:
            with open(f'../data/SFTP/{file_path}', 'r') as f:
                lines = f.readlines()

            columns = lines[0].replace('\n', '').split(',')
            columns = [col.strip() for col in columns]
            data = [line.replace('\n', '').split(',') for line in lines[2:]]

            # Apply formatting for loaded_at column
            loaded_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            columns.append('loaded_at')
            for row in data:
                row.append(loaded_at)

            # Apply formatting for ENTRYDATE column
            entrydate_index = columns.index('ENTRYDATE')
            for row in data:
                entrydate = row[entrydate_index]
                formatted_entrydate = datetime.strptime(entrydate, '%m/%d/%Y').strftime('%m-%d-%Y')
                row[entrydate_index] = formatted_entrydate
            # Change column name from "CityName" to "City"
            if 'CityName' in columns:
                city_index = columns.index('CityName')
                columns[city_index] = 'CITY'
            return columns, data
        except Exception as e:
            try:
                self.logger.error(f"Failed to read data: {e}")
            except:
                pass
            return (), ()

    def prepare_data_frame(self,sftp_data:tuple):

        try:
            sftp_cols,sftp_rows=sftp_data
            sftp_data=pd.DataFrame(columns=sftp_cols,data=sftp_rows)

            return sftp_data

        except Exception as e:
            # the try excepts here are for the airflow
            try:
                self.logger.error(f"Failed to prepare data frame: {e}")
            except:
                pass

    def extract_data(self,file_name:str,return_json=False)->pd.DataFrame:
        try:
            columns,all_data=self.get_columns_and_rows(file_path=file_name)
            sftp_data = columns, all_data
            if not return_json:
                return self.prepare_data_frame(sftp_data)
            sf= self.prepare_data_frame(sftp_data)
            sf_file_name= str(datetime.today()).replace(' ','_')+"_leads_sftp.json"


            sf.to_json(f'../data/temp_files/{sf_file_name}',orient='records')

            return sf_file_name
        except Exception as e:
            print(e)
            try:
                self.logger.error(f"Failed to extract data: {e}")
            except:
                pass