import re
import time
import requests
from urllib import parse
from bs4 import BeautifulSoup

def search(query, noOfPages):
	pages = noOfPages
	start = 0
	results = []
	for i in range(pages):
		search_term = query
		response = requests.get("http://www.google.com/search?q=" + search_term +"&start=" + str(start)).content
		print(response)
		soup = BeautifulSoup(response, "lxml")
		mydivs = soup.find_all("h3", attrs={'class' : 'r'})
		length_of_results = len(mydivs)
		if start == 0:
			start = length_of_results + 1
		else:
			start = start + length_of_results + 1
		for i in mydivs:
			try:
				div = str(i.a['href'])
				text = i.text
				inner = []
				div = re.search('url\?q=(.*)&sa=', div)
				div = div.group(1)
				url = parse.unquote(div)
				inner.append(text)
				inner.append(url)
				results.append(inner)
			except:
				print("Error parsing url")
	return results


print(search("what is python",5))
