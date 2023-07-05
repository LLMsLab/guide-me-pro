#import libraries
import os
import web_scraper as ws

#set parameters
nyl_pub_site_map = "https://www.newyorklife.com/sitemap.xml"
scraper = ws.WebScraper()
urls = scraper.get_urls_in_sitemap(nyl_pub_site_map)

#explore object urls 
print("number of pages is:")
print(len(urls))
print("first few pages are:")
print(urls[:4])
print("last few pages are:")
print(urls[-4:])

#scrape from NYL pub website
scraper.save_to_files(urls)