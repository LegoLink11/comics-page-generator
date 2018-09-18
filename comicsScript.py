import requests, os, bs4
from webbrowser import open as webopen

url = "" #Declares the URL variable

print("Processing...")

def GetWebsite(url, tag, name, getType, append):
    #url is the url of the website we're getting the comic from
    #tag is the location of the image in the html document
    #name is what the image file will be named when it's downloaded
    #getType is how the image source url will be processed
    try:
        res = requests.get(url) #Download the webpage
        res.raise_for_status() #see if it works

        soup = bs4.BeautifulSoup(res.text, "lxml") #Creates a bs4 object so the html document can be parsed
        #print(res.text)

        comicElem = soup.select(tag) #Select the comic image

        print ("Getting comic from {}".format(url))


        #This bit requires a lot of explaining. What the getType variable does is determine how the image source url will be retrieved.
        #With getType 0, it appends something special to the beginning. For when the src isn't in the element directly, but also isn't just preceded by the url.
        #getType 1 gets the image source, and adds the url to the beginning. Used when the img src attribute doesn't have a url at the beginning.
        #getType 2 just gets the image source. Used when the img src attribute is complete.
        #If you want to add your own websites make sure you know which of these to use
        try:
            if getType == 0:
                comicUrl = append + comicElem[0].get("src")
            elif getType == 1:
                comicUrl = url + comicElem[0].get("src")
            else:
                comicUrl = comicElem[0].get("src")
        

            
            res = requests.get(comicUrl) #Get the souce url of the comic image
            res.raise_for_status() #Make sure the website exists

            imageFile = open(os.path.basename(name), "wb") #Makes the imageFile variable as a writable file in binary mode. The name variable defines what the image file will be named.
            for chunk in res.iter_content(10000): #download the image in 10kb chunks
                imageFile.write(chunk) #write the chunk into the file
            imageFile.close()
        except Exception as e:
            print(e)
            print ("Couldn't download comic from {}".format(url))
    except Exception as e:
        print(e)
        print("Couldn't retrieve webpage from {}".format(url))

def GetHoverText(url, tag):
    #Most of what this does was explained in the commenting for the GetWebsite function
    print("Getting hover text from {}".format(url))
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml") 
    textElem = soup.select(tag)
    
    text = textElem[0].get("title")

    #The point of this bit is to make sure apostrophies, quotation marks, and line breaks in the text itself can't screw with the js file when it's written
    text = text.replace("'", "")
    text = text.replace('"', '')
    text = text.replace("\n", " | ")
    text = text.replace("\r", " | ")
    
    return text
    

#Go through all the functions
GetWebsite("https://xkcd.com", "#comic img", "xkcd", 0, "http:")
xkcdtext = GetHoverText("https://xkcd.com", "#comic img")
GetWebsite("https://www.smbc-comics.com/", "#cc-comic", "smbc", 2, "")
GetWebsite("https://www.smbc-comics.com/", "#aftercomic img", "smbc-bonus", 2, "")
smbctext = GetHoverText("https://www.smbc-comics.com/", "#cc-comic")
GetWebsite("http://www.bugmartini.com", "#comic img", "bugmartini", 2, "")
GetWebsite("http://the-whiteboard.com/", 'img[SRC^="autotwb"]', "whiteboard", 1, "") #this website won't work and I don't know why.
GetWebsite("http://www.qwantz.com/index.php", ".comic", "dinosaurcomics", 0, "http://www.qwantz.com/")
dinotext = GetHoverText("http://www.qwantz.com/index.php", ".comic")
GetWebsite("http://nellucnhoj.com", "figure a img", "nellucnhoj", 2, "")
GetWebsite("http://www.housepetscomic.com", "#comic img", "housepets", 2, "")
petstext = GetHoverText("http://www.housepetscomic.com", "#comic img")
GetWebsite("http://www.joshuawright.net/index.html", "[data-muse-type=img_frame] img", "slackwyrm", 0, "http://www.joshuawright.net/")
GetWebsite("https://www.bonequest.com/", ".hitler", "jerkcity", 1, "")
GetWebsite("http://sarahburrini.com/wordpress/", "#comic img", "ponyhof", 2, "")
GetWebsite("http://ruthe.de/", "#link_archive img", "ruthe", 1, "")
GetWebsite("https://2null3.net/category/deutsch/", ".entry-content p img", "2null3", 2, "")
GetWebsite("http://www.sandraandwoo.com/woode/", "#comic img", "sandraandwoo", 0, "http://www.sandraandwoo.com/")

#I bet there's a way better way to do this part.
print("Implementing hover text...")
hoverTextScript = open("hovertext.js", "w")#declare the hoverTextScript variable as a writable javascript file
#This super long line writes an entire javascript file.
hoverTextScript.write('document.getElementById("xkcdtext").innerHTML = "' + xkcdtext + '";document.getElementById("smbctext").innerHTML = "' + smbctext + '";document.getElementById("dctext").innerHTML = "' + dinotext + '";document.getElementById("housepetstext").innerHTML = "' + petstext + '";')
hoverTextScript.close()

print("Done. Opening your comics page...")
webopen("TheFunnies.html") #Open your web browser with the HTML file that you should have downloaded already. All the data that was retrieved in this script is used in that HTML file.
