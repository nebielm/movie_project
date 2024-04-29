import json


file = "data.json"


def read_file(file):
    """
    Reads a Json file and returns it as a python object
    """
    with open(file, "r") as json_data:
        movie_data = json.load(json_data)
    return movie_data


def write_file(file, python_obj):
    """
    Converts Python object to a json string and writes a file.
    """
    with open(file, "w") as json_data:
        json.dump(python_obj, json_data)


def add_movie(title, year, rating, poster):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movie_data = read_file(file)
    movie_data[title] = {"rating": rating, "year": year, "poster": poster}
    write_file(file, movie_data)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movie_data = read_file(file)
    movie_data.pop(title)
    write_file(file, movie_data)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movie_data = read_file(file)
    movie_data[title]["rating"] = rating
    write_file(file, movie_data)
