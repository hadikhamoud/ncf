import requests
import time 
import argparse
from config import NYT_API_KEY, NYT_ARTICLE_SEARCH_ENDPOINT, NYT_DATA_DIR
from helpers import *

logger = setup_logger("nyt", "nyt.log")





def search_articles(query, start_date = "20230101", end_date = "20230131" , page = 1):
    params = {
        'q': query,
        'api-key': NYT_API_KEY,
        'begin_date': start_date,
        'end_date': end_date,
        'page': page
    }




    response = requests.get(NYT_ARTICLE_SEARCH_ENDPOINT, params=params)

    if response.status_code != 200:
        logger.error(f"Error: {response.status_code}")
        return None
    
    logger.info(f"Success: {response.status_code}")

    return response, response.json()['response']['docs']



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", required=True ,help="search query")
    parser.add_argument("--start_date", help="start date", default="20231007")
    parser.add_argument("--end_date", help="end date", default="20231023")
    parser.add_argument("--page", help="page number", default=1)

    args = parser.parse_args()

    query = args.q
    start_date = args.start_date
    end_date = args.end_date
    page = args.page


    response, articles = search_articles(query, start_date, end_date, page)

    payload = response.json()

    out_dir = build_payload_dir_name(NYT_DATA_DIR, query=query, start_date=start_date, end_date=end_date, page=page)

    save_payload_by_query_params(payload, out_dir)







