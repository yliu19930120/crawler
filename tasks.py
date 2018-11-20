import crawler


class Task():

    TASKS = {"JOB_CRAWLER_LISTS":lambda:crawler.Crawler().run()
             ,"JOB_CRAWLER_DETAILS":lambda:crawler.Crawler().catch_detail()}

    def __init__(self):
        pass

    def runJob(self,msg):
        if(msg in self.TASKS.keys()):
            self.TASKS[msg]()

