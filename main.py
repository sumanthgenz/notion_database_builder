import re
from imdb import IMDb
import pandas as pd
import numpy as np

def get_lines(name='films.txt'):
    with open(name) as f:
        lines = f.readlines()
    return [l[:-1] for l in lines]

def get_titles(lines):
    titles = [l.split("(")[0] for l in lines]
    return titles
    
def get_scores(titles, lines):
    scores = [re.findall(r'\([0-9]{2}\)', l) for l in lines]
    for i,s in enumerate(scores):
        if not len(s):
            scores[i] = scores[i-1]
    scores = [int(s[0][1:-1]) for s in scores]
    return scores

def get_ratings(titles, lines):
    lines = [l.split('(')[-1] for l in lines]
    rating_list = ['PG-13', 'PG', 'G', 'NC-17/R', 'NC-17', 'NR', 'R', 'MA', 'N/A', 'U/A', 'U', 'A']
    ratings = []
    for i in range(len(lines)):
        l, t = lines[i], titles[i]
        added = False
        for r in rating_list:
            if r in l:
                if not added:
                    ratings.append(r)
                    added = True
        if not added:
            ratings.append("N/A")
    return ratings
    
def get_years(titles):
    return [ia.search_movie(t)[0]['year'] for t in titles]

def get_grades(scores):
    grades = []
    for s in scores:
        if s >= 90:
            grades.append('*S*')
        elif s > 79:
            grades.append('A+')
        elif s > 77:
            grades.append('A')
        elif s > 75:
            grades.append('A-')
        elif s > 72:
            grades.append('B+')
        elif s > 70:
            grades.append('B')
        elif s > 67:
            grades.append('B-')
        elif s > 65:
            grades.append('C+')
        else:
            grades.append('C')   
    return grades
    
if __name__ == "__main__":
            
  lines = get_lines()
  titles = get_titles(lines)
  scores = get_scores(titles,lines)
  ratings = get_ratings(titles, lines)
  grades = get_grades(scores)
  df = pd.DataFrame({"Title": titles, "Rating": ratings, "Score": scores, "Grade": grades})
  df.to_csv('films.csv')
