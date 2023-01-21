from multiprocessing import Process, Queue
from job_scraper.spiders import indeed_s
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def indeed(event, context):
    def script(queue):
        try:
            settings = get_project_settings()

            settings.setdict({
                'LOG_LEVEL': 'ERROR',
                'LOG_ENABLED': True,
            })

            process = CrawlerProcess(settings)
            process.crawl(indeed_s.IndeedSpider)
            process.start()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    queue = Queue()

    # wrap the spider in a child process
    main_process = Process(target=script, args=(queue,))
    main_process.start()    # start the process
    main_process.join()     # block until the spider finishes

    result = queue.get()    # check the process did not return an error
    if result is not None:
        raise result
        
    return "ok"


if __name__ == "__indeed__":
    indeed("event","context")