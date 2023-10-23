import requests
import time 
import argparse
from config import NYT_API_KEY, NYT_ARTICLE_SEARCH_ENDPOINT, NYT_DATA_DIR, WAJD_API_KEY
from helpers import *

logger = setup_logger("nyt", "nyt.log")





def search_articles(query, start_date = "20230101", end_date = "20230131" , page = 1):
    params = {
        'q': query,
        'api-key': WAJD_API_KEY,
        'begin_date': start_date,
        'end_date': end_date,
        'page': page
    }


    response = requests.get(NYT_ARTICLE_SEARCH_ENDPOINT, params=params)

    if response.status_code != 200:
        logger.error(f"Error: {response.status_code}")
        logger.error(f"Error: {response.text}")
        return None
    
    logger.info(f"Success: {response.status_code}")

    return response, response.json()['response']['docs']



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q" ,help="search query")
    parser.add_argument("--start_date", help="start date", default="20231007")
    parser.add_argument("--end_date", help="end date", default="20231023")
    parser.add_argument("--page_range",nargs=2, help="page number", default=[1, 1])
    parser.add_argument("--keywords_file", help="file containing keywords to search", default=None)    



    args = parser.parse_args()

    query = args.q
    start_date = args.start_date
    end_date = args.end_date
    start_page, end_page = args.page_range
    keywords_file = args.keywords_file
    

    query = read_keywords_file(keywords_file, operator = "")     
    logger.info(f"Searching for articles with query: {query}")    
    for q in query:
        logger.info(f"Searching for articles with query: {q}")
        for page in range(int(start_page), int(end_page) + 1):
            logger.info(f"Searching for articles on page: {page}")
            response, articles = search_articles(q, start_date, end_date, page)
            payload = response.json()
            out_dir = build_payload_dir_name(NYT_DATA_DIR, query=q, start_date=start_date, end_date=end_date, page=page)
            save_payload_by_query_params(payload, out_dir)
            throt(10)

    







