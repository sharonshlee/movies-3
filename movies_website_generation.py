"""
Generate movie website from movies file.
"""
from country import get_country_flags


def read_file(file_path: str) -> str:
    """
    Reading from a file.
    """
    with open(file_path, 'r', encoding='utf8') as file:
        return file.read()


def write_file(file_path: str, content: str):
    """
    Writing to a file.
    """
    with open(file_path, 'w', encoding='utf8') as file:
        file.write(content)


def serialize_movie(title: str,
                    info: dict,
                    flag_urls: list) -> str:
    """
    Serialize a movie to html format.
    :param title: str
    :param info: dict
    :param flag_urls: list
    :return: a serialized html movie (str)
    """
    images = ''
    for url in flag_urls:
        if url:
            images += f'\n<img class="movie-flag" src={url} />'

    return f"""
            <li>
                <div class="movie">
                        <a href="{info['website']}">
                            <img class="movie-poster" src={info['poster']} title="{info['notes']}"/>
                        </a>
                        <div class="movie-title">{title}</div>
                        <div class="movie-year">{info['year']}</div>
                        <div class="movie-year">{info['rating']}</div>
                        <div class="movie-year">""" + images + """ </div>
                </div>
            </li>
            """


class WebsiteGeneration:
    """
    Generate movie website from movies file.
    """
    _TEMPLATE_FILE_PATH = '_static/index_template.html'
    _HTML_FILE_PATH = '_static/index.html'

    def __init__(self, sorted_movies: list[tuple[str, dict]]):
        self._sorted_movies = sorted_movies

    def _get_movies(self) -> str:
        """
        Serialize movies from movies file into html format.
        :return: serialized html movies (str)
        """
        return "\n".join([serialize_movie(title,
                                          info,
                                          get_country_flags(info['country'])
                                          )
                          for title, info in self._sorted_movies])

    def generate_website(self) -> str | None:
        """
        Generate index.html file from movies file.
        :return: website generation message (str | None)
        """
        try:
            template = read_file(WebsiteGeneration._TEMPLATE_FILE_PATH)
            content_title = template.replace('__TEMPLATE_TITLE__', 'My Movie App')
            write_file(WebsiteGeneration._HTML_FILE_PATH, content_title)

            template = read_file(WebsiteGeneration._HTML_FILE_PATH)
            content = template.replace('__TEMPLATE_MOVIE_GRID__', self._get_movies())
            write_file(WebsiteGeneration._HTML_FILE_PATH, content)
            return 'Website was generated successfully.'
        except FileNotFoundError as err:
            print('File not found error:', str(err))
        return None
