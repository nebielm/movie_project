from statistics import median
from random import choice
import movie_storage
import requests


FILE = "data.json"
API_KEY = "2f8ef11f"
API_URL = f"https://www.omdbapi.com/?apikey={API_KEY}&t="


def menu():
    """Create and print the menu for user to choose between
       different commands and let the user choose a command
       through input."""
    print("*" * 10, " My Movies Database ", "*" * 10, "\n")
    menu_list = [
      {"show": "Exit", "execute": lambda: print("Bye!")},
      {"show": "List movies", "execute": list_movies},
      {"show": "Add movie", "execute": add_movie},
      {"show": "Delete movie", "execute": delete_movie},
      {"show": "Update movie", "execute": update_movie},
      {"show": "Status", "execute": status},
      {"show": "Random movie", "execute": random_movie},
      {"show": "Search movie", "execute": search_movie},
      {"show": "Movies sorted by rating", "execute": mov_sort_by_rate},
      {"show": "Generate website", "execute": generate_website}

    ]
    print("Menu:")
    for num, option in enumerate(menu_list):
        print(f"{num}. {option['show']}")
    while True:
        try:
            command_input = int(input(f"\nEnter choice "
                                      f"(0-{len(menu_list)-1}): \n"))
            if command_input in range(len(menu_list)):
                break
            print("You've not chosen a number between 0 and "
                  f"{len(menu_list) - 1}. Try again")
        except Exception:
            print("Your choice is invalid.")
    return command_input, menu_list


def list_movies():
    """Prints all movies and info's in Database"""
    movies = movie_storage.read_file(FILE)
    print(f"{len(movies)} movies in total:\n")
    for movie, info in movies.items():
        print(f"{movie}: {info['rating']} ({info['year']})")
    input("\nTo return to menu press Enter.")


def add_movie():
    """Asks user for new movie, checks if movie is already in
       database and adds new movie with
       rating and year to Database."""
    movies = movie_storage.read_file(FILE)
    while True:
        new_title = input("Add movie name: ")
        if new_title == '':
            print("You've entered nothing. Try again")
        else:
            break
    try:
        res = requests.get(API_URL + new_title)
        movie_dict = res.json()
    except Exception:
        print("It seems your have no internet connection."
              " Try again later.")
        input("\nTo return to menu press Enter.")
        return movies
    if movie_dict["Response"] == "False":
        print(f"Movie with the title {new_title} does not exist.")
        input("\nTo return to menu press Enter.")
        return movies
    elif movie_dict["Title"] in movies:
        print(f"{movie_dict["Title"]} already in Database")
        input("\nTo return to menu press Enter.")
        return movies
    new_title, new_year, new_rating, new_poster, imbd_id = (
        movie_dict["Title"], int(movie_dict["Year"]),
        float(movie_dict["Ratings"][0]["Value"][:-3]), movie_dict["Poster"], movie_dict["imdbID"])
    movie_storage.add_movie(new_title, new_year, new_rating, new_poster, imbd_id)
    print(f"Movie '{new_title}' successfully added to List.")
    input("\nTo return to menu press Enter.")
    return movies


def delete_movie():
    """Asks user for movie to delete, checks if movie is in
       database and deletes it."""
    movies = movie_storage.read_file(FILE)
    while True:
        delete_movie_input = input("Which movie should be deleted? ")
        if delete_movie_input == '':
            print("You've entered nothing. Try again")
        else:
            break
    for movie in movies.keys():
        if delete_movie_input.lower() == movie.lower():
            movie_storage.delete_movie(movie)
            print(f"Movie '{movie}' successfully deleted.")
            input("\nTo return to menu press Enter.")
            return movies
    print(f"Movie '{delete_movie_input}' not in Database")
    input("\nTo return to menu press Enter.")
    return movies


def update_movie():
    """Asks user which movie should be updated, check is movie is
       in database and updates movie with new info's."""
    movies = movie_storage.read_file(FILE)
    while True:
        update_movie_input = input("Which movie should be updated? ")
        if update_movie_input == '':
            print("You've entered nothing. Try again")
        else:
            break
    for movie in movies.keys():
        if update_movie_input.lower() == movie.lower():
            while True:
                movie_note = input("Enter movie notes:  ")
                if len(movie_note) > 0:
                    break
                print("You've entered nothing. Try again")
            movie_storage.update_movie(movie, movie_note)
            print(f"Movie '{movie}' successfully updated.")
            input("\nTo return to menu press Enter.")
            return movies
    print(f"{update_movie_input} not in Database")
    input("\nTo return to menu press Enter.")
    return movies


