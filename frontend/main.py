from fasthtml.common import *
import requests

app, rt = fast_app(live=True)


# @rt("/")
# def get():
#     return Div(P("Hello World!"), hx_get="/change")


# @rt("/change")
# def get():
#     return P("Nice to be here!")

api_url = "http://127.0.0.1:8000"


@app.route("/", methods="get")
def home():
    url = f"{api_url}/movies"
    params = {"type": "movie"}
    data = requests.get(url, params=params)
    data = data.json()
    # return Img(src=data[1]["poster"], style="width: 10%")
    stock = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
    movies = []
    for movie in data:
        if movie["poster"]:
            movies.append(
                Img(src=movie["poster"])
                + P(
                    movie["title"],
                    style="text-align: center; color: black",
                )
            )
        else:
            movies.append(
                Img(src=stock)
                + P(movie["title"], style="text-align: center; color: black")
            )

    return Div(
        Ul(
            (
                Li(
                    (movie),
                    style="""background-color: #f2f2f2;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                        transition: transform 0.2s;""",
                )
                for movie in movies
            ),
            style="margin: 0; padding: 0;list-style-type: none;",
        ),
        style=(
            """max-width: 20%;
            height: 100vh;
            padding: 20px;
            overflow-y: scroll;
            overflow-x: hidden;
            box-sizing: border-box;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);"""
        ),
    )


@app.route("/card", methods="get")
def card_3d_demo():
    """This is a standalone isolated Python component.
    Behavior and styling is scoped to the component."""

    def card_3d(text, background, amt, left_align):
        # JS and CSS can be defined inline or in a file
        # scr = ScriptX("card3d.js", amt=amt)
        align = "left" if left_align else "right"
        sty = StyleX("", background=f"url({background})", align=align)
        return Div(text, Div(), sty, "")

    # Design credit: https://codepen.io/markmiro/pen/wbqMPa
    url = f"{api_url}/movies"
    params = {"type": "movie"}
    data = requests.get(url, params=params)
    data = data.json()
    card = card_3d("Mouseover me", data[0]["poster"], amt=1.5, left_align=True)
    return Div(card, style=None)


@app.route("/", methods=["post", "put"])
def post_or_put():
    return "got a POST or PUT request"


serve()
