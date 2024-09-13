from fasthtml.common import *
import requests

app, rt = fast_app(
    live=True,
    hdrs=(
        Style(
            """
            .box {
                display:flex;
                flex-direction: row; 
            }

            .movie-details {
                padding-top: 1em;
                flex-grow: 1; 
                display: flex;
                justify-content: center;
            }

            .movie-details img { background-color: #f2f2f2;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                    transition: transform 0.2s; }

            .movies { max-width: 20%;
                    height: 100vh;
                    padding: 1em;
                    overflow-y: scroll;
                    overflow-x: hidden;
                    box-sizing: border-box;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    display: flex; 
                    flex-direction: column; }

            .movies button { margin: 20px; padding: 2px; }

                     
            .movie-list { margin: 0; padding: 0;list-style-type: none; }
            
            .movie { background-color: #f2f2f2;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                    transition: transform 0.2s; }
            """
        ),
    ),
)

api_url = "http://127.0.0.1:8000"


def movie_list():
    return Div(
        Ul(
            cls="movie-list",
            hx_get="/movies",
            hx_trigger="load",
            hx_swap="innerHTML",
        ),
        Button(
            "Next",
            hx_get="/movies",
            hx_target=".movie-list",
            hx_swap="beforeend",
        ),
        cls="movies",
    )


def movie_details():
    return Div(cls="movie-details")


@app.route("/", methods="get")
def home():
    global page
    page = 0
    return Div(movie_list(), movie_details(), cls="box")


@app.route("/", methods=["post", "put"])
def post_or_put():
    return "got a POST or PUT request"


page = 0
movies = []


@app.get("/details/{index}")
def get_details(index: int):
    return Div(Img(src=movies[index]["poster"]))


@app.get("/movies")
def get_movies():
    global page
    global movies

    url = f"{api_url}/movies?limit=10&skip={page*10}"
    params = {"type": "movie"}
    data = requests.get(url, params=params)
    data = data.json()
    default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"

    count = 0
    list_movies = []
    for movie in data:
        image = default_img
        if movie["poster"]:
            response = requests.head(movie["poster"], allow_redirects=False)
            if response.status_code == 200:
                image = movie["poster"]
            else:
                image = default_img
        else:
            image = default_img

        movies.append(movie)

        list_movies.append(
            Li(
                Img(
                    src=image,
                ),
                P(
                    movie["title"],
                    style="text-align: center; color: black",
                ),
                cls="movie",
                hx_get=f"/details/{count}",
                hx_target=".movie-details",
                hx_swap="innerHTML",
                hx_trigger="click",
            )
        )
        count += 1

    page += 1
    return list_movies


serve()
