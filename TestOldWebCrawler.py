#!/usr/bin/python3
from urllib.parse import urlsplit
from urllib.request import urlopen
from html.parser import HTMLParser
import datetime


# This function gets the raw HTML string given a url
# returns empty string if there is an HTTP Error
def GetHTML(URL):
    try:
        with urlopen(URL) as f:
            return f.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(str(e))
        return ""

# This function uses the HTML Parser class to add all the absolute links on the page to the stack
def ParseHTML(parser, html, parentURL, parentLevel):
    # Resets list of links and feeds the HTML to the parser
    parser.initLinks()
    parser.feed(html)

    SplitResult = urlsplit(parentURL)

    # Filters out URLs and adds them to the stack
    links = parser.getLinks()
    for link in links:
        linkLength = len(link)
        if linkLength > 0 and link[0] == "#":
            continue
        if linkLength > 3 and link[0:4] == "http":
            stack.append((parentLevel + 1, link))	# Abosulte 
        elif linkLength > 1:
            if link[0] == "/":
                if link[1] == "/":
                    stack.append((parentLevel + 1, SplitResult[0] + ":" + link))	# Protocol relative
                else:
                    stack.append((parentLevel + 1, SplitResult[0] + "://" + SplitResult[1] + link)) # Root relative
            elif link[0] == ".":
                if link[1] == ".":
                    pass
                elif link[1] == "/":
                    stack.append((parentLevel + 1, parentURL + link[1:]))
            else:
                stack.append((parentLevel + 1, parentURL + link))	# Path relative

# Extracts unigrams and returns a feature vector
def ExtractUnigram(url, htmlString):
    featureSet[url] = {}

    for feature in list(htmlString):
        key = str(feature)
        if key in featureSet[url]:
            featureSet[url][key] += 1
        else:
            featureSet[url][key] = 1

    return featureSet
    
# Saves the html as a text file
def SaveHTML(htmlString, filename):
    with open(str(filename) + ".txt", "w", encoding = "utf-8") as f:
        f.write(htmlString)

# This class handles the parsing of the HTML
# It gets the href value of each of the anchor tags on the page
class MyHTMLParser(HTMLParser):
    links = []
    def initLinks(self):
        self.links = []

    def getLinks(self):
        return self.links

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href" and attr[1] is not None:
                    self.links.append(attr[1])


parser = MyHTMLParser()

ExpandedNodes = 0
DuplicateNodes = 0
featureSet = {}
with open("old_results.txt", "a") as f:
	f.write("Depth,ExpandedNodes,DuplicatesExpanded,Time\n")

# Outer loop for the iterative deepening
start = datetime.datetime.now()
for i in range(2,5):
    level = i
    featureSet = {}
    ExpandedNodes = 0
    DuplicateNodes = 0

    # Initialize the stack with the seed URL
    stack = [(0,"http://asdf.com")]

    filenum = 0
    # Start the DFS Search
    while len(stack) > 0:
        # Pops off the top node of the stack and gets the raw HTML string
        node = stack.pop()
        print("\n" + str(node[0]) + ": " + node[1])

        HTMLString = GetHTML(node[1])

        ExpandedNodes = ExpandedNodes + 1
        # Uni-gram feature extraction
        #print("Unigram feature set for " + node[1] + ":\n" + str(featureVector))

        # Save the html into text files
        #SaveHTML(HTMLString, str(i) + str(filenum))
        filenum = filenum + 1

        # If the max depth has not been reached add the chilren nodes to the stack
        if node[0] < i:
            ParseHTML(parser, HTMLString, node[1], node[0])


        if node[1] in featureSet:
            DuplicateNodes = DuplicateNodes + 1
            continue

        featureVector = ExtractUnigram(str(node[1]), HTMLString)
        
    end = datetime.datetime.now()
    with open("old_results.txt", "a") as f:
        f.write(str(level) + "," + str(ExpandedNodes) + "," + str(DuplicateNodes) + "," + str(end - start) + "\n")
        print("Depth: " + str(level))
        print("Nodes expanded: " + str(ExpandedNodes))
        print("Duplicates expanded: " + str(DuplicateNodes))
        print("Time:" + str(end - start))
parser.close()