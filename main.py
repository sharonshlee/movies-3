"""
Main class to run movie app from a IStorage object.
"""
from movie_app import MovieApp
from storage_csv import StorageCsv
# from storage_json import StorageJson


def main():
    """
    Creating and running a movie app
    from a StorageJson object.
    """
    # storage = StorageJson('_static/movies.json')
    storage = StorageCsv('_static/movies.csv')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
