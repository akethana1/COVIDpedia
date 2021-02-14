from bs4 import BeautifulSoup as bs, SoupStrainer as ss
import requests
import pandas as pd
from datetime import timedelta
from os import path
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
Session(app)

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa","Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

@app.before_first_request
def setup():
	if "state_data" not in session:
		session["state_data"] = state_data(states)
		county_data(states)

	return session["state_data"]

def state_data(s):
	data = [{"state": _} for _ in s]

	territories = ["american samoa", "district of columbia", "guam", "marshall islands", "micronesia", "northern mariana islands", "palau", "puerto rico", "u.s. virgin islands"]
	unitedstates = s + territories

	page3 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/vaccines/index.html")
	soup3 = bs(page3.content, 'html.parser')
	soup3.find_all('a', attrs={"class":"dropdown-item noLinking"})
	links = []

	for link in soup3.find_all('a', attrs={"class":"dropdown-item noLinking"}, href=True):
		links.append(link['href'])
		statelinks = dict(zip(unitedstates, links))
	for territory in territories:
		del statelinks[territory]

	for state in s:
		url = f"https://www.nytimes.com/interactive/2020/us/{state.replace(' ', '-').lower()}-coronavirus-cases.html"
		req = requests.Session()
		response = req.get(url)
		strainer = ss("td", attrs={"class": "num yesterday svelte-fin3s2"})
		soup = bs(response.content, features="html.parser", parse_only=strainer)
		counts = soup.find_all("span", attrs={"class": "svelte-fin3s2"})

		strainer = ss("tr", attrs={"class": "svelte-fin3s2"})
		soup = bs(response.content, features="html.parser", parse_only=strainer)
		yesterday = str(soup.find_all("th", attrs={"class": "header yesterday svelte-fin3s2"})[0].text).split("On ")[1]

		data[s.index(state)]["link"] = statelinks[state]
		data[s.index(state)]["cases"] = counts[0].text
		data[s.index(state)]["deaths"] = counts[1].text
		data[s.index(state)]["hospitalized"] = counts[2].text
	return data, yesterday

def county_data(s):
	if "state_data" not in session or not path.exists("templates/county.html"):
		data = []

		for state in s:
			url = f"https://www.nytimes.com/interactive/2020/us/{state.replace(' ', '-').lower()}-coronavirus-cases.html"
			req = requests.Session()
			response = req.get(url)
			soup1 = bs(response.text, 'html5lib')
			table = soup1.find_all('table',
			attrs={"class": "svelte-1a4y62p"})
			table_top = pd.read_html(str(table))[0]
			result = pd.concat([table_top])
			data.append(result)

		datacolumns=data[0].columns
		for i in range(50):
			data[i] = data[i].rename(columns={
			"Unnamed: 0": "State / County",
			"Totalcases": "Total Cases",
			"Totaldeaths": "Total Deaths",
			"Per 100,000": "Cases Per 100K",
			"Per 100,000.1": "Deaths Per 100K",
			"Daily avg.in last7 days": "Average Daily Cases - Last 7 Days",
			"Per 100,000.2": "Average Daily Cases Per 100K - Last 7 Days",
			"Daily avg.in last7 days.1": "Average Daily Deaths - Last 7 Days",
			"Per 100,000.3": "Average Daily Deaths Per 100K - Last 7 Days"
			})
			data[i] = data[i].drop(datacolumns[-1], axis=1)

		countyfile = open("templates/county.html", "w")
		countyfile.close()
		countyfile = open("templates/county.html", "a")
		countyfile.write('{% extends "layout.html" %} {% block title %} County Statistics {% endblock %} {% block main %}')

		for i in data:
			datahtml = i.to_html()
			countyfile.write(datahtml)

		countyfile.write('{% endblock %}')
		countyfile.close()

def safety_info():
	page2 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html")
	soup = bs(page2.content, 'html.parser')
	cdc = [i.get_text() for i in soup.find_all("h2") + soup.find_all("h3")][:-2]
	return cdc

@app.route("/all-states")
def index():
	data, yesterday = setup()
	return render_template("index.html", data={"counts": data, "all_states": states, "yesterday": yesterday})

@app.route("/state", methods=["POST"])
def getstate():
	selectedstate = request.form.get("stateselector").replace(' ', '-').lower()
	return redirect(url_for("countsbystate", state=selectedstate))

@app.route("/state/<state>", methods=["GET", "POST"])
def countsbystate(state):
	if state == "all":
		return redirect(url_for("index"))
	else:
		data, yesterday = setup()
		return render_template("index.html", data={"counts": [data[states.index(state.replace("-", " ").title())]], "all_states": states, "yesterday": yesterday})

@app.route("/safety-tips")
def safety():
	return render_template("safety.html", tips=safety_info())

@app.route("/county")
def displaycounty():
	county_data(states)
	return render_template("county.html")

@app.route("/")
def home():
	return redirect(url_for("index.html"))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
