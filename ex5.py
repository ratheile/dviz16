

import plotly
plotly.tools.set_credentials_file(username='mariella.greutmann', api_key='qDCo06vWnbzjCxAyQRpC')

import plotly.graph_objs as go


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


############################################# TASK 1 ################################################################
# In the first task, you have to create a plot in order to present the movie rating of IMDb movies from
# Switzerland for the time period between 2000 and 2010 for all genres (aggregated). 
# In the same plot and for the same time period you have to present also the mean movie rating computed per year.

# ---------------------------------------- COUNTRY == SWITZERLAND ----------------------------------------
filename = "countries.txt"
with open(filename, "r", encoding="latin-1") as f:
    data = f.readlines()[14:]

print("read file countries.txt")

# swiss_movies contains all swiss movies and its year: swiss_movies([moviename, year])
swiss_movies = []
# fill swiss_token with data
for line in data:
    tokens = line.split()
    # extract only the infos you need to insert them in swiss_token 
    if tokens[-1] == 'Switzerland':
        mov_year = extract_movie_and_year(tokens, 0)
        if mov_year[1] != None and mov_year[1] >= 2000 and mov_year[1] <= 2010:
            # append to the swiss_token list now the moviename and the year of swiss movies
            swiss_movies.append(mov_year)
            
#----------------------------- RATINGS ------------------------------------------------------     
                        
filename = "ratings.txt"
with open(filename, "r", encoding="latin-1") as f:
    data = f.readlines()[297:695711]

print("read file ratings.txt")

# rating_list will contain all movies, their rating, and year. --> rating_list(moviename, year, rating, nr_votes)
rating_list = []

for line in data:
    tokens = line.split()
    rating = tokens[2]
    nr_votes = tokens[1]
    mov_year = extract_movie_and_year(tokens,3)
    mov_year.append(float(rating))
    mov_year.append(int(nr_votes))
    
    # fill rating_list with its data 
    rating_list.append(mov_year)
    
print("rating list created: ", rating_list[15])

# since rating_list is going to be too huge for looping through, we reduce its size for task one and include only movie
# between 2000 and 2010
rating_list_2000_2010 = []

for mov in rating_list:
    if mov[1] != None and mov[1] >= 2000 and mov[1] <= 2010:
        rating_list_2000_2010.append(mov)

# Some "movies" or series such as FIFA champions league have lots of different instances (1 per game). Remove such "duplicates"
unique_swiss_movies = []
for movie in swiss_movies:
    if movie not in unique_swiss_movies:
        unique_swiss_movies.append(movie)
    else:
        pass

print("unique swiss movies created ", unique_swiss_movies[15])

# Get the rating for each movie. For series, the average over all instances is computed
# swiss_movies([moviename, year]), rating_list([moviename, year, rating, nr_votes])


#rating_per_swiss_movie=([movie, year, rating(average)])
rating_per_swiss_movie = []

for movie in unique_swiss_movies:
    counter = 0
    rating_sum = 0
    for rating in rating_list_2000_2010:
        if movie[0] == rating[0] and movie[1] == rating[1]:
            counter = counter + 1
            rating_sum = rating_sum + rating[2]
    if counter != 0:
        avg_rating = rating_sum / counter
        rating_per_swiss_movie.append([movie[0], movie[1], avg_rating]) 
        
print("rating per swiss movie created ", rating_per_swiss_movie[15])

#Now we need to sort the list by year (increasing) from 2000 - 2010
sorted_rating_per_swiss_movie = sorted(rating_per_swiss_movie, key=lambda x: x[1])

print("sorted rating per swiss movie, example tuple: ", sorted_rating_per_swiss_movie[15])


import collections
# Get average (for swiss movies) per year
lastmovie = []
average_per_year = {}
counter = 0
sum_year = 0
for m in range(len(sorted_rating_per_swiss_movie)):
    # same year
    if sorted_rating_per_swiss_movie[m][1] == sorted_rating_per_swiss_movie[m-1][1]:
        counter = counter + 1
        sum_year = sum_year + sorted_rating_per_swiss_movie[m][2]
    if m == len(sorted_rating_per_swiss_movie) - 1:
        average_per_year[sorted_rating_per_swiss_movie[m][1]] = sum_year / counter
    # new year
    else:
        # first one
        if counter == 0:
            counter = counter + 1
            sum_year = sum_year + sorted_rating_per_swiss_movie[m][2] 
        else:
            average_per_year[sorted_rating_per_swiss_movie[m-1][1]] = sum_year / counter
            counter = 1
            sum_year = 0 + sorted_rating_per_swiss_movie[m][2]
print(average_per_year)
        
sorted_avg = collections.OrderedDict(sorted(average_per_year.items()))

# The y axis is going to be the rating
# The x axis: year (2000-2010)
# Create a bar graph, where each bar contains the name of the movie --> "grouped bar chart"


# include: the average rating of the movies per year
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

x_data = []
for x in range(2000,2011):
    x_data.append(x)
    
print(x_data)

bar_list = []

for movie in sorted_rating_per_swiss_movie:
    none_list = [None] * 11
    none_list[movie[1] - 2000] = movie[2]
    trace = go.Bar(
        x = x_data,
        y = none_list,
        name=movie[0]
    )

    bar_list.append(trace)

liste = []
for y in range(2000,2011):
    liste.append(sorted_avg[y])
      
print(liste)
# Include the average here
trace2 = go.Scatter(
    x = x_data,
    y = liste
)

bar_list.append(trace2)

layout = go.Layout(
    title='Rating of Swiss Movies',
    xaxis=dict(
        title='Year'),
    yaxis=dict(
        title='Rating'),
    showlegend=False
)

