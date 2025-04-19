from scraping import fetch_data
from parser import parse_data
from blob_helper import BlobHelper
from dotenv import load_dotenv
import os

load_dotenv()
connect_str = os.getenv('CONNECTION_STR')
blob_helper = BlobHelper(connect_str)
raw_data_path = "raw/2025S1/data.html"
save_folder = "data/2025S1"

academic_year = "2025"
semester = "1"

fetch_data(academic_year, semester, raw_data_path)
parse_data(raw_data_path, save_folder)
blob_helper.upload_folder(save_folder, "2025S1")