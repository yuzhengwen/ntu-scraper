## Scraping
`scraping.py` -> To scrape mod data from ntu website and store it as local html files  
`scraping_exams.py` -> Scrape exam data  
`scraping_configs.py` -> Some shared configs for scraping  

## Parsing
`parser.py` -> Convert html files to python objects (dictionaries and lists), then save as JSON files  

## Data Upload
`db.py` -> Upload to MongoDB (localhosted) - need to change for prod server  
`blob_helper.py` -> Upload to Azure Blob Storage (Requires env variable for access string)  