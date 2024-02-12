from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "API peliculas"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Aqui va la peli", min_length=2, max_length=50)
    overview: str = Field(default="aqui va la sinopsis", max_length=100)
    year: str = Field(default="aqui va el año")
    rating: float = Field(le=10, ge=0)
    category: str = Field(default="aqui va la categoria/genero")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "ASD123456",
                "year": "2022",
                "rating": 9.8,
                "category": "Acción"

            }
        }


movies = [
    {
        "id": 1,
        "title": "Her",
        "overview": "la mejor peli del fokin world",
        "year": "2013",
        "rating": 7.5,
        "category": "drama"
    },
    {
        "id": 2,
        "title": "interstellar",
        "overview": "la otra mejor peli del fokin world",
        "year": "2014",
        "rating": 9.5,
        "category": "fiction"
    },
    {
        "id": 3,
        "title": "Cowboy Bebop: The Movie",
        "overview": "baaanggg",
        "year": "2016",
        "rating": 8.0,
        "category": "western"
    }
]


@app.get("/", tags=["Home"])
def read_root():
    return HTMLResponse("<h1>Bienvenido a la API de peliculas</h1>", status_code=200)


@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200)
def read_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content=movie)
    return HTMLResponse("<h1>No se encontro la pelicula</h1>", status_code=404)


@app.get("/movies/category/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=18)) -> List[Movie]:
    filtered_by_category = [movie for movie in movies if movie["category"] == category]
    return JSONResponse(content=filtered_by_category)


@app.get("/movies/year/", tags=["movies"], response_model=List[Movie])
def get_movies_by_year(year: str) -> List[Movie]:
    filtered_by_year = [movie for movie in movies if movie["year"] == year]
    return JSONResponse(content=filtered_by_year)


@app.post("/movies", tags=["movies"], status_code=201, response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "pelicula creada con exito"}, status_code=201), movies


@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def modify_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
        return JSONResponse(status_code=200, content={"message": "se ha modificado correctamente la pelicula"}), movie


@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
        return JSONResponse(status_code=200, content={"message": "se ha eliminado exitosamente la plicula"}), movies