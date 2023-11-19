import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    running_dict = dict()
    if corpus[page]:
        current_page_links = corpus[page]
    else:
        current_page_links = corpus.keys()
    running_dict[f"{page}"] =round((1.0-damping_factor)/ len(corpus), 2)
    for pages in corpus:
        running_dict[f"{pages}"] = round((1.0-damping_factor)/ len(corpus), 2)
    for link in current_page_links:
        running_dict[f"{link}"] += damping_factor/len(current_page_links)
    return (running_dict) 


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    current_page = (random.choice(list(corpus.keys())))
    pagerank_dict = dict()
    for page in corpus:
        pagerank_dict[f"{page}"] = 0
    for i in range(n-1):
        available_links = list(transition_model(corpus, current_page, damping_factor).keys())
        link_weights = list(transition_model(corpus, current_page, damping_factor).values())
        current_page = random.choices(available_links, weights =  [i * 100 for i in link_weights] , k = 1)[0]
        pagerank_dict[current_page] += 1
    for page in pagerank_dict:
        pagerank_dict[f"{page}"] /= n
    return pagerank_dict
        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = dict()
    convergence_threshold = 0.001  
    N = len(corpus) 
    for page in corpus:
        pagerank_dict[f"{page}"] = 1/N
    while True:
        count = 0
        for page in corpus:
            running_pagerank = (1-damping_factor)/N
            difference = 0
            for second_loop_page in corpus:
                if page in corpus[second_loop_page]:
                    num_links = len(corpus[second_loop_page])
                    difference += pagerank_dict[second_loop_page] / num_links
            difference *= damping_factor
            running_pagerank += difference
            if abs(pagerank_dict[page] - running_pagerank) < convergence_threshold:
                count += 1
            pagerank_dict[page] = running_pagerank
        if count == N:
            break
    return pagerank_dict
        

if __name__ == "__main__":
    main()