def status():
    """Calculates average rating and median from rating
       find out which movie is best and worst according to ratings,
       and prints the new gained information."""
    movies = movie_storage.read_file(FILE)
    rating_list = []
    for movie, info in movies.items():
        rating_list.append(info["rating"])
    rating_list.sort()
    avr_rating = sum(rating_list) / len(rating_list)
    med_rating = median(rating_list)
    best_movies = ''
    worst_movies = ''
    for movie, info in movies.items():
        if info["rating"] == rating_list[-1]:
            best_movies = movie
        elif info["rating"] is rating_list[0]:
            worst_movies = movie
    print(f"The average rating in your Database is {avr_rating}.\n"
          f"The Median in your Database is {med_rating}.\n"
          f"Best movies with a {rating_list[-1]} rating: '{best_movies}'\n"
          f"Best movies with a {rating_list[0]} rating: '{worst_movies}'")
    input("\nTo return to press Enter.")


def random_movie():
    """Prints random movie from database."""
    movies = movie_storage.read_file(FILE)
    movies_list = list(movies.keys())
    random_mov = choice(movies_list)
    random_mov_rate = movies[random_mov]["rating"]
    random_mov_year = movies[random_mov]["year"]
    print(f"Random movie recommendation: '{random_mov}' "
          f"(Year: {random_mov_year}, Rating: {random_mov_rate})\n")
    input("To return to the press Enter.")


def search_movie():
    """Searches in database for a movie request from user."""
    movies = movie_storage.read_file(FILE)
    while True:
        movie_name_input = input("Search a movie: ")
        if movie_name_input == '':
            print("You've entered nothing. Try again")
        else:
            break
    for movie in movies:
        if movie_name_input.lower() == movie.lower():
            print(f"Movie found: '{movie}'\n")
            input("\nTo return to the press Enter.")
            return
    print(f"'{movie_name_input}' not found.")
    input("\nTo return to the press Enter.")


def mov_sort_by_rate():
    """Sorts database by ratings and prints it to user."""
    movies = movie_storage.read_file(FILE)
    movies_sorted = dict(sorted(movies.items(),
                         key=lambda item: item[1]["rating"], reverse=True))
    for movie, info in movies_sorted.items():
        print(f"{info['rating']}: {movie} ({info['year']})")
    input("\nTo return to the menu press Enter.")


def generate_website():
    movies = movie_storage.read_file(FILE)
    with open("index_template.html", "r") as fileobj:
        index_templ = fileobj.read()
    title = "NEBIEL'S MOVIE APP"
    movie_grid = ""
    for movie in movies:
        movie_grid += (f'           <li>\n'
                       f'               <div class="movie">\n'
                       f'                   <a href="https://www.imdb.com/title/{movies[movie]["imdbID"]}/" target="_blank">\n'
                       f'                       <img class="movie-poster" src="{movies[movie]["poster"]}" '
                       f'alt="{movie}" title="{movies[movie].get("note", "N/A")}">\n'
                       f'                   </a>\n'
                       f'                   <div class="movie-title">{movie}</div>\n'
                       f'                   <div class="movie-year">{movies[movie]["year"]}</div>\n'
                       f'                   <div class ="rating-bar">\n'
                       f'                       <div class="movie-rating" style="width: '
                       f'{(movies[movie]["rating"])*10}%;">\n'
                       f'                           <span>{movies[movie]["rating"]}/10</span>\n'
                       f'                       </div>\n'
                       f'                   </div>\n'
                       f'               </div>\n'
                       f'           </li>\n')
    first_step = index_templ.replace("__TEMPLATE_TITLE__", title)
    final_output = first_step.replace("        __TEMPLATE_MOVIE_GRID__",
                                      movie_grid)
    with open("index.html", "w") as fileobj:
        fileobj.write(final_output)
        print("Website was generated successfully.")


def main():
    """Create a while loop so that the program execute the
       function according to users choice"""
    while True:
        print()
        command_input, menu_list = menu()
        menu_list[command_input]["execute"]()
        if command_input == 0:
            break


if __name__ == "__main__":
    main()
