import crawler
import threading

class Task():

    TASKS = {"JOB_CRAWLER_LISTS":lambda:crawler.Crawler().run()
             ,"JOB_CRAWLER_DETAILS":lambda:crawler.Crawler().catch_from_queue()}

    def __init__(self):
        pass

    def runJob(self,msg):
        if(msg in self.TASKS.keys()):
            t = threading.Thread(self.TASKS[msg](),name=msg+'Thread')
            t.start()
            t.join()



