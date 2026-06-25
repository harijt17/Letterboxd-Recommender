from pydantic import BaseModel


class UploadResponse(BaseModel):

    session_id: str

    profile_file: str

    watched_movies: int

    ratings: int

    reviews: int

    diary_entries: int

    status: str