from fastapi import FastAPI, Body
from typing import Optional

movies = [
    {"title":"Adventure", "director":"J K rowling","genre":"thriller", "rating" :4.5},
    {"title":"Ghost riders", "director":"John williams","genre":"horror", "rating" :4.0},
    {"title":"Rising youth", "director":"J K Rowling","genre":"romance", "rating" :3.8},
    {"title":"Sherlock holmes","director":"Terry Brian","genre":"thriller", "rating" :3.9},
    {"title":"Dawn & Dusk", "director":"Thomas Moorley","genre":"romance","rating": 4.3}
]


app = FastAPI()


#filter movies by genre
@app.get("/movies")
def get_all_movies(genre : str = None):
    if genre:
        mv_list = []
        for movie in movies:
            if genre.casefold() == movie.get('genre').casefold():
                mv_list.append(movie)
        return mv_list
    return movies


#get movie by title
@app.get("/movies/bytitle/{title}")
def get_movie_by_title(title : str):
    mv_list = []
    for movie in movies:
        if movie.get('title').casefold() == title.casefold():
            mv_list.append(movie)
    return mv_list

# Get all movies by a director
@app.get("/movies/bydirector/{director_name}")
def get_movie_by_director(director_name: str, genre: str = None):
    mv_list = []
    for i in range(len(movies)):
        if movies[i].get('director').casefold() != director_name.casefold():
            continue
        if genre is not None and genre.casefold() != movies[i].get('genre').casefold():
            continue
        mv_list.append(movies[i])
    return mv_list


#add movie
@app.post("/movies/add_movie/")
def add_movie(create_movie = Body()):
    movies.append(create_movie)
    return {"message": "Movie added successfully", "movie": create_movie}

#update movie
@app.put("/movies/update_movie/{title}")
def update_movie(title : str,updated_movie = Body()):
    for i in range(len(movies)):
        if title.casefold() ==  movies[i].get("title").casefold():
            movies[i] = updated_movie
            return {"message": "movie updated successfully", "movie": updated_movie}


#delete movie
@app.delete("/movies/delete_movie/{title}")
def delete_movie(title : str):
    for i in range(len(movies)):
        if title.casefold() == movies[i].get('title').casefold():
            deleted_movie = movies.pop(i)
            return {"message":"Movie delted successfully","movie": deleted_movie}
    return {"error": "Movie not found"}



# /movies/search
# Requirements

# Use multiple query params:

# title
# director
# genre
# min_rating
# max_rating

@app.get("/movies/search")
def search_by_query(title : Optional[str] = None, director: Optional[str] = None,\
    genre: Optional[str] = None, min_rating: Optional[float] = None, max_rating: Optional[float] = None)->list:
    movie_list = []
    for movie in movies:
        if title is not None and movie['title'].casefold() != title.casefold():
            continue
        if director is not None and movie['director'].casefold() != director.casefold():
            continue
        if genre is not None and movie['genre'].casefold() != genre.casefold():
            continue
        if min_rating is not None and movie['rating'] < min_rating:
            continue
        if max_rating is not None and movie['rating'] > max_rating:
            continue

        movie_list.append(movie)

    return movie_list if movie_list else {"message":"no movie found"}


    