data = bar_list
fig = go.Figure(data=data, layout=layout)

py.iplot(fig, filename='t1')






############################################# TASK 2 #################################################################
# Create an IMDb yearly movie count and genre plot --> movies per genre per year
# genre_list(movie, year, genre)

import itertools

# ------------------------------------------- Genres -----------------------------------------------------------------
filename = "genres.txt"
with open(filename, "r", encoding="latin-1") as f:
    data = f.readlines()[383:2398020]

# genre_list will contain all movies, their rating, and year. --> genre_list(movie, year, genre)
genre_list = []
for line in data:
    tokens = line.split()
    genre = tokens[-1]
    mov_year = extract_movie_and_year(tokens, 0)
    mov_year.append(genre)
    # append to the swiss_token list now the moviename and the year  
    genre_list.append(mov_year)
print(genre_list[9])

# first sort genre_list by year
#sorted_genre_list = sorted(genre_list, key=lambda x: x[1])

# Get genres and their corresponding counts
counter = 0
total_counter = 0
genre_dic = {}

#create nested dictionary
for year in range(1995, 2016):
    genre_dic[year]= {}
    
for m in range(len(genre_list)):
    # same year
    if type(genre_list[m][1]) is int:
        if genre_list[m][1] >= 1995 and genre_list[m][1] <= 2015:
            if genre_list[m][2] in genre_dic[genre_list[m][1]]:
                genre_dic[genre_list[m][1]][genre_list[m][2]] = genre_dic[genre_list[m][1]][genre_list[m][2]] + 1
                total_counter = total_counter + 1
            else:
                genre_dic[genre_list[m][1]][genre_list[m][2]] = 1
        
# The x axis is going to be the years, we chose the range from 2000 until 2015
x_data = []
for x in range(1995,2016):
    x_data.append(x)
    
all_genres = []
# get list of all genres
for year in range(1995,2016):
    new_list = list(genre_dic[year].keys())
    for item in new_list:
        all_genres.append(item)
    
all_genres = list(set(all_genres))
print(all_genres)
    
trace_list = []
for genre in all_genres:
    y_data = []
    for year in range(1995,2016):
        if genre in genre_dic[year]:
            y_data.append(genre_dic[year][genre])
        else:
            y_data.append(0)
            
    trace1 = go.Scatter(
    x=x_data,
    y=y_data,
    mode='lines',
    line=dict(width=0.5),
    fill='tonexty',
    name = genre
) 
    trace_list.append(trace1)

                    
data = trace_list
layout = go.Layout(
    title='Movie Count from 1995 - 2015',
    showlegend=True,
    xaxis=dict(
        type='category',
        title="Year"
    ),
    yaxis=dict(
        type='linear',
        title = "Nr. of Movies",
        range=[1, 50000]
    )
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='stacked-area-plot')




############################################# TASK 3 #################################################################
# Create a plot presenting the duration of movies over IMDb score, including also information about the number of
# votes per movie --> movie length, rating, nr. of votes per movie

# ----------------------------------------- Movie Length ---------------------------------------------------------
filename = "running-times.txt"
with open(filename, "r", encoding="latin-1") as f:
    data = f.readlines()[14:1347506]

# genre_list will contain all movies, their rating, and year. --> rating_list(moviename, year, rating)
movie_length = []
for line in data:
    length = None
    tokens = line.split()
    if containsdigit(tokens[-1]) == True:
        if tokens[-1].isdigit() == False:
            length = extractnr(tokens[-1])
        else:
            length = tokens[-1]
    else:
        if containsdigit(tokens[-2]) == True:
            if tokens[-2].isdigit() == False:
                length = extractnr(tokens[-2])
            else:
                length = tokens[-2]
        else:
            if containsdigit(tokens[-3]) == True:
                if containsdigit(tokens[-3]) == True:
                    length = extractnr(tokens[-3])
                else:
                    length = tokens[-3]
            else:
                if containsdigit(tokens[-4]) == True:
                    if containsdigit(tokens[-4]) == True:
                        length = extractnr(tokens[-4])
                    else:
                        length = tokens[-4]
                else:
                    length = tokens[-4]
    print(length)

    mov_year = extract_movie_and_year(tokens, 0)
    mov_year.append(length)

    # append to the swiss_token list now the moviename and the year
    movie_length.append(mov_year)
print(movie_length[9])

# Noch komisch... einigi film ueber 1000 min laengi evtl. eifach ignoriere.... ^^


# ---------------------------------- Rating / Nr. of Votes Per Movie ------------------------------------------------
# included in rating_list(moviename, year, rating, nr_votes)









############################################## Task 4 ###############################################################
# Movie ratings in rating_list, genre in genre_list()

from collections import defaultdict
import functools as ft
import multiprocessing as mp

genre_rating = defaultdict(list)

print(len(genre_list))
print(len(rating_list))


def process_genre_rating():

    for rating in rating_list:
        for genre in genre_list:
            if rating[0] == genre[0] and rating[1] == genre[1]:
                genre_rating[genre[2]].append(rating[2])
                break



pool = mp.Pool()
ratings_list = pool.map(process_genre_rating())


genre__avg = {}
for genre in all_genres:
    genre_avg[genre] = 0


# Calculate average of ratings per genre and store it in a dictionary: genre_avg{["genre":avg]}
rating_sum = 0

for key, value in genre_rating:
    for rating in value:
        rating_sum = rating_sum + rating
        genre_avg[genre] = rating_sum / len(value)
        rating_sum = 0

print(genre_avg)







