import requests


def get_poster(film):
    if film == '':
        return "Oops! Try adding something into the search field."

    api_key = '15d2ea6d0dc1d476efbca3eba2b9bbfb'
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={film}"
    response = requests.get(search_url).json()

    if response['total_results'] > 0:
        movie = response['results'][0]
        print(f"Your search found: {movie['title']}")
        poster_path = movie['poster_path']
        image_url = f"http://image.tmdb.org/t/p/w500/{poster_path}"
        return image_url
    else:
        return False

