import requests

API_ULR = "http://127.0.0.1:8000"
MOVIE_PAGE_SIZE = 10


def fetch_movies(page: int):
    global MOVIE_PAGE_SIZE
    url = f"{API_ULR}/movies?limit=10&skip={page*MOVIE_PAGE_SIZE}"
    params = {"type": "movie"}
    data = requests.get(url, params=params)
    return data.json()


def process_movies(movies: list):
    default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
    for movie in movies:
        if movie["poster"]:
            response = requests.head(movie["poster"], allow_redirects=False)
            if response.status_code != 200:
                movie["poster"] = default_img
        else:
            movie["poster"] = default_img

    return movies
