"""
Test functions in StorageCsv class
"""
import os
import pytest

from storage_csv import StorageCsv

TEST_FILE_PATH = '_static/test_movies.csv'


def create_test_file():
    """
    A test data file in CSV format is created if it does not exist.
    """
    test_data = """title,rating,year,notes,poster,website,country
testMovie,5.5,2023,,poster,https://www.testwebsite.com,Canada, UK
"""
    if not os.path.exists(TEST_FILE_PATH):
        with open(TEST_FILE_PATH, 'w', encoding='utf8') as file:
            file.write(test_data)


def test_list_movies_with_valid_file():
    """
    Test successful list movies
    """
    create_test_file()
    assert StorageCsv(TEST_FILE_PATH).list_movies()


def test_list_movies_with_invalid_file_format():
    """
    Test raising ValueError
    with invalid file format
    when listing movies
    """
    with pytest.raises(ValueError):
        StorageCsv('_static/test_movies.json').list_movies()


def test_list_movies_with_non_exists_file():
    """
    Test raising FileNotFoundError
    with non exists file
    when listing movies
    """
    with pytest.raises(FileNotFoundError):
        StorageCsv('_static/mov.csv').list_movies()


def test_add_movie_with_valid_inputs():
    """
    Test successful add a movie
    with valid inputs
    """
    create_test_file()
    assert StorageCsv(TEST_FILE_PATH) \
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
        assert StorageCsv(TEST_FILE_PATH) \
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
        assert StorageCsv(TEST_FILE_PATH) \
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
        assert StorageCsv(TEST_FILE_PATH) \
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
        assert StorageCsv(TEST_FILE_PATH) \
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
        assert StorageCsv(TEST_FILE_PATH) \
            .delete_movie(111)


def test_delete_movie_with_empty_title():
    """
    Test raising ValueError
    with empty title
    when deleting a movie
    """
    with pytest.raises(ValueError):
        assert StorageCsv(TEST_FILE_PATH) \
            .delete_movie('')


def test_update_movie_with_invalid_title():
    """
    Test raising TypeError
    with invalid title
    when updating a movie
    """
    with pytest.raises(TypeError):
        assert StorageCsv(TEST_FILE_PATH) \
            .update_movie(111, 'test notes')


def test_update_movie_with_empty_title():
    """
    Test raising ValueError
    with empty title
    when updating a movie
    """
    with pytest.raises(ValueError):
        assert StorageCsv(TEST_FILE_PATH) \
            .update_movie('', 'test notes')


def test_update_movie_with_invalid_notes():
    """
    Test raising TypeError
    with invalid notes
    when updating a movie
    """
    with pytest.raises(TypeError):
        assert StorageCsv(TEST_FILE_PATH) \
            .update_movie('test movie', 111)

    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
