# coding:utf-8

import datetime
import codecs
import requests
from pyquery import PyQuery as pq


def git_add_commit_push():
	pass

def createMarkdown(date, filename):
	with open(filename,'w') as f:
		f.write("###" + date + "\n")

def scrape(language, filename): 

	HEADERS = {
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'
	    , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	    , 'Accept-Encoding': 'gzip,deflate,sdch'
	    , 'Accept-Language': 'zh-CN,zh;q=0.8'
	}

	url = 'https://github.com/trending?l={language}'.format(language=language)
	r = requests.get(url, headers = HEADERS)
	assert r.status_code == 200

	print r.encoding


	d = pq(r.content)
	items= d('li.repo-list-item')

	# codecs to solve the problem utf-8 codec like chinese
	with codecs.open(filename, "a", "utf-8") as f:
		f.write('\n####{language}\n'.format(language=language))

		for item in items:
			i = pq(item)
			title = i("h3 a").text()
			owner = i("span.prefix").text()
			description = i("p.repo-list-description").text()
			url = i("h3 a").attr("href")
			url = "https://github.com" + url
			ownerImg = i("p.repo-list-meta a img").attr("src")

			print title, owner, description, url, ownerImg
			f.write("* <img src='" + ownerImg + "' height='20' width='20'>[" + title + "](" + url + "): " + description + "\n")


def main():
	
	strdate = datetime.datetime.now().strftime('%Y-%m-%d')
	filename = '{date}.md'.format(date = strdate)
	
	#create markdown file
	createMarkdown(strdate, filename)

	#TODO: use goroutinez
	scrape('python', filename)
	scrape('java', filename)
	
	#git add commit push
	git_add_commit_push()


if __name__ == '__main__':
	main()

