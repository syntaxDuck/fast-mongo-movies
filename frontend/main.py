from fasthtml.common import *

app, rt = fast_app(live=True)


# @rt("/")
# def get():
#     return Div(P("Hello World!"), hx_get="/change")


# @rt("/change")
# def get():
#     return P("Nice to be here!")


@app.route("/", methods="get")
def home():
    return H1("Hello, World")


@app.route("/", methods=["post", "put"])
def post_or_put():
    return "got a POST or PUT request"


serve()
