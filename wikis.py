from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import argparse

class WikiScraper(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def scrape(self, core = "Apple"):
        url = "https://en.wikipedia.org/wiki/{}".format(core.replace(' ', '_'))
        print("Walking through " + url)
        self.driver.get(url)
        err_locs = self.driver.find_elements_by_class_name("mbox-text")
        for loc in err_locs:
            if "Wikipedia does not have an article with this exact name" in loc.text:
                print("Article with name '{}' does not exist...".format(core))
                exit()

        body = self.driver.find_element_by_id("bodyContent")
        hrefs = body.find_elements_by_xpath("//a[@href]")
        num_articles = len(hrefs)

        link = hrefs[random.randint(0, num_articles)].get_attribute("href")
		
        while not ("https://en.wikipedia.org/wiki" in link and\
                   "talk" not in link.lower() and\
                   "main" not in link.lower() and\
                   ":" not in link[9:] and\
                   "?" not in link and\
                   "#" not in link):
   
                   link = hrefs[random.randint(0, num_articles)].get_attribute("href")

        return link.replace("https://en.wikipedia.org/wiki/", "")

def main():
   
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--article", help="The base article", default="Apple")
    parser.add_argument("-i", "--iterations", help="The number of articles to parse", default=3)
    parser.add_argument("-d", "--delay", help="The number of seconds to wait before"
                                              "opening another article", type=float, default=0)	

    args = parser.parse_args()

    scraper = WikiScraper()
    print("Clearing previous wikis file")
    with open("wikis.txt", "w+") as file:
        file.write(args.article + "\n")

    next_article = scraper.scrape(args.article)

    for i in range(int(args.iterations)):    
        with open("wikis.txt", "a+") as file:
            file.write(next_article + "\n")

        next_article = scraper.scrape(next_article)
        sleep(args.delay)

    input("Please press enter when you're done reading your article")
    print("The steps required to get here are contained in wikis.txt")

if __name__ == '__main__':
    main()
