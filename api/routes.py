from uuid import uuid4
from pathlib import Path
import shutil
import json

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Body
)

from api.services import (
    ExportPipeline
)

from matching.enrich_profile import (
    ProfileEnricher
)

from profiling.taste_profile_builder import (
    TasteProfileBuilder
)


router = APIRouter()

pipeline = ExportPipeline()

enricher = ProfileEnricher()

taste_builder = (
    TasteProfileBuilder()
)


@router.post("/upload")
async def upload_export(
    file: UploadFile = File(...)
):

    if not file.filename.endswith(
        ".zip"
    ):

        raise HTTPException(
            status_code=400,
            detail="Please upload a ZIP file"
        )

    session_id = (
        uuid4()
        .hex[:12]
    )

    exports_dir = Path(
        "Data/exports"
    )

    exports_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    zip_path = (
        exports_dir /
        f"{session_id}.zip"
    )

    with open(
        zip_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:

        result = (
            pipeline.process_export(
                zip_path,
                session_id
            )
        )

        return {

            "status":
                "success",

            **result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post(
    "/favorites/{session_id}"
)
def save_favorites(
    session_id: str,
    favorites: list[str] = Body(...)
):

    user_dir = (
        Path("Data/users")
        / session_id
    )

    profile_path = (
        user_dir
        / "profile.json"
    )

    if not profile_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    with open(
        profile_path,
        "r",
        encoding="utf-8"
    ) as f:

        profile = json.load(f)

    profile["favorites"] = (
        favorites
    )

    with open(
        profile_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            profile,
            f,
            indent=4,
            ensure_ascii=False
        )

    # -------------------------
    # Rebuild matched profile
    # -------------------------

    matched_path = (
        user_dir
        / "matched_profile.json"
    )

    match_stats = (
        enricher.enrich_profile(
            profile_path,
            matched_path
        )
    )

    # -------------------------
    # Rebuild taste profile
    # -------------------------

    taste_path = (
        user_dir
        / "taste_profile.json"
    )

    taste_stats = (
        taste_builder.build_profile(
            matched_path,
            taste_path
        )
    )

    return {

        "status":
            "saved",

        "favorites_count":
            len(favorites),

        "favorites":
            favorites,

        "match_stats":
            match_stats,

        "taste_stats":
            taste_stats
    }
@router.get(
    "/watched/{session_id}"
)
def get_watched_movies(
    session_id: str
):

    user_dir = (
        Path("Data/users")
        / session_id
    )

    profile_path = (
        user_dir
        / "profile.json"
    )

    if not profile_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    with open(
        profile_path,
        "r",
        encoding="utf-8"
    ) as f:

        profile = json.load(f)

    watched = profile.get(
        "watched",
        []
    )

    movies = []

    for movie in watched:

        title = (
            movie.get("Name")
            or movie.get("Title")
            or movie.get("title")
        )

        if title:

            movies.append(
                title
            )

    movies = sorted(
        list(set(movies))
    )

    return {

        "count":
            len(movies),

        "movies":
            movies
    }

@router.get("/test")
def test():

    return {

        "message":
            "routes working"
    }