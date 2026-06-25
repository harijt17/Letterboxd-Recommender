from pathlib import Path
import json

from unzip_export import extract_export
from validate_export import validate_export
from build_user_profile import build_profile


ZIP_FILE = (
    "data/exports/"
    "letterboxd-harijt17-2026-06-24-07-27-utc.zip"
)

print("=" * 50)
print("LETTERBOXD EXPORT TEST")
print("=" * 50)

# Step 1
print("\n[1] Extracting ZIP...")

export_folder = extract_export(
    ZIP_FILE
)

print(
    f"Extracted to:\n{export_folder}"
)

# Step 2
print("\n[2] Validating export...")

missing = validate_export(
    export_folder
)

if missing:

    print(
        "Missing files:"
    )

    for file in missing:
        print(file)

    exit()

print("Validation passed")

# Step 3
print("\n[3] Building profile...")

profile = build_profile(
    export_folder
)

# Step 4
print("\n[4] Saving profile...")

username = profile[
    "profile"
].get(
    "username",
    "unknown"
)

output_file = (
    Path("data/users")
    / f"{username}.json"
)

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        profile,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Saved:\n{output_file}"
)

# Step 5
print("\nPROFILE SUMMARY")

print(
    f"Watched Movies: "
    f"{len(profile['watched'])}"
)

print(
    f"Ratings: "
    f"{len(profile['ratings'])}"
)

print(
    f"Reviews: "
    f"{len(profile['reviews'])}"
)

print(
    f"Diary Entries: "
    f"{len(profile['diary'])}"
)

print("\nDone!")