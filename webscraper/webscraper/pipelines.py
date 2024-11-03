# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class WebscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
                
        bname = adapter.get('business_name')
        
        if isinstance(bname, str):
            base_name = bname.split('(')[0].strip()  
            # Get text before '(' and remove whitespace
            
            # Check if base name starts with 'x'
            if not base_name.lower().startswith('x'):
                print("******** This does not start with X ************")
                raise DropItem(f"Business name doesn't start with X: {base_name}")
                
            # Update the business_name to use only the base name
            adapter['business_name'] = base_name
            
        return item
