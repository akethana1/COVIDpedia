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
data = []#county data
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
for i in range(50):#rename columns for county data
    data[i]=data[i].rename(columns={"Unnamed: 0": "State+County", "Per 100,000":"Cases Per 100,000",
                       "Per 100,000.1":"Deaths Per 100,000",
                       "Daily avg.in last7 days":"Daily avg. Cases in last 7 days",
                       "Per 100,000.2":"Daily avg. Cases in last 7 days per 100,000",
                       "Daily avg.in last7 days.1":"Daily avg. Deaths in last 7 days",
                       "Per 100,000.3":"Daily avg. Deaths in last 7 days per 100,000"})
    data[i]=data[i].drop(["Weekly cases per capita Fewer More"],axis=1)

f.close()
page1 = requests.get("https://www.nytimes.com/interactive/2020/us/california-coronavirus-cases.html?#county")
# page1.content
soup1 = bs(page1.text, 'html5lib')
#print(soup1.prettify())
import pandas as pd
#3 CDC COVID Guidelines
#3 CDC COVID Guidelines
page2 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html")
soup2 = bs(page2.content, 'html.parser')
rules = [i.get_text() for i in soup2.find_all("h2") + soup2.find_all("h3")][:-2]

cdc = [i.get_text() for i in rules]

for i in cdc:
	print(i)
#4 vaccine information
page3 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/vaccines/index.html")
soup3 = bs(page3.content, 'html.parser')
soup3.find_all('a',attrs={"class":"dropdown-item noLinking"})
print(soup3.find_all('a',attrs={"class":"dropdown-item noLinking"}))
links=[]
states=[
        "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
        "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
        "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
        "maine", "maryland", "massachusetts", "michigan", "minnesota",
        "sippi", "missouri", "montana", "nebraska", "nevada",
        "new hampshire", "new jersey", "new mexico", "new york",
        "north carolina", "north dakota", "ohio", "oklahoma", "oregon",
        "pennsylvania", "rhode island", "south carolina", "south dakota",
        "tennessee", "texas", "utah", "vermont", "virginia", "washington",
        "west virginia", "wisconsin", "wyoming"]
for i in range(len(soup3.find_all('a',attrs={"class":"dropdown-item noLinking"}))):
  print(print(soup3.find_all('a',attrs={"class":"dropdown-item noLinking"})[i].get_text()))
for link in soup3.find_all('a',attrs={"class":"dropdown-item noLinking"}, href=True):
    links.append(link['href'])
print(states)
print(links)



