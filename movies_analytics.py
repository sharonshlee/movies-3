"""
Movies analytics provides
search, sorting and
movies statistics on
average, median, best, and worst movie
"""
import random
from fuzzywuzzy import fuzz

from matplotlib import pyplot as plt

from utils import colors


def get_median(ratings: list) -> float:
    """
    Calculate the median of a list of ratings.
    :param ratings: list
    :return: median for ratings (float)
    """
    ratings.sort()
    # Find the middle value(s) of the sorted list.
    numbers = len(ratings)
    if numbers % 2 == 0:
        return (ratings[numbers // 2 - 1] + ratings[numbers // 2]) / 2

    return ratings[numbers // 2]


def get_median_scores(scores: dict) -> float:
    """
    Get median scores of the movies.
    :param scores: dict
    :return: median scores (float)
    """
    # Get the values of the dictionary and store them in a list.
    ratings = list(scores.values())
    return get_median(ratings)


class MovieAnalytics:
    """
    Movies analytics class:
    search, sorting and
    movies statistics on
    average, median, best, and worst movie
    """

    def __init__(self, movies: dict):
        self._movies = movies

    def _get_median_rating(self) -> float:
        """
        Get median rating of the movies.
        :return: median for ratings (float)
        """
        # Get the values of the dictionary and store them in a list.
        ratings = [info['rating'] for title, info in self._movies.items()]
        # Sort the list in ascending order.
        return get_median(ratings)

    def fuzzy_search(self) -> str:
        """
        Search all the movies by part of the movie name,
        incorrect spelling, case-insensitive.
        :return: search message (str)
        """
        name = input('Enter a movie title: ')
        # Dictionary to store similarity scores for each movie name
        scores = {}
        for key in list(self._movies.keys()):
            ratio = fuzz.ratio(name.lower(), key.lower())
            scores[key] = ratio

        # if score is 100 means movie name entered has the exact match in the movies dict.
        if 100 in scores.values():
            return [f"\nSearch result for {colors.get('red')}'{name}'"
                    f"{colors.get('default')}:\n"
                    f"{colors.get('purple')}{title}, "
                    f"{colors.get('yellow')}{info.get('rating')} - "
                    f"{info.get('year')}{colors.get('default')}"
                    for title, info in self._movies.items()
                    if title.lower() == name.lower()][0]

        # no exact match, need recommendations

        # find the median score
        median_score = get_median_scores(scores)

        # get the scores that is above the median score, return top half of the results.
        recommended_names = {}
        for title, score in scores.items():
            if score >= median_score:
                recommended_names[title] = score

        # sort descending to get the top score
        recommended_names_desc_tuple = sorted(recommended_names.items(),
                                              key=lambda x: x[1], reverse=True)

        not_found_message = f"{colors.get('red')}" \
                            f"Movie '{name}' does not exist." \
                            f"{colors.get('default')}"

        if median_score == 0:
            return f"\n{not_found_message}"

        matches_result = "\n".join(f"{colors.get('purple')}{name[0]}, "
                                   f"{colors.get('yellow')}"
                                   f"{self._movies.get(name[0])['rating']} - "
                                   f"{self._movies.get(name[0])['year']}"
                                   f"{colors.get('default')}"
                                   for name in recommended_names_desc_tuple)

        return f"\n{not_found_message}\n" \
               f"{colors.get('red')}Did you mean:" \
               f"{colors.get('default')}\n\n" \
               f"{matches_result}"

    def _get_average_rating(self) -> float:
        """
        Get average rating of the movie.
        :return: average rating (float)
        """
        return sum(info.get('rating')
                   for title, info
                   in self._movies.items()) / len(self._movies)

    def sort_movies_by_rating_desc_tuple(self) -> list[tuple[str, dict]]:
        """
        Sort movies by rating descending,
        highest to the lowest rating
        :return: sorted movies desc (list[tuple[str, dict])
        """
        return sorted(self._movies.items(),
                      key=lambda x: x[1]['rating'],
                      reverse=True)

    def _get_best_movie(self, best: bool = True) -> str:
        """
        Get the best or worst movie by rating.
        :param best: bool
        :return: best or worst movie (str)
        """
        # sort the rating by desc
        movies_desc_tuple = self.sort_movies_by_rating_desc_tuple()

        if best:
            # the highest rating (the first rating in tuple)
            tuple_index = 0
            word = 'Best'
        else:
            # the lowest rating (the last rating in tuple)
            tuple_index = -1
            word = 'Worst'

        movies = [
            f"{colors.get('purple')}"
            f"{title}-{colors.get('yellow')}"
            f"{info['rating']}-{info['year']}"
            f"{colors.get('default')}"
            for title, info in movies_desc_tuple
            if info['rating'] == movies_desc_tuple[tuple_index][1]['rating']]

        return f"{colors.get('green')}{word} movie(s): {', '.join(movies)}"

    def get_movie_stats(self) -> str:
        """
        Get movie statistics,
        average, median ratings,
        best and worst movies.
        :return: move statistics (str)
        """
        return f"{colors.get('green')}" \
               f"Average rating: {colors.get('yellow')}" \
               f"{self._get_average_rating():.2f}" \
               f"{colors.get('default')}\n{colors.get('green')}" \
               f"Median rating: {colors.get('yellow')}" \
               f"{self._get_median_rating():.2f}" \
               f"{colors.get('default')}\n" \
               f"{self._get_best_movie()}\n" \
               f"{self._get_best_movie(False)}"  # worst movie

    def get_random_movie(self) -> str:
        """
        Get a random movie name and rating.
        :return: random movie (str)
        """
        # use random.choice to return random items in the list of movies
        title, info = random.choice(list(self._movies.items()))
        return f"{colors.get('purple')}{title}, " \
               f"{colors.get('yellow')}{info['rating']}-{info['year']}" \
               f"{colors.get('default')}"

    def sort_movies_by_rating_desc(self) -> str:
        """
        Sort movies by rating,
        highest to the lowest rating.
        :return: formatted sorted movie desc (str)
        """
        return "\n".join(
            [f"{colors.get('purple')}{title}, "
             f"{colors.get('yellow')}{info['rating']}-{info['year']}"
             f"{colors.get('default')}"
             for title, info in self.sort_movies_by_rating_desc_tuple()])

    def create_rating_histogram(self) -> str:
        """
        Create a histogram bar chart
        of the movies by x-axis names and y-axis ratings.
        Save the histogram to a .png file.
        :return: histogram creation message (str)
        """
        ratings = [info['rating'] for title, info in self._movies.items()]
        plt.bar(self._movies.keys(), ratings)

        # add the names to the body of the bars
        for index, rating in enumerate(ratings):
            plt.text(index, rating,
                     list(self._movies.keys())[index],
                     ha='center', rotation=90, va='top')

        plt.title('Movies Ratings')
        plt.xlabel('Movies Names')
        plt.ylabel('Ratings')

        # save plot to file
        file_name = ''
        while not file_name.endswith('.png'):
            file_name = input(
                f"{colors.get('yellow')}"
                f"Enter a file name to save the histogram ends with '.png': "
                f"\n{colors.get('default')}")

        plt.savefig(f'_static/{file_name}')

        return f"\n{colors.get('red')}" \
               f"'{file_name}' file has been created." \
               f"{colors.get('default')}"
