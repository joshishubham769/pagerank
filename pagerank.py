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


def transition_model(corpus, page, damping_factor):#hon gaya
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    total number of pages nt,pages the page links to np
    dict page:probability(pb) pb=(1-damping_factor)/nt+damping_factor/np
    """
    dic={}
    #print(page," ",corpus[page])
    linked_pages=corpus[page]
    
    np=len(linked_pages)
    nt=len(corpus)
    
    if(np==0):
        for p in corpus.keys():
            dic[p]=1/nt
        return dic
    
    for p in corpus.keys():
        if p in linked_pages:
            dic[p]=(1-damping_factor)/nt+damping_factor/np
        else:
            dic[p]=(1-damping_factor)/nt
    
    return dic

def choose(dictionary):

    k=random.random()
    t=0
    for key in dictionary.keys():
        if k<t+dictionary[key] and k>t:
            return key
        t=t+dictionary[key]
        
def sample_pagerank(corpus, damping_factor, n):#sahi
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dic={}
    for key in corpus.keys():
        dic[key]=0
        
    page=random.choice(list(corpus.keys()))
    dic[page]=1
    
    for i in range(n):
    
        kdic=transition_model(corpus,page,damping_factor)
        page=choose(kdic)
        dic[page]=dic[page]+1
        
    for m in dic.keys():
        dic[m]=dic[m]/n

    return dic
        
        
def conditional(corpus,key,dic):
    s=0
    
    
    for k in corpus.keys():
        if key in corpus[k]:
            s=s+dic[k]/len(corpus[k])

    return s   


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dic={}
    n=len(corpus)
    
    for key in corpus.keys():
        dic[key]=1/n

    while True:
        flag=True
        
        for key in dic.keys():
            k=(1-damping_factor)/n+damping_factor*conditional(corpus,key,dic)
            if abs(dic[key]-k)>0.001:
                flag=False
            dic[key]=k
            
        
        if flag:
            break

    return dic
    


if __name__ == "__main__":
    main()
