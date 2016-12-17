from flask import Flask
from flask import request

from multiprocessing import Pool

import plotly.graph_objs as go
import plotly.offline as offline
from plotly import tools
import numpy as np

import pandas as pd


############################################# Helper ################################################################
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


############################################# Load Data ################################################################

#countries


filename = "countries.txt"
with open(filename, "r", encoding="latin-1") as f:
    countries = f.readlines()[14:]
print("read file countries.txt")


filename = "ratings.txt"
with open(filename, "r", encoding="latin-1") as f:
    ratings = f.readlines()[297:695711]
print("read file ratings.txt")


############################################# Start Server ################################################################
offline.init_notebook_mode() 
app = Flask(__name__, static_url_path='/static')



@app.route('/')
def root():
    return app.send_static_file('index.html')


############################################# TASK 1 ################################################################
@app.route('/task1') 
def task1():
    # ---------------------------------------- COUNTRY == SWITZERLAND ----------------------------------------

    
    # swiss_movies contains all swiss movies and its year: swiss_movies([moviename, year])
    swiss_movies = []
    # fill swiss_token with data
    for line in countries:
        tokens = line.split()
        # extract only the infos you need to insert them in swiss_token 
        if tokens[-1] == 'Switzerland':
            mov_year = extract_movie_and_year(tokens, 0)
            if mov_year[1] != None and mov_year[1] >= 2000 and mov_year[1] <= 2010:
                # append to the swiss_token list now the moviename and the year of swiss movies
                swiss_movies.append(mov_year)
                
    #----------------------------- RATINGS ------------------------------------------------------     
    
    # rating_list will contain all movies, their rating, and year. --> rating_list(moviename, year, rating, nr_votes)
    rating_list = []
    
    for line in ratings:
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
     #       ,marker=dict(
    #            line=dict(
    #            width=50))
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
    div = offline.plot(fig,  output_type="div")
    return div;   
    
    
    
    
    
    
    
    
    
    
    
    
    
@app.route('/test')
def test():

    x = np.random.randn(2000)
    y = np.random.randn(2000)

    data = [
        go.Histogram2dContour(x=x, y=y, contours=go.Contours(coloring='heatmap')),
        go.Scatter(x=x, y=y, mode='markers', marker=go.Marker(color='white', size=3, opacity=0.3))
    ]

    layout = go.Layout(
        title="Test",
        autosize=False,
        width=500,
        height=500,
        xaxis=dict(title="Testx"),
        yaxis=dict(title="Testy")
    )
    fig = go.Figure(data=data, layout=layout)
    div = offline.plot(fig,  output_type="div")
    return div;