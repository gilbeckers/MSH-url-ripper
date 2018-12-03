import urllib.request as urllib2
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://my-smarthome.be/product.html?id="


def scrap_link(input_link):
    #Opening site using urllib2
    html_page = html_page = urllib2.urlopen(input_link)
    soup = BeautifulSoup(str(html_page.read()), 'html.parser')

    for link in soup.findAll('a', {'class': 'crumb'}):
        try:
            #print(link['href'])
            return link['href']
        except KeyError as e:
            print("Key error in html parsing ({0}): {1}".format(e.errno, e.strerror))
            print(html_page.url)
            #pass
            raise



df = pd.read_csv('Velbus producten_shopping.csv')
id_columns = df['Internal_Variant_ID'] #df.column_name #you can also use df['column_name']

# Add new column
df["scrapped_link"] = "not_scrapped_yet"

for (row_index, the_id) in enumerate(id_columns):
    actual_id = the_id.split(":")[1]
    scrapped_link = "scrapping_failed"
    try:
        scrapped_link = scrap_link(base_url+actual_id)
        print(str(row_index) + ": " + scrapped_link)
    except KeyError:
        pass

    #Update column
    df.set_value(row_index, 'scrapped_link', scrapped_link)


# Write to new csv file
df.to_csv("result.csv")




# end
