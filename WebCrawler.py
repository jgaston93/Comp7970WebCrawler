#!/usr/bin/python3
from urllib.parse import urlsplit
from urllib.request import urlopen
from html.parser import HTMLParser
import hashlib
from GRNN import GRNN
from Helpers import load_dataset

###############################################################################################
### Feature set format:
### {"url.com": (filename, feature_vectorDict )}
###############################################################################################

# Takes url and returns unique name for use in filename and
# feature set
def file_name_for_url(url):
    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    return str(int(m.hexdigest(), 16))[0:12] + ".txt"


# This function gets the raw HTML string given a url
# returns empty string if there is an HTTP Error
def get_html(url):
    # see if we already saved this page's html
    name = file_name_for_url(url)
    if name in feature_set:
        file = open(name, "r")
        return file.read()

    try:
        with urlopen(url) as f:
            return f.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(str(e))
        return ""

# This function uses the HTML Parser class to add all the absolute links on the page to the stack
def parse_html(html, parent_url, parent_level):
    # Resets list of links and feeds the HTML to the parser
    parser.init_links()
    parser.feed(html)

    same_domain = []
    different_domain = []
    split_result = urlsplit(parent_url)

    # Filters out URLs and adds them to the stack
    links = parser.get_links()
    for link in links:
        child_url = generate_child_url(parent_url, link)
        if child_url is None:
            continue
        # Divide URLs based on there NetLoc produced from the urlsplit function
        child_split_result = urlsplit(child_url)
        if len(same_domain) < same_branching_factor and child_split_result[1] == split_result[1]:
            same_domain.append((parent_level + 1, child_url))
        elif len(different_domain) < different_branching_factor and child_split_result[1] != split_result[1]:
            different_domain.append((parent_level + 1, child_url))

    # Add the different NetLocs on top so they get explored first
    stack.extend(same_domain)
    stack.extend(different_domain)

# Parses scheme and url type and returns a cleaned child URL
def generate_child_url(parent_url, link):
    split_result = urlsplit(parent_url)

    # Create the URL for the given HREF
    link_length = len(link)
    child_url = ""
    if link_length > 0 and link[0] == "#":
        return None	# Skip page relative links
    if link_length > 3 and link[0:4] == "http":
        child_url = link	# Absolute
    elif link_length > 0:
        if link[0] == "/":
            if link_length > 1 and link[1] == "/":
                child_url = split_result[0] + ":" + link	# Protocol relative
            else:
                child_url = split_result[0] + "://" + split_result[1] + link # Root relative
        elif link[0] == ".":
            if link[1] == ".":
                return None						# Directory traversal (todo)
            elif link[1] == "/":
                child_url = parent_url + link[1:]	# Path relative
        else:
            if parent_url[-1] == "/":
                child_url = parent_url + link	# Path relative
            else:
                child_url = split_result[0] + "://" + split_result[1] + "/" + link # Root relative
    return child_url

# Initializes the dictionary of unigram features
def generate_unigrams_feature_list():
    initial_feature_list = {}
    for char in range(ord(" "), ord("~") + 1):
        initial_feature_list[chr(char)] = 0
    return initial_feature_list

# Extracts unigrams and returns a feature vector
def extract_unigram(url, html_string):
    if url in feature_set:
        return feature_set[url]
    else:
        name = file_name_for_url(url)
        feature_set[url] = (name, generate_unigrams_feature_list())

    for feature in list(html_string):
        key = str(feature)
        if key in feature_set[url][1]:
            feature_set[url][1][key] += 1

    for key in feature_set[url][1]:
        feature_set[url][1][key] = feature_set[url][1][key]/len(html_string)

    return feature_set[url]

# Saves the html as a text file
def save_html(html_string, url):
    file_name = file_name_for_url(url)
    with open(str(file_name), "w", encoding="utf-8") as f:
        f.write(html_string)

def save_feature_vector(url):
    vector_dict = feature_set[url]
    

# This class handles the parsing of the HTML
# It gets the href value of each of the anchor tags on the page
class MyHTMLParser(HTMLParser):
    links = []
    def init_links(self):
        self.links = []

    def get_links(self):
        return self.links

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href" and attr[1] is not None:
                    self.links.append(attr[1])

##################################################################
# SCRIPTING
##################################################################

parser = MyHTMLParser()
feature_set = {}
# Outer loop for the iterative deepening
level = 4
different_branching_factor = 5
same_branching_factor = 0
seed_url = "https://google.com"

num_pages = 20
pages_visted = 0

dataset = load_dataset("our_dataset.txt")
grnn = GRNN(dataset)

for i in range(level):
    # Initialize the stack with the seed URL
    stack = [(0, seed_url)]
    # Start the DFS Search
    while len(stack) > 0:
        # Pops off the top node of the stack and gets the raw HTML string
        node = stack.pop()

        # Unique name for this node to be used for filename and key in feature_set
        print("\nDepth " + str(node[0] + 1) + ": " + node[1])

        html_string = get_html(node[1])
        if html_string == "":
            continue

        # If the max depth has not been reached add the chilren nodes to the stack
        if node[0] < i:
            parse_html(html_string, node[1], node[0])

        # Skip feature extraction if it's already been done on this node
        if node[1] in feature_set:
            continue

        # Uni-gram feature extraction
        feature_vector = extract_unigram(node[1], html_string)
        # print("Unigram feature set for " + node[1] + ":\n" + str(feature_vector))

        # Ask this node if it is the solution
        clasifier_result = grnn.classify(feature_vector[1].values())
        print(clasifier_result)


        # Save the html into text files
        save_html(html_string, node[1])
        save_feature_vector(node[1])

        pages_visted += 1
        if pages_visted == num_pages:
            print('doneski')
            break

parser.close()
