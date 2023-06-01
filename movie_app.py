"""
MovieApp class
to display menu, user input and
movies functions calling.
"""
import requests

from utils \
    import \
    colors, \
    choices, \
    menu, \
    user_input_choice, \
    exit_app

from istorage import IStorage
from movies_analytics import MovieAnalytics
from movies_website_generation import WebsiteGeneration


class MovieApp:
    """
    MovieApp class
    to display menu, user input and
    movies functions calling.
    """
    _API_KEY = 'YOUR_API_KEY'
    _BASE_URL_KEY = f'http://www.omdbapi.com/?apikey={_API_KEY}'
    _IMDB_BASE_URL = 'https://www.imdb.com/title/'

    def __init__(self, storage: IStorage):
        self._storage = storage

    def _command_list_movies(self) -> str:
        """
        List all the movies with total count, names and ratings.
        :return: movies info (str)
        """
        movies = self._storage.list_movies()
        if not movies:
            return f"{colors.get('red')}" \
                   f"There are no movies in the file." \
                   f"{colors.get('default')}"
        print(
            f"\n{colors.get('green')}There are {colors.get('red')}"
            f"{len(movies)}{colors.get('green')} "
            f"movies in the database.{colors.get('default')}\n")
        return "\n".join(
            [f"{colors.get('purple')}{name}, "
             f"{colors.get('yellow')}{info.get('rating')}"
             f"{colors.get('default')}"
             for name, info in movies.items()])

    def _command_add_movie(self) -> str:
        """
        Adds a movie to the movies database
        based on the movie info
        from OMDBAPI and IMDB websites.
        :return: add message (str)
        """
        title = input('Enter a movie title: ')
        while not title:
            title = input('Enter a movie title: ')

        try:
            response = requests.get(f'{MovieApp._BASE_URL_KEY}&t={title}', timeout=5)
            response.raise_for_status()  # check if there was an error with the request
            response = response.json()

            title = response.get('Title', '')
            year = int(response.get('Year', 0))
            rating = float(response.get('imdbRating', 0))
            poster = response.get('Poster', '')
            website = MovieApp._IMDB_BASE_URL + response.get('imdbID', '')
            country = response.get('Country', '')

            return self._storage.add_movie(title,
                                           rating,
                                           year,
                                           poster,
                                           website,
                                           country)

        except (requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException):
            return f"{colors.get('red')}Request error. \n" \
                   'Check your internet connection and ' \
                   'make sure the website is accessible.' + \
                colors.get('default')

    def _command_update_movie(self) -> str:
        """
        Update a movie's notes based on name.
        :return: update message (str)
        """
        title = input('Enter a movie title: ')
        while not title:
            title = input('Enter a movie title: ')

        notes = input('Enter a movie notes: ')
        while not notes:
            notes = input('Enter a movie notes: ')

        return self._storage.update_movie(title, notes)

    def _command_delete_movie(self) -> str:
        """
        Delete a movie based on title.
        :return: delete message (str)
        """
        title = input('Enter a movie title: ')
        while not title:
            title = input('Enter a movie title: ')
        return self._storage.delete_movie(title)

    def _command_movie_stats(self) -> str:
        """
        Get movie statistics,
        average, median ratings,
        best and worst movies.
        :return: movie statistics (str)
        """
        return MovieAnalytics(self._storage.list_movies()) \
            .get_movie_stats()

    def _command_random_movie(self) -> str:
        """
        Get a random movie name and rating.
        :return: random movie (str)
        """
        return MovieAnalytics(self._storage.list_movies()) \
            .get_random_movie()

    def _command_search_movie(self) -> str:
        """
        Search all the movies by part of the movie name,
        incorrect spelling, case-insensitive.
        :return: search message (str)
        """
        return MovieAnalytics(self._storage.list_movies()) \
            .fuzzy_search()

    def _command_sort_movie(self) -> str:
        """
        Sort movies by rating,
        highest to the lowest rating.
        :return: formatted sorted movie desc (str)
        """
        return MovieAnalytics(self._storage.list_movies()) \
            .sort_movies_by_rating_desc()

    def _command_movie_histogram(self) -> str:
        """
        Create a histogram bar chart
        of the movies by x-axis names and y-axis ratings.
        Save the histogram to a .png file.
        :return: histogram creation message (str)
        """
        return MovieAnalytics(self._storage.list_movies()) \
            .create_rating_histogram()

    def _command_generate_website(self) -> str | None:
        analytics = MovieAnalytics(self._storage.list_movies())
        website = WebsiteGeneration(analytics.sort_movies_by_rating_desc_tuple())
        return website.generate_website()

    def _get_function_name(self) -> dict:
        """
        Get function name based on user input command.
        """
        return {'0': exit_app,
                '1': self._command_list_movies,
                '2': self._command_add_movie,
                '3': self._command_delete_movie,
                '4': self._command_update_movie,
                '5': self._command_movie_stats,
                '6': self._command_random_movie,
                '7': self._command_search_movie,
                '8': self._command_sort_movie,
                '9': self._command_movie_histogram,
                '10': self._command_generate_website
                }

    def run(self):
        """
        To display menu, user input and functions calling.
        """
        print(f"\n{colors.get('yellow')}"
              f"********** My Movies Database **********"
              f"{colors.get('default')}")

        while True:
            print(menu())
            choice = user_input_choice()

            if choice in self._get_function_name():
                # Display subtitle
                print(f"\n--------- {choices.get(choice)} ---------")

                function_name = self._get_function_name().get(choice)

                if choice == '0':
                    print(function_name())
                    break

                print(function_name())
            else:
                # if user input other than 0-10, continue request input
                continue

            print("__________________________________\n")
