from bs4 import BeautifulSoup
import requests, lxml, sys

class TorrBot:
    def __init__(self):
        self.url = "https://pirateproxy.gdn/search/{0}/0/99/0"

    def getUrl(self, name):
        self.url = self.url.format(name.replace(" ", "%20"))
        print(self.url)

    def query(self):
        website = requests.get(self.url)
        self.Soup = BeautifulSoup(website.content, 'lxml')

    def getMagnets(self):
        try:
            output = self.Soup.find_all("tr")
            output.pop(0)
            magnets = []
            for i in range(len(output)):
                x = (output[i].find_all('td'))
                title = x[1].div.a.getText()
                try:
                    magnet = (x[1].find_all('a', href=True))[1]
                    magnets.append({
                        'title': title,
                        'magnet': magnet['href']
                    })
                except Exception as e:
                    print(e)
            return magnets
        except Exception:
            print(Exception)
            return None
