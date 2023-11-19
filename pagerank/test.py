import os
import random
import re
import sys
from pagerank import transition_model, sample_pagerank, iterate_pagerank

DAMPING = 0.85
SAMPLES = 10000

corpus0 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
#print(sample_pagerank(corpus0, 0.85, SAMPLES))

#print((transition_model(corpus0, "1.html", 0.85)))


print(iterate_pagerank(corpus0,0.85))

