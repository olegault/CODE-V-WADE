import re
import sys
##use re.search here to parse for file names

q_answer = []
i=0
pattern = ['reproductive health', 'menstural health', 'period', 'cycle', 'period calendar']
text_file = open("polisis_ouput.json", "r")
for line in text_file:
    if re.search(pattern, line):
        q_answer[i]=1
        i=i+1
        