#!/usr/bin/python3
from urllib.parse import urlsplit
from urllib.request import urlopen
from html.parser import HTMLParser

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
		if len(SameDomain) + len(DifferentDomain) < branchingFactor:
			if childSplitResult[1] == SplitResult[1]:
				SameDomain.append((parentLevel + 1, childURL))
			else:
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
		featureSet[url] = GenerateUnigramsFeatureList()

	for feature in list(htmlString):
		key = str(feature)
		if key in featureSet[url]:
			featureSet[url][key] += 1
	for key in featureSet[url]:
		featureSet[url][key] = featureSet[url][key]/len(htmlString)
	return featureSet[url]
	
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

featureSet = {}
# Outer loop for the iterative deepening
level = 4
branchingFactor = 2
for i in range(level):
	
	# Initialize the stack with the seed URL
	stack = [(0,"http://asdf.com/")]

	filenum = 0
	# Start the DFS Search
	while len(stack) > 0:
		# Pops off the top node of the stack and gets the raw HTML string
		node = stack.pop()
		print("\n" + str(node[0]) + ": " + node[1])
		HTMLString = GetHTML(node[1])
		if HTMLString == "":
			continue

		# If the max depth has not been reached add the chilren nodes to the stack
		if node[0] < i:
			ParseHTML(parser, HTMLString, node[1], node[0])

		# Skip feature extraction if it's already been done on this node
		if node[1] in featureSet:
			continue

		# Uni-gram feature extraction
		featureVector = ExtractUnigram(str(node[1]), HTMLString)
		print("Unigram feature set for " + node[1] + ":\n" + str(featureVector))

		# Save the html into text files
		SaveHTML(HTMLString, str(i) + str(filenum))
		filenum = filenum + 1

		# Ask this node if it is the solution
		
parser.close()
