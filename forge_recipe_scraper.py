from bs4 import BeautifulSoup
import requests

forge_page = requests.get('https://wiki.hypixel.net/The_Forge').content
print('\n'*40)
soup = BeautifulSoup(forge_page, 'html.parser')
soup_tables = soup.find_all("table", class_="wikitable")
list_of_tables = []
for i in soup_tables:
    list_of_tables.append(i)

list_of_sub_tables = []
for i in list_of_tables:
    list_of_sub_tables.append(i.find_all("tr", class_=""))

for i in list_of_sub_tables:
    i.pop(0)
    i.pop(0)
    for j in i:
        print(j.find_all('td', class_="")[0].prettify())
#print(list_of_sub_tables[0][0].prettify())
