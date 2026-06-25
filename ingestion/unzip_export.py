from pathlib import Path
import zipfile
import shutil


def extract_export(zip_path: str):

    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(
            f"ZIP file not found: {zip_path}"
        )

    extract_dir = (
        Path("Data/extracted")
        / zip_path.stem
    )

    # Clean previous extraction if exists
    if extract_dir.exists():
        shutil.rmtree(
            extract_dir
        )

    extract_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    with zipfile.ZipFile(
        zip_path,
        "r"
    ) as zip_ref:

        zip_ref.extractall(
            extract_dir
        )

    return extract_dir