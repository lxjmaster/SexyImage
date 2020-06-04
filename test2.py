__AUTHOR__ = "Master_lxj"
__WEBSITE__ = "http://www.dagouzi.cn"
__DOC__ = "To do something"

import requests
from fake_useragent import UserAgent
from lxml import etree
import re
import time
import multiprocessing
import random

user_agent = UserAgent()


def fetch_html(url):
	time.sleep(random.random())
	headers = {
		"user-agent": user_agent.chrome
	}
	request = requests.get(url, headers=headers)
	response = request.content
	
	return response


def parse_html(response):
	html = etree.HTML(response)
	image_ele = html.xpath('//*[@id="container"]/ul/li')
	for image in image_ele:
		images = image.xpath('*/a/img')
		for img in images:
			image_url = img.get("src")
			# print(image_url)
			title = image_url.split("/")
			download_img(title[-1], image_url)
	more_images = html.xpath('//*[@id="data-more"]/text()')
	regex = r'"imgthumb":"(http://.*?)"'
	pattern = re.compile(regex)
	more_results = re.findall(pattern, more_images[0])
	for result in more_results:
		title = result.split("/")
		download_img(title[-1], result)


def download_img(image_title, image_url):
	time.sleep(random.random())
	print("正在下载：" + image_url)
	headers = {
		"user-agent": user_agent.chrome,
		"Upgrade-Insecure-Requests": "1",
		"Referer": "https://www.tooopen.com/img/88_879_1_10.aspx",
	}
	request = requests.get(image_url, headers=headers)
	response = request.content
	with open("images3/" + image_title, "wb+") as f:
		f.write(response)


def spider(page):

	# url = f"https://www.tooopen.com/img/88_878_1_{page}.aspx"
	url = f"https://www.tooopen.com/img/88_879_1_{page}.aspx"
	r = fetch_html(url)
	parse_html(r)


if __name__ == '__main__':
	# img_url = "http://img08.tooopen.com/20191128/tooopen_sl_091435143560802.jpg"
	pool = multiprocessing.Pool(processes=4)
	
	start = time.time()
	for page in range(1, 70):
		pool.apply_async(spider, args=(page,))
	
	pool.close()
	pool.join()
	print(time.time() - start)

	#4进程 59.23647117614746