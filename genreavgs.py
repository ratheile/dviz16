import functools as ft
import multiprocessing as mp
import numpy as np
import json

import plotly.graph_objs as go
import plotly.offline as offline
from plotly import tools

def containsdigit(s):
    if any(char.isdigit() for char in s) == True:
        return True
    else:
        return False

def extractnr(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def extract_movie_and_year(tokens, start):   
    moviename = ""
    year = None
    appendnext = True
    ismovie = True
    ismovienow = False
    for t in range(start, len(tokens)-1):
        ismovienow = ismovie
        if tokens[t+1].startswith('(1') == False and tokens[t+1].startswith('(2') == False and ismovienow == True:
            appendnext = True
        elif tokens[t+1].startswith('(1') == True or tokens[t+1].startswith('(2') == True :
            ismovie = False
            year = extractnr(tokens[t+1])
                
        if appendnext == True and ismovienow == True:
            moviename = moviename + str(" " + tokens[t])
            appendnext == False
    return [moviename, year]


#returns [name, year, rating, votes, length]
def processRatingsLine(line): 
    tokens = line.split()
    rating = tokens[2]
    nr_votes = tokens[1]
    mov_year = extract_movie_and_year(tokens,3)
    mov_year.append(float(rating))
    mov_year.append(int(nr_votes))
    mov_year.append(-1)
    return [(mov_year[0], mov_year[1]), rating]
    
    
def processGenres(line):
    tokens = line.split()
    genre = tokens[-1]
    mov_year = extract_movie_and_year(tokens, 0)
    mov_year.append(genre)
    return [(mov_year[0], mov_year[1]), genre, -0.1]

filename = "ratings.txt"
with open(filename, "r", encoding="latin-1") as f:
    ratings = f.readlines()[297:695711]
print("read file: ratings.txt")

filename = "genres.txt"
with open(filename, "r", encoding="latin-1") as f:
    genres = f.readlines()[385:2397982]
print("read file: running-times.txt")

pool = mp.Pool()
ratings_list = pool.map(processRatingsLine, ratings)
print("rating list created: ", len(ratings_list))


genres_list = pool.map(processGenres, genres)
print("genres list created: ", len(genres_list))

rating_d = dict(ratings_list)

for genre_entry in genres_list:
    if genre_entry[0] in rating_d:
        genre_entry[2] = float(rating_d[genre_entry[0]]) 


data_with_rating= list(filter(lambda x:x[2] and x[2] > 0, genres_list))

np_genres = np.array(data_with_rating)

uni_gen = np.unique(np_genres[:,[1]])

genre_avgs = {}
for gen in uni_gen:    
    subset = list(filter(lambda x: x[1] == gen, np_genres))
    count = 0
    scores = 0.0
    for movie in subset:
        count = count+1
        scores = scores + movie[2]
    genre_avgs[gen] = scores / count

with open('static/genreavgs.json', 'w') as outfile:
    json.dump(genre_avgs, outfile)