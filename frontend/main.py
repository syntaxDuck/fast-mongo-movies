from fasthtml.common import *
import requests

app, rt = fast_app(live=True)


# @rt("/")
# def get():
#     return Div(P("Hello World!"), hx_get="/change")


# @rt("/change")
# def get():
#     return P("Nice to be here!")


@app.route("/", methods="get")
def home():
    url = "http://127.0.0.1:8000/users"
    params = {"name": "Ros"}
    data = requests.get(url, params=params)
    return H1(f"Hello, World, {data.json()}")


@app.route("/", methods=["post", "put"])
def post_or_put():
    return "got a POST or PUT request"


serve()
