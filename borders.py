#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup # beautifulsoup4==4.9.3
import urllib.request
import networkx as nx # networkx==2.6.2
from community import community_louvain # python-louvain==0.15


URL = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders"
with urllib.request.urlopen(URL) as source:
    soup = BeautifulSoup(source, "html.parser")

table = soup.find_all("table", {"class": "wikitable sortable"})[0]
tbody = table.find_all("tbody")[0]
trs = tbody.find_all("tr")

G = nx.Graph()

for row in trs[2:]:
    row = row.find_all('td')
    countryA = row[0].find_next("a").text.strip()
    try:
        length = float(row[1].text.replace(",",""))
    except:
        length = 0.0
    if countryA[0] != '[':
        G.add_node(countryA)
        G.nodes[countryA]["l"] = length

        countryB_list = [x.find_next("a").text for x in row[5].find_all('span', {'class': 'flagicon'})]

        if not countryB_list:
            continue
        for countryB in countryB_list:
            print(countryB)
            G.add_edge(countryA, str(countryB))

isolated_countries = list(nx.isolates(G))
G.remove_nodes_from(isolated_countries)
G.remove_nodes_from(["Palestine", "Antártica Chilena Province",
                     "West Bank", "Gaza Strip", "European Union"])

part = community_louvain.best_partition(G)
community_louvain.modularity(part, G)

with open("borders-1.graphml", "wb") as graph:
    nx.write_graphml(G, graph)
