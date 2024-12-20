import scrapy
from scrapy.crawler import CrawlerProcess
import networkx as nx
import matplotlib.pyplot as plt
import json
from webscraper.items import WebscraperItem

class NDBusinessSpider(scrapy.Spider):
    name = 'ndbusinesses'
    allowed_domains = ['firststop.sos.nd.gov']
    start_urls = ['https://firststop.sos.nd.gov/api/Records/businesssearch']
    
    def start_requests(self):
        payload = {
            "SEARCH_VALUE": "X",
            "STARTS_WITH_YN": True,
            "ACTIVE_ONLY_YN": True
        }
        
        yield scrapy.Request(
            self.start_urls[0],
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            body=json.dumps(payload),
            callback=self.parse_item
        )
    
    def parse_item(self, response):
        res = json.loads(response.body)
        rows = res.get("rows", {})
        
        # First yield the complete rows
        rows_item = WebscraperItem()
        rows_item['rows'] = rows
        yield rows_item
        
        # Process each business entry
        for key, value in rows.items():
            business_id = int(key)
            business_name = value.get("TITLE", [""])[0]
            
            # Make request for detailed business info
            business_url = f'https://firststop.sos.nd.gov/api/FilingDetail/business/{business_id}/false'
            yield scrapy.Request(
                business_url,
                callback=self.parse_business,
                meta={
                    'business_id': business_id,
                    'business_name': business_name,
                    'rows': rows
                },
                method='GET',
                headers={
                    'Accept': '*/*',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
                    'Authorization': 'undefined',
                    'Connection': 'keep-alive'
                }
            )

    def parse_business(self, response):
        business_id = response.meta.get('business_id')
        business_name = response.meta.get('business_name')
        res = json.loads(response.body)
        
        # Then process individual items
        relationship_types = ["Commercial Registered Agent", "Owner Name", "Owners", "Registered Agent"]
        
        for item in res.get("DRAWER_DETAIL_LIST", []):
            if item.get('LABEL') in relationship_types:
                # Yield individual parameters
                detail_item = WebscraperItem()
                detail_item['business_id'] = business_id
                detail_item['business_name'] = business_name
                detail_item['relationship_type'] = item['LABEL']
                detail_item['entity'] = item['VALUE'].split("\n")[0]
                yield detail_item