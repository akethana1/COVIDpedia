from bs4 import BeautifulSoup as bs, SoupStrainer as ss
import requests
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana","Iowa","Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island","South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

def state_data(s):
	data = [{"state": _} for _ in s]

	for state in s:
		url = f"https://www.nytimes.com/interactive/2020/us/{state.replace(' ', '-').lower()}-coronavirus-cases.html"
		session = requests.Session()
		response = session.get(url)
		strainer = ss("td", attrs={"class": "num yesterday svelte-fin3s2"})
		soup = bs(response.content, features="html.parser", parse_only=strainer)
		counts = soup.find_all("span", attrs={"class": "svelte-fin3s2"})

		strainer = ss("tr", attrs={"class": "svelte-fin3s2"})
		soup = bs(response.content, features="html.parser", parse_only=strainer)
		yesterday = str(soup.find_all("th", attrs={"class": "header yesterday svelte-fin3s2"})[0].text).split("On ")[1]

		data[s.index(state)]["cases"] = counts[0].text
		data[s.index(state)]["deaths"] = counts[1].text
		data[s.index(state)]["hospitalized"] = counts[2].text
	return data, yesterday

# def county_data(s):
# 	soup1 = bs(response.text, 'html5lib')
# 	table = soup1.find_all('table', attrs={"class": "svelte-1a4y62p"})
# 	table_top = pd.read_html(str(table))[0]
# 	result = pd.concat([table_top])
# 	data.append(result)
# 	for i in counts:
# 	f.write(i.text)
# 	f.write("\n")
# 	f.write("\n====\n")
# 	for i in range(50):#rename columns for county data
# 	data[i]=data[i].rename(columns={"Unnamed: 0": "State+County", "Per 100,000":"Cases Per 100,000",
# 	"Per 100,000.1":"Deaths Per 100,000",
# 	"Daily avg.in last7 days":"Daily avg. Cases in last 7 days",
# 	"Per 100,000.2":"Daily avg. Cases in last 7 days per 100,000",
# 	"Daily avg.in last7 days.1":"Daily avg. Deaths in last 7 days",
# 	"Per 100,000.3":"Daily avg. Deaths in last 7 days per 100,000"})
# 	data[i]=data[i].drop(["Weekly cases per capita Fewer More"],axis=1)

# def vaccine_info(s):
# 	page3 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/vaccines/index.html")
# 	soup = bs(page3.content, 'html.parser')
# 	# print(soup.find_all("li"))
# 	cdc = []
# 	for i in range(67,115):
# 	cdc.append(soup.find_all("a",class_="dropdown-item noLinking")[i].get_text())
# 	print(soup.find_all("li")[i].get_text()+" "+str(i))
# 	print(cdc)

@app.route("/all-states")
def index():
	data, yesterday = state_data(states)
	return render_template("index.html", data={"counts": data, "all_states": states, "yesterday": yesterday})

@app.route("/state", methods=["POST"])
def getstate():
	selectedstate = request.form.get("stateselector")
	return redirect(url_for("countsbystate", state=selectedstate))

@app.route("/state/<state>", methods=["GET", "POST"])
def countsbystate(state):
	if state == "all":
		return redirect(url_for("index"))
	else:
		data, yesterday = state_data(states)
		return render_template("index.html", data={"counts": [data[states.index(state)]], "all_states": states, "yesterday": yesterday})

# repl.it needs these two lines to run flask, but it's not necessary on any other IDE
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
