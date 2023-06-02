"""
Main class to run movie app from a IStorage object.
"""
import argparse
from movie_app import MovieApp
from storage_csv import StorageCsv
from storage_json import StorageJson


def main():
    """
    Creating and running a movie app
    from a StorageJson object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Movie file path')
    args = parser.parse_args()

    file_path = f'_static/{args.file_path}'

    file_extension = file_path.split('.')[-1]

    storage_classes = {
        'json': StorageJson,
        'csv': StorageCsv
    }

    storage_class = storage_classes.get(file_extension)

    movie_app = MovieApp(storage_class(file_path))
    movie_app.run()


if __name__ == "__main__":
    main()
