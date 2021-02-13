import requests
page = requests.get("https://www.nytimes.com/interactive/2020/us/california-coronavirus-cases.html?")
page.content

from bs4 import BeautifulSoup as bs, SoupStrainer
soup = bs(page.content, 'html.parser')
#new thing
#print(soup.prettify())
#print(soup.find_all("h2",class_="card-title h3 mb-2 text-left"))
##print(soup.find_all("h3",class_="card-title h3 mb-2 text-left"))
#print(soup.find_all("h3"))
#print(soup.find_all("strong"))
#nocorona = soup.select("CDC")
#print(soup.find_all("h2",class_="card-title h3 mb-2 text-left")[0])

f = open("data.txt", "a")
# page1.content
#print(soup1.prettify())
data = []
import pandas as pd
for state in ["alabama", "alaska", "arizona", "arkansas", "california","colorado", "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois","indiana","iowa","kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts","michigan","minnesota","mississippi","missouri","montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon","pennsylvania", "rhode island", "south carolina", "south dakota","tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia", "wisconsin", "wyoming"]:
  url = f"https://www.nytimes.com/interactive/2020/us/{state.replace(' ', '-')}-coronavirus-cases.html"
  session = requests.Session()
  response = session.get(url)
  strainer = SoupStrainer("tbody", attrs={"class": "svelte-fin3s2"})
  soup = bs(response.content, features="html.parser", parse_only=strainer)
  counts = soup.find_all("span", attrs={"class": "svelte-fin3s2"})
  soup1 = bs(response.text, 'html5lib')
  f.write(state)
  f.write("\n")
  table = soup1.find_all('table', attrs={"class": "svelte-1a4y62p"})               #finds all tables
  table_top = pd.read_html(str(table))[0]      #the top table        
  result = pd.concat([table_top])
  data.append(result)
  for i in counts:
    f.write(i.text)
    f.write("\n")
    f.write("\n====\n")
pd.concat(data).to_csv('test.csv')
f.close()
page1 = requests.get("https://www.nytimes.com/interactive/2020/us/california-coronavirus-cases.html?#county")
# page1.content
soup1 = bs(page1.text, 'html5lib')
#print(soup1.prettify())
import pandas as pd
print(soup1.find_all('table', attrs={"class": "svelte-1a4y62p"})[0])
page2 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html")
soup2 = bs(page2.text, 'html5lib')
#3 tips -> li
page3 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html")
soup3 = bs(page3.text, 'html5lib')
print(soup3.find_all("li"))
