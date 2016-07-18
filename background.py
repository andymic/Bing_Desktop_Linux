#!/usr/bin/python3
from urllib.request import urlopen, urlretrieve
from datetime import datetime
import os, getpass, json, sys, getopt, sched, time

def getJson(url):
    print("fetching json...")
    req = urlopen(url)
    enconding = req.headers.get_content_charset()
    data = json.loads(req.read().decode(enconding))
    return data['images']
  
def downloadImages(url, path, data):
    i = 1
    print("downloading images...")
    for d in data:
        imgName = str("today_1920x1080_"+ str(i) +".jpg")
        localPath = os.path.join(path, imgName)
        print("file location: "+localPath)
        urlretrieve(url + d['url'], localPath)
        i = i + 1
      
def setBackground(path):
    print("updating background to :" + path)
    cmd = "gsettings set org.gnome.desktop.background picture-uri file://" + path
    os.system(cmd)
    
def runInterval(frequency, localPath):
    sc = sched.scheduler(time.time, time.sleep)
    delay =  8 /  frequency
    delay = ((60**2) * delay)

    if frequency != 1:
        print("time is "+ str(datetime.now().strftime('%I:%M:%S %p')))
        print("background will update in "+ str(delay/60) + " minutes intervals")

    i = 1
    
    while True:
        imgName = str("today_1920x1080_"+ str(i) +".jpg")
        path = os.path.join(localPath, imgName)

        if i == 1:
            sc.enter(0, 1, setBackground, argument = (path,))
        else:
            sc.enter(delay, 1, setBackground, argument = (path,))

        sc.run()

        if i == frequency:
            print("done!")
            break

        i = i + 1


def getCurrentUser():
    return getpass.getuser()
  
def checkPath(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def help():
    print("~~~~~~~")
    print("|USAGE|")
    print("~~~~~~~")
    print("background.py -f <number>")
    print("-f is the number of times the background will be updated (1-8) over an 8hr span")

def run(frequency):
    baseUrl = str("http://www.bing.com")
    jsonUri = str("/HPImageArchive.aspx?format=js&idx=0&n="+str(frequency)+"&mkt=en-US")
    user = getCurrentUser()
    imgPath = str("/home/"+user+"/Pictures/Wallpapers/")

    checkPath(imgPath)
    data = getJson(baseUrl + jsonUri) 
    downloadImages(baseUrl, imgPath, data)
    runInterval(frequency, imgPath)


def main(argv):
    print("------------------------")
    print("| BING DESKTOP (Linux) |")
    print("------------------------")

    #Currently the api return 8 image nodes max
    frequency = 1

    try:
        opts, args = getopt.getopt(argv, "hf:", ["--frequency="])
    except getopt.GetoptError as ge:
        print(str(ge))
        help()
        sys.exit(1)

    for opt, arg in opts:
        val = int(arg)
        if opt  == '-h':
            help()
            sys.exit()
        elif opt in ("-f", "--frequency") and val >= 1 and val <= 8:
            frequency = val
        else:
           help()
           sys.exit()

    #8hr workdays :D
    print("Backgroud will change "+ str(frequency) + " time(s) over the next 8hrs")
    run(frequency)
        
if __name__ == '__main__':
    main(sys.argv[1:])

