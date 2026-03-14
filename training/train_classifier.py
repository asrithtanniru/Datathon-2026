import argparse
from pathlib import Path

import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def get_device() -> torch.device:
    return torch.device("mps" if torch.backends.mps.is_available() else "cpu")


def train_classifier(
    dataset_dir: Path,
    model_output_path: Path,
    epochs: int = 4,
    batch_size: int = 8,
    learning_rate: float = 1e-4,
) -> None:
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    dataset = datasets.ImageFolder(root=dataset_dir, transform=transform)
    if len(dataset) == 0:
        raise ValueError("No images found in dataset. Run training/prepare_dataset.py first.")

    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    device = get_device()
    print(f"Using device: {device}")
    print(f"Classes: {dataset.classes}")

    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    model.train()
    for epoch in range(epochs):
        running_loss = 0.0

        for images, labels in data_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item())

        avg_loss = running_loss / max(1, len(data_loader))
        print(f"Epoch [{epoch + 1}/{epochs}] - Loss: {avg_loss:.4f}")

    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "state_dict": model.state_dict(),
            "class_to_idx": dataset.class_to_idx,
        },
        model_output_path,
    )
    print(f"Saved model checkpoint: {model_output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train room classifier with ResNet50")
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("dataset"),
        help="Path to class-structured dataset directory",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("models/room_classifier.pth"),
        help="Path to save the trained model checkpoint",
    )
    parser.add_argument("--epochs", type=int, default=4, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=8, help="Training batch size")
    parser.add_argument("--learning-rate", type=float, default=1e-4, help="Adam learning rate")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_classifier(
        dataset_dir=args.dataset_dir,
        model_output_path=args.output_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
    )


if __name__ == "__main__":
    main()
