"""
StorageCsv class reading and writing to a JSON file.
"""
import json

from istorage import IStorage
from utils import colors, check_file_path


class StorageJson(IStorage):
    """
    StorageJson class inherited IStorage Interface
    that exposes all the 4 CRUD commands.
    It reads and writes to a JSON file.
    """
    def __init__(self, file_path: str):
        self._file_path = file_path

    def _read_file(self):
        """
        Reading from a JSON file.
        """
        check_file_path(self._file_path, '.json')

        with open(self._file_path, 'r', encoding='utf8') as handle:
            return json.load(handle)

    def _write_file(self, movies: dict):
        """
        Writing to a JSON file.
        """
        check_file_path(self._file_path, '.json')

        with open(self._file_path, 'w', encoding='utf8') as file:
            json.dump(movies, file)

    def list_movies(self) -> dict:
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.
        The function loads the information from the JSON
        file and returns the data.
        :return: movies (dict)
        """
        return self._read_file()

    def add_movie(self,
                  title: str,
                  rating: float,
                  year: int,
                  poster: str,
                  website: str,
                  country: str) -> str:
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        :param title: str
        :param rating: float
        :param year: int
        :param poster: str
        :param website: str
        :param country: str
        :returns: add message (str)
        """
        if not isinstance(title, str):
            raise TypeError('Title must be string.')
        if not isinstance(rating, float):
            raise TypeError('Rating must be float.')
        if not isinstance(year, int):
            raise TypeError('Year must be int.')
        if not isinstance(poster, str):
            raise TypeError('Poster must be string.')
        if not isinstance(website, str):
            raise TypeError('Website must be string.')
        if not isinstance(country, str):
            raise TypeError('Country must be string.')

        if not title:
            raise ValueError('Title must not be empty.')
        if not rating:
            raise ValueError('Rating must not be empty.')

        movies = self.list_movies()

        if title in movies:
            return colors.get('red') + \
                f"Movie '{title}' won't be added as it is already exist." + \
                colors.get('default')

        movies[title] = {'rating': rating,
                         'year': year,
                         'notes': '',
                         'poster': poster,
                         'website': website,
                         'country': country
                         }

        self._write_file(movies)

        return colors.get('red') + \
            f"Movie '{title}' was successfully added." + \
            colors.get('default')

    def delete_movie(self, title: str) -> str:
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        :param title: str
        :return: delete message (str)
        """
        if not isinstance(title, str):
            raise TypeError('Title must be string.')

        if not title:
            raise ValueError('Title must not be empty.')

        movies = self.list_movies()

        if title in movies:
            del movies[title]

            self._write_file(movies)

            return f"{colors.get('red')}" \
                   f"Movie '{title}' successfully deleted." \
                   f"{colors.get('default')}"

        return f"{colors.get('red')}" \
               f"Movie '{title}' not found." \
               f"{colors.get('default')}"

    def update_movie(self, title: str, notes: str) -> str:
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        :param title: str
        :param notes: str
        :return: update message (str)
        """
        if not isinstance(title, str):
            raise TypeError('Title must be string.')
        if not isinstance(notes, str):
            raise TypeError('Notes must be string.')

        if not title:
            raise ValueError('Title must not be empty.')

        movies = self.list_movies()

        if title in movies:
            movies[title]['notes'] = notes

            self._write_file(movies)

            return colors.get('red') + \
                f"Movie '{title}' successfully updated." + \
                colors.get('default')

        return colors.get('red') + \
            f"Movie '{title}' not found." + \
            colors.get('default')
