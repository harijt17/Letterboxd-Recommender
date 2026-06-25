from pathlib import Path
import json

from ingestion.unzip_export import (
    extract_export
)

from ingestion.validate_export import (
    validate_export
)

from ingestion.build_user_profile import (
    build_profile
)

from matching.enrich_profile import (
    ProfileEnricher
)

from profiling.taste_profile_builder import (
    TasteProfileBuilder
)


class ExportPipeline:

    def __init__(self):

        self.enricher = (
            ProfileEnricher()
        )

        self.taste_builder = (
            TasteProfileBuilder()
        )

    def process_export(
        self,
        zip_path,
        session_id
    ):

        # Extract

        extract_dir = (
            extract_export(
                zip_path
            )
        )

        # Validate

        validation = (
            validate_export(
                extract_dir
            )
        )

        if not validation["valid"]:

            raise ValueError(
                f"Missing files: "
                f"{validation['missing_files']}"
            )

        # User folder

        user_dir = (
            Path("Data/users")
            / session_id
        )

        user_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------
        # profile.json
        # --------------------

        profile = (
            build_profile(
                extract_dir
            )
        )

        profile_path = (
            user_dir
            / "profile.json"
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

        # --------------------
        # matched_profile.json
        # --------------------

        matched_path = (
            user_dir
            / "matched_profile.json"
        )

        match_stats = (
            self.enricher
            .enrich_profile(
                profile_path,
                matched_path
            )
        )

        # --------------------
        # taste_profile.json
        # --------------------

        taste_path = (
            user_dir
            / "taste_profile.json"
        )

        taste_stats = (
            self.taste_builder
            .build_profile(
                matched_path,
                taste_path
            )
        )

        return {

            "session_id":
                session_id,

            "profile_file":
                str(
                    profile_path
                ),

            "matched_file":
                str(
                    matched_path
                ),

            "taste_file":
                str(
                    taste_path
                ),

            "match_stats":
                match_stats,

            "taste_stats":
                taste_stats,

            "profile_stats":
                profile.get(
                    "profile_stats",
                    {}
                )
        }