from fasthtml.common import *
from .components import movie_details, movie_list
from .data import fetch_movies, process_movies, MOVIE_PAGE_SIZE
from .helper import build_movie_list

app, rt = fast_app(
    live=True,
    hdrs=(
        Style(
            """
            .box {
                display:flex;
                flex-direction: row; 
                align-items: flex-start;
            }

            .details-header {
                display: flex; 
                flex-direction: column;
            }

            .details-header-info {
                display: flex;
                flex-direction: column;
            }

            .details-header-body {
                display: flex;
            }

            .details-header-body div {
                padding-left: 1em;
            }
            
            .details-header-body p {
                margin: 0;
            }
            
            .details-header-body hr {
                margin-top: 0.5em;
                margin-bottom: 0.5em;
            }
            
            .details-header-info h1 {
                padding: 0;
                margin: 0;
            }


            .movie-details {
                padding-top: 1em;
                flex-grow: 1; 
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .details-poster {
                width: 40%;
                height: 100%;
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

movies = []


@app.route("/", methods="get")
def home():
    global movies
    movies = []

    return Div(movie_list(), movie_details(), cls="box")


@app.get("/details/{index}")
def get_details(index: int):
    movie = movies[index]

    info_data = f"{movie["year"]}・{movie["runtime"] // 60}h {movie["runtime"] % 60}m"

    return Div(
        Div(
            Div(
                H1(movie["title"]),
                Div(P(info_data)),
                cls="details-header-info",
            ),
            Div(
                Img(src=movie["poster"], cls="details-poster"),
                Div(
                    P( B("Genres:  "), ', '.join(movie["genres"])),
                    Hr(),
                    P( B("Directors:  "), ', '.join(movie["directors"])),
                    Hr(),
                    P( B("Writers:  "), ', '.join(movie["writers"])),
                    Hr(),
                    P(B("Cast:  "), ', '.join(movie["cast"])),
                    Hr(),
                    P(B("Countries:  "), ', '.join(movie["countries"])),
                ),
                cls="details-header-body",
            ),
            cls="details-header",
        ),
        P(movie["plot"]),
        P(movie["fullplot"]),
        cls="movie-details",
    )


@app.get("/movies")
def get_movies():
    global movies
    global MOVIE_PAGE_SIZE

    page = len(movies) // MOVIE_PAGE_SIZE
    raw_movies = fetch_movies(page)
    new_movies = process_movies(raw_movies)
    movies += new_movies

    return build_movie_list(movies)


serve()
