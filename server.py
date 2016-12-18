from flask import Flask
#from flask import request

import collections

import json

import multiprocessing as mp

import plotly.graph_objs as go
import plotly.offline as offline
from plotly import tools
import numpy as np

#import pandas as pd


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


#returns [name, year, rating, votes, length]
def processRatingsLine(line): 
    tokens = line.split()
    rating = tokens[2]
    nr_votes = tokens[1]
    mov_year = extract_movie_and_year(tokens,3)
    mov_year.append(float(rating))
    mov_year.append(int(nr_votes))
    mov_year.append(-1)
    return mov_year 
    
    
    
def processMovieLength(line):
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
    mov_year = extract_movie_and_year(tokens, 0)
    mov_year.append(length)
    return mov_year
    
    
    
    
    #returns [name, year, rating, votes, length]
def processRatingsLineT4(line): 
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

filename = "running-times.txt"
with open(filename, "r", encoding="latin-1") as f:
    running_times = f.readlines()[14:1347506]
print("read file: running-times.txt")

filename = "genres.txt"
with open(filename, "r", encoding="latin-1") as f:
    genres = f.readlines()[385:2397982]
print("read file: genres.txt")


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
    #returns [name, year, rating, votes, length]

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
    
    
    # Get average (for swiss movies) per year
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
    
   
############################################# TASK 2 #################################################################
# Create an IMDb yearly movie count and genre plot --> movies per genre per year
# genre_list(movie, year, genre)
    
@app.route('/task2') 
def task2():  
    # genre_list will contain all movies, their rating, and year. --> genre_list(movie, year, genre)
    genre_list = []
    for line in genres:
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
    div = offline.plot(fig,  output_type="div")
    return div;   


    
    
    
    
    
    
############################################# TASK 3 #################################################################
# Create a plot presenting the duration of movies over IMDb score, including also information about the number of
# votes per movie --> movie length, rating, nr. of votes per movie

# ----------------------------------------- Movie Length ---------------------------------------------------------
@app.route('/task3') 
def task3():    

    pool = mp.Pool()

    #array title, year, rating, votes, dummy value -1 for length
    ratings_list = pool.map(processRatingsLine, ratings)
    print("rating list created: ", len(ratings_list))
    
    in_time_range_titles = list(filter(lambda x:x[1] and x[1] >= 2000 and x[1] >= 2010, ratings_list))
    print("rating list in time created: ", len(in_time_range_titles))
    
    #array title, year, length
    length_list = pool.map(processMovieLength, running_times)
    print("length list created: ", len(length_list))
    
    in_time_range_lengths = list(filter(lambda x:x[1] and x[1] >= 2000 and x[1] >= 2010, length_list))
    print("rating list in time created: ", len(in_time_range_lengths))
    
    
    #create a dict (name, duration) from [name, year, duration] Nx3 array
    d = dict(np.array(in_time_range_lengths)[:,[0,2]])
    for element in in_time_range_titles:
        if element[0] in d:
            try: 
                element[2] = float(element[2]) #check that entry is numeric
                element[3] = float(element[3]) #check that entry is numeric
                element[4] = float(d[element[0]]) #check that entry is numeric
            except: print('Exception with: ', element, 'and: ', d[element[0]])
        
    #array title, year, rating, votes, time # data here is valid data because of the filter mechanism
    data_with_length= list(filter(lambda x:x[4] and x[4] > 0 and x[4] < 150, in_time_range_titles))
            
    pool.terminate()
    pool.join()
    
    np_dwl = np.array(data_with_length) #convert to np array
    
    #row: ratings, votes, time
    np_dwl = np.array([np_dwl[:,2],np_dwl[:,3], np_dwl[:,4]], dtype='float') 
    
    print("Starting plot {} {} {} {} {} {}".format( 
          np.min(np_dwl[0,:]), 
          np.max(np_dwl[0,:]),
          np.min(np_dwl[1,:]),
          np.max(np_dwl[1,:]),
          np.min(np_dwl[2,:]),
          np.max(np_dwl[2,:]),
          ))
    
    length = len(np_dwl[0])
    
    x1 = np_dwl[0,:length/3]
    y1 = np_dwl[2,:length/3]
    
    x2 = np_dwl[0,length/3:length/3*2]
    y2 = np_dwl[2,length/3:length/3*2]
    
    x3 = np_dwl[0,length/3*2:]
    y3 = np_dwl[2,length/3*2:]
    
    trace_low_votes =  go.Histogram2dContour(x=x1, y=y1, contours=go.Contours(coloring='heatmap'))
    trace_medium_votes =  go.Histogram2dContour(x=x2, y=y2, contours=go.Contours(coloring='heatmap'), showscale=False)
    trace_mucho_votes =  go.Histogram2dContour(x=x3, y=y3, contours=go.Contours(coloring='heatmap'), showscale=False)
    
    fig = tools.make_subplots(rows=1, cols=3, subplot_titles=('Rating vs Length with low # Votes', 'Rating vs Length with medium # Votes',
                                                              'Rating vs Length with high # Votes'))
    
    fig.append_trace(trace_low_votes, 1, 1)
    fig.append_trace(trace_medium_votes, 1, 2)
    fig.append_trace(trace_mucho_votes, 1, 3)
    
    
    fig['layout']['xaxis1'].update(title='Rating')
    fig['layout']['yaxis1'].update(title='Movie Length')
    
    fig['layout']['xaxis2'].update(title='Rating')
    fig['layout']['yaxis2'].update(title='Movie Length')
    
    fig['layout']['xaxis3'].update(title='Rating')
    fig['layout']['yaxis3'].update(title='Movie Length')
    
    fig['layout'].update(height=600, width=3*600, title='Rating, Movie Length, Nr. Votes')
 
    div = offline.plot(fig,  output_type="div")
    return div;
    
    
 ############################################# TASK 3 ################################################################
@app.route('/task4') 
def task4():       
    pool = mp.Pool()
    ratings_list = pool.map(processRatingsLineT4, ratings)
    print("rating list created: ", len(ratings_list))
    
    
    genres_list = pool.map(processGenres, genres)
    print("genres list created: ", len(genres_list))
    
    rating_d = dict(ratings_list)
    
    for genre_entry in genres_list:
        if genre_entry[0] in rating_d:
            genre_entry[2] = float(rating_d[genre_entry[0]]) 
    
    pool.terminate()
    pool.join()
    
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
        
    return json.dumps(genre_avgs)
    
    
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