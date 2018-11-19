import requests
import time

from bs4 import BeautifulSoup

from core import LogUtil


class Crawler():

    def __init__(self,url):
        self.url = url
        self.total = 0
        self.start = time.time()
        self.log = LogUtil.LogUtil.get_logger()


    def get(self,url):
        r = requests.get(url)
        r.encoding = 'GBK'
        return r.text

    def parse_list_page(self,list_page):
        soup = BeautifulSoup(list_page, "html5lib")
        urls = []
        for tag in soup.select("p[class='t1 ']"):
            urls.append(tag.select_one('a[onmousedown]')['href'])
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

    def parse_detail(self,page):
        job = {'job_id':''
            ,'job_name':''
            ,'company_name':''
            ,'city':''
            ,'district':''
            ,'exp_up':0
            ,'exp_down':0
            ,'education':''
            ,'recruiting_nums':0
            ,'issue_date':''
            ,'tags':[]
            ,'required':[]
            ,'func_type':''
            ,'keywords':[]
            ,'address':''
            ,'company_description':''
            ,'catch_url':''
            ,'source':'51JOB'
            ,'catch_date':time.localtime(time.time())
               }

    def cost(self):
        return time.time()-self.start

    def run(self):
        self.catch(self.url)
        self.log.info("耗时%sms",self.cost())

if __name__ == '__main__':
    url = 'https://search.51job.com/list/040000,000000,0000,00,9,99,java,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    crawler = Crawler(url)
    crawler.run()
