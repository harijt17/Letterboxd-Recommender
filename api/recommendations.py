from pathlib import Path
import json

from fastapi import (
    APIRouter,
    HTTPException
)

from recommender.recommend import (
    Recommender
)


router = APIRouter()

recommender = Recommender()


@router.get(
    "/recommend/{session_id}"
)
def get_recommendations(
    session_id: str,
    limit: int = 50
):

    user_dir = (
        Path("Data/users")
        / session_id
    )

    matched_profile_path = (
        user_dir
        / "matched_profile.json"
    )

    if not matched_profile_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    result = (
        recommender.recommend(
            matched_profile_path,
            limit
        )
    )

    recommendations_path = (
        user_dir
        / "recommendations.json"
    )

    with open(
        recommendations_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )

    return {

        "session_id":
            session_id,

        **result
    }