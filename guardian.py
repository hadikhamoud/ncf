import requests
import argparse
import os
import json
from helpers import *
from config import GURADIAN_API_KEY, GURADIAN_DATA_DIR, GURADIAN_ENDPOINT


logger = setup_logger("guardian", "guardian.log")



def get_articles(query, page_size=10, order_by="relevance", show_fields="all", page=1, from_date = "2023-10-07", to_date = "2023-10-23"):
    payload = {
        "api-key": GURADIAN_API_KEY,
        "q": query,
        "show-fields": show_fields,
        "page-size": page_size,
        # "order-by": order_by,
        "page": page,
        "from-date": from_date,
        "to-date": to_date
    }
    response = requests.get(GURADIAN_ENDPOINT, params=payload)
    if response.status_code != 200:
        logger.error(f"Error: {response.status_code}")
        return None
    
    logger.info(f"Success: {response.status_code}")

    return response, response.json()["response"]["results"]




def save_articles(articles, out_dir):
    #save articles to out_dir
    logger.info("Saving articles to: ", out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for article in articles:
        filename = article["id"] + ".txt"
        filename = filename.replace("/", "--")

        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w") as f:
            f.write(article["fields"]["bodyText"])
    
    logger.info("Saved articles to: ", out_dir)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", nargs="+", help="search query (accepts multiple values)")
    parser.add_argument("--keywords_file", help="file containing keywords to search", default=None)
    parser.add_argument("--page_size", type=int, help="number of articles to return", default=10)
    parser.add_argument("--page_range", type=int, nargs=2, help="range of pages to search (start end)", default=[1, 1])
    parser.add_argument("--order_by", help="order by relevance or newest", default="relevance")
    parser.add_argument("--show_fields", help="show fields", default="all")
    parser.add_argument("--from-date", help="page number", default=1)
    parser.add_argument("--to-date", help="page number", default=1)

    args = parser.parse_args()

    queries = args.q
    keywords_file = args.keywords_file
    page_size = args.page_size
    order_by = args.order_by
    show_fields = args.show_fields
    start_page, end_page = args.page_range

    if queries is None and keywords_file is None:
        raise Exception("Either --q or --keywords_file must be specified")
    
    if queries is None:
        queries = read_keywords_file(keywords_file, "|")
        logger.info(queries)
        queries = [queries]
    

    for query in queries:
        logger.info(f"Query: {query}")
        for page in range(start_page, end_page + 1):
            logger.info(f"page: {page}")
            payload_dir_name = build_payload_dir_name(
                # Assuming GURADIAN_DATA_DIR is defined elsewhere
                GURADIAN_DATA_DIR, 
                q=query, page_size=page_size, 
                order_by=order_by, show_fields=show_fields, 
                page=page
            )
            logger.info(f"Query: {query}")
            logger.info(f"Page size: {page_size}")
            logger.info(f"Order by: {order_by}")
            logger.info(f"Show fields: {show_fields}")
            logger.info(f"Page: {page}")
            logger.info(f"Payload dir name: {payload_dir_name}")

            response, articles = get_articles(query, page_size, order_by, show_fields, page)
            payload = response.json()
            save_payload_by_query_params(payload, payload_dir_name)
            logger.info(f"Saved payload to: {payload_dir_name}")

    
    






