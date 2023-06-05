"""
Test functions in StorageJson class
"""
import json
import os
import pytest

from storage_json import StorageJson

TEST_FILE_PATH = '_static/test_movies.json'


def create_test_file():
    """
    A test data file in JSON format is created if it does not exist.
    """
    test_data = {"TestTitanic": {"rating": 7.9,
                                 "year": 1997,
                                 "poster": "https://m.media-amazon.com/images"
                                           "/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTU"
                                           "tMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4Nz"
                                           "Y1MzY@._V1_SX300.jpg",
                                 "notes": "My favourite movie!!",
                                 "website": "https://www.imdb.com/title/tt0120338",
                                 "country": "United States, Mexico"}
                 }
    if not os.path.exists(TEST_FILE_PATH):
        with open(TEST_FILE_PATH, 'w', encoding='utf8') as file:
            json.dump(test_data, file)


def test_list_movies_with_valid_file():
    """
    Test successful list movies
    """
    create_test_file()
    assert StorageJson(TEST_FILE_PATH).list_movies()


def test_list_movies_with_invalid_file_format():
    """
    Test raising ValueError
    with invalid file format
    when listing movies
    """
    with pytest.raises(ValueError):
        StorageJson('_static/movies.csv').list_movies()


def test_list_movies_with_non_exists_file():
    """
    Test raising FileNotFoundError
    with non exists file
    when listing movies
    """
    with pytest.raises(FileNotFoundError):
        StorageJson('_static/mov.json').list_movies()


def test_add_movie_with_valid_inputs():
    """
    Test successful add a movie
    with valid inputs
    """
    create_test_file()
    assert StorageJson(TEST_FILE_PATH) \
        .add_movie('testMovie',
                   5.5,
                   2023,
                   'poster',
                   'https://www.testwebsite.com',
                   'Canada')


def test_add_movie_with_invalid_title():
    """
    Test raising TypeError
    with invalid title
    when adding a new movie
    """
    with pytest.raises(TypeError):
        assert StorageJson('_static/movies.json') \
            .add_movie(123,
                       5.5,
                       2023,
                       'poster',
                       'https://www.testwebsite.com',
                       'Canada')


def test_add_movie_with_invalid_rating():
    """
    Test raising TypeError
    with invalid rating
    when adding a new movie
    """
    with pytest.raises(TypeError):
        assert StorageJson('_static/movies.json') \
            .add_movie('testMovie',
                       5,
                       2023,
                       'poster',
                       'https://www.testwebsite.com',
                       'Canada')


def test_add_movie_with_invalid_year():
    """
    Test raising TypeError
    with invalid year
    when adding a new movie
    """
    with pytest.raises(TypeError):
        assert StorageJson('_static/movies.json') \
            .add_movie('testMovie',
                       5.5,
                       '2023',
                       'poster',
                       'https://www.testwebsite.com',
                       'Canada')


def test_add_movie_with_empty_title():
    """
    Test raising ValueError
    with empty title
    when adding a new movie
    """
    with pytest.raises(ValueError):
        assert StorageJson('_static/movies.json') \
            .add_movie('',
                       5.5,
                       2023,
                       'poster',
                       'https://www.testwebsite.com',
                       'Canada')


def test_delete_movie_with_invalid_title():
    """
    Test raising TypeError
    with invalid title
    when deleting a movie
    """
    with pytest.raises(TypeError):
        assert StorageJson('_static/movies.json') \
            .delete_movie(111)


def test_delete_movie_with_empty_title():
    """
    Test raising ValueError
    with empty title
    when deleting a movie
    """
    with pytest.raises(ValueError):
        assert StorageJson('_static/movies.json') \
            .delete_movie('')


def test_update_movie_with_invalid_title():
    """
    Test raising TypeError
    with invalid title
    when updating a movie
    """
    with pytest.raises(TypeError):
        assert StorageJson('_static/movies.csv') \
            .update_movie(111, 'test notes')


def test_update_movie_with_empty_title():
    """
    Test raising ValueError
    with empty title
    when updating a movie
    """
    with pytest.raises(ValueError):
        assert StorageJson('_static/movies.csv') \
            .update_movie('', 'test notes')


def test_update_movie_with_invalid_notes():
    """
    Test raising TypeError
    with invalid notes
    when updating a movie
    """
    with pytest.raises(TypeError):
        assert StorageJson('_static/movies.csv') \
            .update_movie('test movie', 111)

    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
