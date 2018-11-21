
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError

import LogUtil
import RedisUtil
import MongoUtil


class Crawler():

    DEFULAT_URL = 'https://search.51job.com/list/040000,000000,0000,00,9,99,java,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

    def __init__(self,url=DEFULAT_URL):
        self.url = url
        self.total = 0
        self.start = time.time()
        self.log = LogUtil.LogUtil.get_logger()
        self.redis = RedisUtil.RedisUtil.getRedis()
        self.col = MongoUtil.MongoUtil.getCollection('crawler','Job')
        self.s_key = 'urls'

    def get(self,url):
        text = None
        try:
            r = requests.get(url)
            r.encoding = 'GBK'
            text = r.text
        except Exception as result:
            self.log.warn('目标网站链接超时,10秒后重连 e|%s',result)
            time.sleep(10)
            self.get(url)
        return text

    def parse_list_page(self,list_page):
        soup = BeautifulSoup(list_page, "html5lib")
        urls = []
        for tag in soup.select("p[class='t1 ']"):
            href = tag.select_one('a[onmousedown]')['href']
            self.redis.sadd(self.s_key, href)
            urls.append(href)
        _next = ''
        lis = soup.select("li[class='bk']")

        for li in lis:
            if('下一页'==li.text):
                _next = li.select_one('a[href]')['href']
                # print(_next)
        return urls,_next

    def catch(self,target):
        page = self.get(target)
        r = self.parse_list_page(page)
        for l in r[0]:
            self.total += 1
            if (self.total % 100 == 0):
                self.log.info("总条数%s,耗时%sms",self.total,self.cost())
        _next = r[1]

        if(_next!=''):
            self.catch(_next)

    def catch_from_queue(self):
        while True:
            url = self.redis.spop(self.s_key)
            self.catch_detail(url)

    def catch_detail(self,url):
        try:
            page = requests.get(url).text
            self.parse_detail(url, page)
        except Exception as result:
            self.log.error('%s解析详情失败%s',url,result)
        else:
            self.log.info('解析详情成功')

    def parse_detail(self,url,page):

        job = {'job_id':0
            ,'job_name':''
            ,'company_name':''
            ,'base':[]
            ,'tags':[]
            ,'required':[]
            ,'func_type':''
            ,'keywords':[]
            ,'address':''
            ,'company_description':''
            ,'catch_url':''
            ,'source':'51JOB'
            ,'catch_date':datetime.utcnow()
               }
        soup = BeautifulSoup(page, "html5lib")
        job['job_id'] = int(soup.find(id='hidJobID')['value'])
        job['job_name'] = soup.select_one('h1[title]')['title']
        job['education'] = soup.select_one('div[class="cn"]').select_one('strong').text
        base = ''.join(soup.select_one('p[class="msg ltype"]')['title'].split())
        job['base'] = base.split('|')
        job['company_name'] = soup.select_one('a[class="catn"]')['title']
        tags = soup.select('span[class="sp4"]')
        for tag in tags:
             job['tags'].append(tag.text)
        detail = soup.select_one('div[class="bmsg job_msg inbox"]')
        requires = detail.find_all("p")
        for d in detail.select('p[class="fp"]'):
            title = d.find('span').text
            if('关键字：'==title):
                for key in d.find_all('a'):
                    job['keywords'].append(key.text)
            else:
                print()
                job['func_type'] = ''.join(d.select_one('a').text.split())
        for r in requires:
            if not r.has_attr('class'):
                job['required'] = r.text.split('；')
        job['company_description'] = ''.join(soup.select_one('div[class="tmsg inbox"]').text.split())
        job['address'] = ''.join(soup.select_one('div[class="bmsg inbox"]').select_one('p[class="fp"]').text.split())
        job['address'] = job['address'].split('：')[1]
        job['catch_url'] = url
        print(job)
        self.log.info('%s抓取完毕,存入数据',url)
        self.col.insert_one(job)

    def cost(self):
        return time.time()-self.start

    def run(self):
        self.catch(self.url)
        self.log.info("耗时%sms",self.cost())

if __name__ == '__main__':
    url = 'https://jobs.51job.com/shenzhen-lgq/103377435.html?s=01&t=1'
    crawler = Crawler()
    crawler.catch_detail(url)
