import argparse
import shutil
from pathlib import Path

# Maps filename prefixes to final class folder names.
PREFIX_TO_CLASS = {
    "bath": "bathroom",
    "bathroom": "bathroom",
    "bedroom": "bedroom",
    "kitchen": "kitchen",
    "livingroom": "living_room",
    "living_room": "living_room",
    "diningroom": "dining_room",
    "dining_room": "dining_room",
}

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def infer_room_type(filename: str) -> str | None:
    stem = Path(filename).stem.lower()
    if not stem:
        return None

    token = stem.split("_")[0]
    return PREFIX_TO_CLASS.get(token)


def prepare_dataset(raw_images_dir: Path, dataset_dir: Path) -> None:
    raw_images_dir.mkdir(parents=True, exist_ok=True)
    dataset_dir.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    skipped_count = 0

    for image_path in sorted(raw_images_dir.iterdir()):
        if not image_path.is_file():
            continue

        if image_path.suffix.lower() not in VALID_EXTENSIONS:
            skipped_count += 1
            continue

        room_type = infer_room_type(image_path.name)
        if not room_type:
            print(f"[SKIP] Could not infer room type from filename: {image_path.name}")
            skipped_count += 1
            continue

        destination_dir = dataset_dir / room_type
        destination_dir.mkdir(parents=True, exist_ok=True)

        destination_path = destination_dir / image_path.name
        if destination_path.exists():
            print(f"[SKIP] Destination already exists: {destination_path}")
            skipped_count += 1
            continue

        shutil.move(str(image_path), str(destination_path))
        moved_count += 1
        print(f"[MOVE] {image_path.name} -> {destination_dir.name}/")

    print("\nDataset preparation complete")
    print(f"Moved: {moved_count}")
    print(f"Skipped: {skipped_count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare room classification dataset from flat filenames")
    parser.add_argument(
        "--raw-images-dir",
        type=Path,
        default=Path("raw_images"),
        help="Directory containing flat raw image files (default: raw_images)",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("dataset"),
        help="Output dataset directory structured by class (default: dataset)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prepare_dataset(args.raw_images_dir, args.dataset_dir)


if __name__ == "__main__":
    main()
