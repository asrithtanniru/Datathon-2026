import argparse
import random
import shutil
from pathlib import Path

import kagglehub

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Keywords searched in parent folder names to infer class.
CLASS_KEYWORDS = {
    "bathroom": ["bathroom", "bath"],
    "bedroom": ["bedroom", "bed"],
    "kitchen": ["kitchen"],
    "living_room": ["livingroom", "living_room", "living room", "living"],
    "dining_room": ["diningroom", "dining_room", "dining room", "dining"],
}

# Prefixes to match your current flat filename style.
CLASS_PREFIX = {
    "bathroom": "bath",
    "bedroom": "bedroom",
    "kitchen": "kitchen",
    "living_room": "livingroom",
    "dining_room": "diningroom",
}


def infer_class_from_path(path: Path) -> str | None:
    relative_parts = [part.lower() for part in path.parts]
    searchable = " ".join(relative_parts)

    for class_name, keywords in CLASS_KEYWORDS.items():
        if any(keyword in searchable for keyword in keywords):
            return class_name
    return None


def collect_images_by_class(dataset_root: Path) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = {class_name: [] for class_name in CLASS_KEYWORDS}

    for file_path in dataset_root.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in VALID_EXTENSIONS:
            continue

        class_name = infer_class_from_path(file_path)
        if class_name:
            grouped[class_name].append(file_path)

    return grouped


def clear_raw_images(raw_images_dir: Path) -> None:
    for item in raw_images_dir.iterdir():
        if item.name == ".gitkeep":
            continue
        if item.is_file():
            item.unlink()


def build_subset(
    grouped_images: dict[str, list[Path]],
    raw_images_dir: Path,
    per_class: int,
    seed: int,
) -> None:
    random.seed(seed)
    raw_images_dir.mkdir(parents=True, exist_ok=True)

    total_copied = 0
    for class_name, images in grouped_images.items():
        if not images:
            print(f"[WARN] No images found for class: {class_name}")
            continue

        sample_size = min(per_class, len(images))
        selected = random.sample(images, sample_size)
        prefix = CLASS_PREFIX[class_name]

        for index, src_path in enumerate(selected, start=1):
            extension = src_path.suffix.lower() if src_path.suffix else ".jpg"
            dst_name = f"{prefix}_{index:04d}{extension}"
            dst_path = raw_images_dir / dst_name
            shutil.copy2(src_path, dst_path)

        total_copied += sample_size
        print(f"[OK] {class_name}: copied {sample_size} images")

    print(f"\nFinished. Total copied to raw_images: {total_copied}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Kaggle house room dataset and copy a small class-balanced subset to raw_images"
    )
    parser.add_argument(
        "--dataset-id",
        default="robinreni/house-rooms-image-dataset",
        help="Kaggle dataset ID (default: robinreni/house-rooms-image-dataset)",
    )
    parser.add_argument(
        "--raw-images-dir",
        type=Path,
        default=Path("raw_images"),
        help="Output directory for flat filenames (default: raw_images)",
    )
    parser.add_argument(
        "--per-class",
        type=int,
        default=120,
        help="How many images per class to copy (default: 120)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible sampling",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing files in raw_images before copying new subset",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.per_class <= 0:
        raise ValueError("--per-class must be > 0")

    print(f"Downloading dataset: {args.dataset_id}")
    dataset_path = Path(kagglehub.dataset_download(args.dataset_id))
    print(f"Dataset downloaded to: {dataset_path}")

    grouped_images = collect_images_by_class(dataset_path)
    for class_name, images in grouped_images.items():
        print(f"[FOUND] {class_name}: {len(images)}")

    if args.clean:
        clear_raw_images(args.raw_images_dir)

    build_subset(
        grouped_images=grouped_images,
        raw_images_dir=args.raw_images_dir,
        per_class=args.per_class,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
