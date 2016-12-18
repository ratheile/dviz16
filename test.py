import functools as ft
import multiprocessing as mp
import numpy as np

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


filename = "ratings.txt"
with open(filename, "r", encoding="latin-1") as f:
    ratings = f.readlines()[297:695711]
print("read file: ratings.txt")

filename = "running-times.txt"
with open(filename, "r", encoding="latin-1") as f:
    running_times = f.readlines()[14:1347506]
print("read file: running-times.txt")

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
data_with_length= list(filter(lambda x:x[4] and x[4] > 0 and x[4] < 1000, in_time_range_titles))
        
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


x = np_dwl[0,:]
y = np_dwl[2,:]

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
offline.plot(fig, filename='t1')
