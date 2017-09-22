#!/usr/bin/python3
from urllib.parse import urlsplit
from urllib.request import urlopen
from html.parser import HTMLParser
import hashlib
import datetime

###############################################################################################
### Feature set format: 
### {"url.com": (filename, featureVectorDict )}
###############################################################################################

# Takes url and returns unique name for use in filename and 
# feature set
def FileNameForUrl(url):
	m = hashlib.md5()
	m.update(url.encode('utf-8'))
	return str(int(m.hexdigest(), 16))[0:12] + ".txt"


# This function gets the raw HTML string given a url
# returns empty string if there is an HTTP Error
def GetHTML(url):
	# see if we already saved this page's html
	name = fileNameForUrl(url)
	if name in featureSet:
		file = open(name, "r")
		return file.read()

	try:
		with urlopen(url) as f:
			return f.read().decode("utf-8", errors="replace")
	except Exception as e:
		#print(str(e))
		return ""

# This function uses the HTML Parser class to add all the absolute links on the page to the stack
def ParseHTML(parser, html, parentURL, parentLevel):
	# Resets list of links and feeds the HTML to the parser
	parser.initLinks()
	parser.feed(html)

	SplitResult = urlsplit(parentURL)
	SameDomain = []
	DifferentDomain = []

	# Filters out URLs and adds them to the stack
	links = parser.getLinks()
	for link in links:

		# Create the URL for the given HREF
		linkLength = len(link)
		childURL = ""
		if linkLength > 0 and link[0] == "#":
			continue	# Skip page relative links
		if linkLength > 3 and link[0:4] == "http":
			childURL = link	# Abosulte 
		elif linkLength > 0:
			if link[0] == "/":
				if linkLength > 1 and link[1] == "/":
					childURL = SplitResult[0] + ":" + link	# Protocol relative
				else:
					childURL = SplitResult[0] + "://" + SplitResult[1] + link # Root relative
			elif link[0] == ".":
				if link[1] == ".":
					continue						# Directory traversal (todo)
				elif link[1] == "/":
					childURL = parentURL + link[1:]	# Path relative
			else:
				if parentURL[-1] == "/":
					childURL = parentURL + link	# Path relative
				else:
					childURL = SplitResult[0] + "://" + SplitResult[1] + "/" + link # Root relative
				

		# Divide URLs based on there NetLoc produced from the urlsplit function
		childSplitResult = urlsplit(childURL)
		if len(SameDomain) < SameBranchingFactor and childSplitResult[1] == SplitResult[1]:
			SameDomain.append((parentLevel + 1, childURL))
		elif len(DifferentDomain) < DifferentBranchingFactor and childSplitResult[1] != SplitResult[1]:
			DifferentDomain.append((parentLevel + 1, childURL))

	# Add the different NetLocs on top so they get explored first
	stack.extend(SameDomain)
	stack.extend(DifferentDomain)

# Initializes the dictionary of unigram features
def GenerateUnigramsFeatureList():
	InitialFeatureList = {}
	for c in range(ord(" "), ord("~") + 1):
		InitialFeatureList[chr(c)] = 0
	return InitialFeatureList

# Extracts unigrams and returns a feature vector
def ExtractUnigram(url, htmlString):
	if url in featureSet:
		return featureSet[url]
	else:
		name = FileNameForUrl(url)
		featureSet[url] = (name, GenerateUnigramsFeatureList())

	for feature in list(htmlString):
		key = str(feature)
		if key in featureSet[url][1]:
			featureSet[url][1][key] += 1

	for key in featureSet[url][1]:
		featureSet[url][1][key] = featureSet[url][1][key]/len(htmlString)

	return featureSet[url]
	
# Saves the html as a text file
def SaveHTML(htmlString, url):
	filename = FileNameForUrl(url)
	with open(str(filename), "w", encoding = "utf-8") as f:
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

ExpandedNodes = 0
DuplicateNodes = 0


with open("results.txt", "a") as f:
	f.write("Depth,SameBranchingFactor,DifferentBranchingFactor,ExpandedNodes,DuplicatesExpanded,Time\n")
featureSet = {}
# Outer loop for the iterative deepening
level = 0
DifferentBranchingFactor = 0
SameBranchingFactor = 0
for i in range(2, 5):
	level = i
	for j in range(1,5):
		featureSet = {}
		ExpandedNodes = 0
		DuplicateNodes = 0
		parser = MyHTMLParser()
		DifferentBranchingFactor = 2**j
		SameBranchingFactor = 2**(j-1)
		start = datetime.datetime.now()
		for i in range(level):
	
			# Initialize the stack with the seed URL
			stack = [(0, "http://asdf.com/")]
			# Start the DFS Search
			while len(stack) > 0:
				# Pops off the top node of the stack and gets the raw HTML string
				node = stack.pop()

				# Unique name for this node to be used for filename and key in featureSet
				#print("\n" + str(node[0]) + ": " + node[1])

				HTMLString = GetHTML(node[1])
				if HTMLString == "":
					continue
		
				ExpandedNodes = ExpandedNodes + 1
				# If the max depth has not been reached add the chilren nodes to the stack
				if node[0] < i:
					ParseHTML(parser, HTMLString, node[1], node[0])

				# Skip feature extraction if it's already been done on this node
				if node[1] in featureSet:
					DuplicateNodes = DuplicateNodes + 1
					continue

				# Uni-gram feature extraction
				featureVector = ExtractUnigram(node[1], HTMLString)
				#print("Unigram feature set for " + node[1] + ":\n" + str(featureVector))

				# TODO Ask this node if it is the solution

				# Save the html into text files
				#SaveHTML(HTMLString, node[1])

		
		end = datetime.datetime.now()
		parser.close()
		with open("results.txt", "a") as f:
			f.write(str(level) + "," + str(SameBranchingFactor) + "," + str(DifferentBranchingFactor) + "," + str(ExpandedNodes) + "," + str(DuplicateNodes) + "," + str(end - start) + "\n")
		print("Depth: " + str(level))
		print("Same Branching factor: " + str(SameBranchingFactor))
		print("Different Branching factor: " + str(DifferentBranchingFactor))
		print("Nodes expanded: " + str(ExpandedNodes))
		print("Duplicates expanded: " + str(DuplicateNodes))
		print("Time:" + str(end - start))
