"""
IStorage Interface that exposes all the 4 CRUD commands.
Two classed that implement these interfaces:
1. StorageJson
2. StorageCsv
"""
from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    IStorage Interface,
    an abstract class to be implemented by:
    1. StorageJson
    2. StorageCsv
    """

    @abstractmethod
    def list_movies(self) -> dict | None:
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.
        The function loads the information from a
        file and returns the data.
        :return: movies (dict | None)
        """

    @abstractmethod
    def add_movie(self,
                  title: str,
                  rating: float,
                  year: int,
                  poster: str,
                  website: str,
                  country: str) -> str:
        """
        Adds a movie to the movies database.
        Loads the information from file, add the movie,
        and saves it.
        The function doesn't need to validate the input.
        :param title: str
        :param rating: float
        :param year: int
        :param poster: str
        :param website: str
        :param country: str
        :returns: add message (str | None)
        """

    @abstractmethod
    def delete_movie(self, title: str) -> str:
        """
        Deletes a movie from the movies database.
        Loads the information from file, deletes the movie,
        and saves it.
        The function doesn't need to validate the input.
        :param title: str
        :return: delete message (str)
        """

    @abstractmethod
    def update_movie(self, title: str, notes: str) -> str:
        """
        Updates a movie from the movies database.
        Loads the information from file, updates the movie,
        and saves it.
        The function doesn't need to validate the input.
        :param title: str
        :param notes: str
        :return: update message (str)
        """
