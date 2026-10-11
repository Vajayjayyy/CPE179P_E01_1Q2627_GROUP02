import os
import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision import transforms

class ContainerDataset:
    def __init__(self, data_dir, ann_file):
        # The Roboflow images are already 416x416, so we just convert to tensor
        self.transform = transforms.Compose([
            transforms.ToTensor()
        ])
        
        # Load the COCO formatted dataset
        self.dataset = torchvision.datasets.CocoDetection(
            root=data_dir,
            annFile=ann_file,
            transform=self.transform
        )

    def collate_fn(self, batch):
        return tuple(zip(*batch))

    def get_loader(self, batch_size=16, shuffle=True):
        return DataLoader(
            self.dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=2,
            collate_fn=self.collate_fn
        )

if __name__ == "__main__":
    # Replace with your actual paths from the Roboflow export
    DATA_DIR = "./dataset/train"
    ANN_FILE = "./dataset/train/_annotations.coco.json"
    
    if os.path.exists(DATA_DIR) and os.path.exists(ANN_FILE):
        container_data = ContainerDataset(DATA_DIR, ANN_FILE)
        train_loader = container_data.get_loader()
        
        # Test the loader
        images, targets = next(iter(train_loader))
        print(f"Loaded batch of {len(images)} images.")
        print(f"Image tensor shape: {images[0].shape}") # Should be [3, 416, 416]
    else:
        print("Dataset not found. Please extract the Roboflow export into ./dataset/train")