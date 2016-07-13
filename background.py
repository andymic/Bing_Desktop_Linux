#!/usr/bin/python3
from urllib.request import urlopen, urlretrieve
import os, getpass, json

def getImageURI(url):
    req = urlopen(url)
    enconding = req.headers.get_content_charset()
    data = json.loads(req.read().decode(enconding))
    return data['images'][0]['url']
  
def downLoadImage(url, localPath):  
    urlretrieve(url, localPath)
      
def setBackground(path):
    cmd = "gsettings set org.gnome.desktop.background picture-uri file://" + path
    os.system(cmd)
    
def getCurrentUser():
    return getpass.getuser()
  
def checkPath(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
if __name__ == '__main__':
    baseURL = str("http://www.bing.com")
    jsonUri = str("/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
    imgName = str("today_1920x1080.jpg")
    user = getCurrentUser()
    imgPath = str("/home/"+user+"/Pictures/wallpapers/")
    localPath = os.path.join(imgPath, imgName)
    
    checkPath(imgPath)
    imgUri = getImageURI(baseURL + jsonUri)
    downLoadImage(baseURL + imgUri, localPath)    
    setBackground(localPath)
