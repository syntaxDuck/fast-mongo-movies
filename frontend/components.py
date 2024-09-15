from fasthtml.common import *


def movie_list():
    return Div(
        Ul(
            cls="movie-list",
            hx_get=f"/movies",
            hx_trigger="load",
            hx_swap="innerHTML",
        ),
        Button(
            "Next ▷",
            hx_get=f"/movies",
            hx_target=".movie-list",
            hx_swap="innerHTML",
        ),
        cls="movies",
    )


def movie_details():
    return Div(cls="movie-details")


def rating(rating, review_count, source, style_class):
    return Div(
        Img(src=source),
        Div(
            B(f"{rating} / 10"),
            P(review_count),
        ),
        cls=style_class,
    )


def detail(name, key, item):
    if key not in item or item[key] is None:
        return (P(B(f"{name}:  "), "N/A"),)

    if not isinstance(item[key], list):
        item[key] = [item[key]]

    return (P(B(f"{name}:  "), ", ".join(item[key])),)
