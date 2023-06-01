"""
StorageCsv class reading and writing to a CSV file.
"""
import csv
from istorage import IStorage
from utils import colors


class StorageCsv(IStorage):
    """
    StorageCsv class inherited IStorage Interface
    that exposes all the 4 CRUD commands.
    It reads and writes to a CSV file.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path

    def _read_file(self) -> str:
        """
        Reading from a CSV file.
        :return: file content (str)
        """
        with open(self._file_path, 'r', encoding='utf8') as file:
            return file.read()

    def _write_line(self, *args):
        """
        Append a movie to movies CSV file.
        :param args: Any
        """
        with open(self._file_path, 'a', encoding='utf8') as file:
            data = ''
            for i, arg in enumerate(args):
                if i == len(args) - 1:
                    data += arg + '\n'
                else:
                    data += arg + ','

            file.writelines(data)

    def _read_lines(self) -> list:
        """
        Reading lines in a csv file
        :return: lines (list)
        """
        lines = []
        with open(self._file_path, 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            for row in reader:
                lines.append(row)
        return lines

    def _write_all_content(self, lines):
        """
        Writing all content to a csv file
        :param lines: list
        """
        with open(self._file_path, 'w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerows(lines)

    def list_movies(self) -> dict | None:
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.
        The function loads the information from the CSV
        file and returns the data.
        :return: movies (dict | None)
        """
        try:
            csv_contents = self._read_lines()
            movies = {}
            for content in csv_contents[1:]:
                movies[content[0]] = {'rating': float(content[1]),
                                      'year': int(content[2]),
                                      'notes': content[3],
                                      'poster': content[4],
                                      'website': content[5],
                                      'country': ",".join(content[6:len(content)])
                                      }
            return movies
        except FileNotFoundError as err:
            print('File not found error:', str(err))
        return None

    def add_movie(self,
                  title: str,
                  rating: float,
                  year: int,
                  poster: str,
                  website: str,
                  country: str) -> str | None:
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
        try:
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

            movies = self._read_file()

            if title in movies:
                return colors.get('red') + \
                    f"Movie '{title}' won't be added as it is already exist." + \
                    colors.get('default')

            self._write_line(title,
                             str(rating),
                             str(year),
                             '',  # notes
                             poster,
                             website,
                             country)

            return colors.get('red') + \
                f"Movie '{title}' was successfully added." + \
                colors.get('default')
        except FileNotFoundError as err:
            print('File not found error:', str(err))
        except TypeError as err:
            print(err)
        return None

    def delete_movie(self, title: str) -> str:
        """
        Deletes a movie from the movies database.
        Loads the information from file, deletes the movie,
        and saves it.
        The function doesn't need to validate the input.
        :param title: str
        :return: delete message (str)
        """
        try:
            if not isinstance(title, str):
                raise TypeError('Title must be string.')

            movies = self._read_file()

            if title in movies:
                lines = self._read_lines()

                for i, line in enumerate(lines):
                    if title == line[0]:
                        # delete a line of content
                        lines.pop(i)

                self._write_all_content(lines)

                return f"{colors.get('red')}" \
                       f"Movie '{title}' successfully deleted." \
                       f"{colors.get('default')}"

        except FileNotFoundError as err:
            print('File not found error:', str(err))
        except TypeError as err:
            print(err)

        return f"{colors.get('red')}" \
               f"Movie '{title}' not found." \
               f"{colors.get('default')}"

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
        try:
            if not isinstance(title, str):
                raise TypeError('Title must be string.')

            if not isinstance(notes, str):
                raise TypeError('Notes must be string.')

            movies = self._read_file()

            if title in movies:
                lines = self._read_lines()

                for line in lines[1:]:
                    if title == line[0]:
                        print(title, line[0])
                        # update a line of content
                        line[3] = notes

                self._write_all_content(lines)

                return f"{colors.get('red')}" \
                       f"Movie '{title}' successfully updated." \
                       f"{colors.get('default')}"

        except FileNotFoundError as err:
            print('File not found error:', str(err))
        except TypeError as err:
            print(err)
        return f"{colors.get('red')}" \
               f"Movie '{title}' not found." \
               f"{colors.get('default')}"
