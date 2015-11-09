#!/usr/bin/python
#-*- coding:utf-8 -*-
__author__ = 'david'
from __builtin__ import *
from selenium import webdriver

import sys,time,datetime,math,os

PhantomJS = './tools/phantomjs'
DataFile = './data/DOCKET_ICEB-2015-0002.csv'
CrawledFile = './data/CrawledLinks.txt'
CommentsFile = './data/comments.txt'
ReadableComments = './comments.md'
driver = webdriver.PhantomJS(executable_path=PhantomJS)

def main():
  reload(sys)
  sys.setdefaultencoding('utf-8')

  #Load crawled
  crawledLinks = []
  if os.path.exists(CrawledFile):
      with open(CrawledFile,'r') as crawled:
          data=crawled.readlines()
          for d in data:
              d=d.strip('\n')
              crawledLinks.append(d)

  #Load links
  links = []
  with open(DataFile,'r') as df:
    data=df.readlines()
    # skip 6 lines
    for s in data[7:]:
        url = s.strip('\n').split(',')[-1]
        if crawledLinks.count(url) < 1:
            links.append(url)

  #Crawl comments
  parallel = 4
  it = int(math.ceil(len(links)/float(parallel)))

  for i in range(0,it):
      start = i*parallel
      if start+parallel < len(links):
          results=map(getComment,links[start : start+parallel])
          writeComments(results)
          writeCrawled(links[start : start+parallel])
          print '+',
          sys.stdout.flush()
      else:
          results=map(getComment,links[start:])
          writeComments(results)
          writeCrawled(links[start : start+parallel])
          print '+',
          sys.stdout.flush()

  driver.quit()

def writeComments(comments):
    with open(CommentsFile,'a+') as comment, open(ReadableComments,'a+') as readable:
        for cmt in comments:
            comment.write(cmt+'\n')
            readable.write("* "+cmt+"\n\n---\n\n")


def writeCrawled(urls):
    with open(CrawledFile,'a+') as crawled:
        for url in urls:
            crawled.write(url+'\n')

# reduce function
def getComment(url):
  print '.',
  sys.stdout.flush()

  driver.get(url)
  time.sleep(5)
  elem = driver.find_element_by_xpath("//*")
  source_code = elem.get_attribute("outerHTML")
  res = source_code.split('View document:')[-1].split('</div>')[3]
  res=res.replace("<br>","").replace(' <div class="">',"").replace('<div class="hidden">','')
  #driver.close()

  return res.strip(' ')


if __name__ == '__main__':
    main()
