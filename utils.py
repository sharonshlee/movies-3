"""
A utility file for global access constants.
"""
colors = {'default': '\033[0m',
          'red': '\033[31m',
          'green': '\033[32m',
          'purple': '\033[35m',
          'orange': '\033[38;5;208m',
          'yellow': '\033[33m',
          'blue': '\033[34m'}

choices = {'0': "Exit movie app",
           '1': "Movies Listings",
           '2': "Adding a movie",
           '3': "Deleting a movie",
           '4': "Updating a movie",
           '5': "Movies Statistics",
           '6': "Get a random movie",
           '7': "Searching movies",
           '8': "Sorting Movies",
           '9': "Movies Ratings Histogram",
           '10': "Generate Movies Website"}


def menu() -> str:
    """
    Display menu and request user input choice of menu.
    """
    return f"""
            {colors.get('orange')}
            Menu:
            0. Exit
            1. List movies
            2. Add movie
            3. Delete movie
            4. Update movie
            5. Stats
            6. Random movie
            7. Search movie
            8. Movies sorted by rating
            9. Create Rating Histogram
            10.Generate website
            {colors.get('default')}
            """


def user_input_choice() -> str:
    """
    Get menu choice from user.
    """
    return input(f"{colors.get('blue')}"
                 f"Enter choice (0-10): "
                 f"{colors.get('default')}")


def exit_app() -> str:
    """
    Exit app statement.
    """
    return "Bye!"
