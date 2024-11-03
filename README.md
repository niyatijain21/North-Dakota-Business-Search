# North-Dakota-Business-Search

-  Inspected the data source ~https://firststop.sos.nd.gov/search/business Developer Tools
   API endpoints for Business Search (POST) and Business Details (GET) respectively.
-  These endpoints were used to extract active companies (id, name, relationships data) that start with "X". The data was crawled using a spider from the Scrapy Library provided by python for web scraping tasks. The extracted data was stored in NDbusinessdata.json.
-  The items that were yeilded were maintained and a pipeline tasks with some cleaning steps was implemented.
-  A graph was constructed depicting the relationships between the companies based on the labels - Commercial Registered Agent, Owner Name, Owners, Registered Agent. A graph library called NetworkX along with matplotlib was used for the same. The graph is stored as finalplot.png.

**Takeaways:**
- There were 203 companies(rows) extracted with 20 companies that do not start with 'X'. I've identified this data quality aspect and am implementing additional filtering in the processing pipeline to ensure we focus specifically on X-prefixed companies.
- The graph reveals a hierarchical business registration structure in North Dakota where most X-named companies (shown as paired nodes) have single-point relationships with registered agents or owners, while a few prominent registered agents (shown as hub structures with multiple spokes) serve as central points managing multiple businesses, suggesting a concentration of business registration services among a few key agents in the state.
