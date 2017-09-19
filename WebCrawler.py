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

	# Filters out URLs and adds them to the stack
	links = parser.getLinks()
	for link in links:
		if len(link) > 3 and link[0:4] == "http":	# Absolute URL
			stack.append((parentLevel + 1, link))
		elif len(link) > 0 and link[0] == "/":		# Relative URL
			if len(link) > 1 and link[1] == "/":
				stack.append((parentLevel + 1, SplitResult[0] + ":" + link))
			else:
				stack.append((parentLevel + 1, SplitResult[0] + "://" + SplitResult[1] + link))

# Extracts unigrams and returns a feature vector
def ExtractUnigram(htmlString):
	featureSet = dict()

	for feature in list(htmlString):
		key = str(feature)
		if key in featureSet.keys():
			featureSet[key] += 1
		else:
			featureSet[key] = 1

	return featureSet

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

# Outer loop for the iterative deepening
level = 4
for i in range(level):
	# Initialize the stack with the seed URL
	stack = [(0,"http://asdf.com/")]

	# Start the DFS Search
	while len(stack) > 0:
		# Pops off the top node of the stack and gets the raw HTML string
		node = stack.pop()
		print("\n" + str(node[0]) + ": " + node[1])
		HTMLString = GetHTML(node[1])

		# Uni-gram feature extraction
		featureVector = ExtractUnigram(HTMLString)
		print("Unigram feature set for " + node[1] + ":\n" + str(featureVector))

		# Save the html into text files

		# If the max depth has not been reached add the chilren nodes to the stack
		if node[0] < i:
			ParseHTML(parser, HTMLString, node[1], node[0])
		

parser.close()