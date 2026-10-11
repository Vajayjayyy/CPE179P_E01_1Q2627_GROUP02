import torch
import torchvision
from torchvision.models.detection import fasterrcnn_mobilenet_v3_large_fpn
from coco_loader import ContainerDataset

def get_model(num_classes):
    # Load a pre-trained, lightweight model suitable for edge devices
    model = fasterrcnn_mobilenet_v3_large_fpn(pretrained=True)
    
    # Replace the classifier head with our number of classes (Container + Background)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(in_features, num_classes)
    return model

def setup_training():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(f"Using device: {device}")
    
    # We have 2 classes: Background (0) and Container Code (1)
    model = get_model(num_classes=2)
    model.to(device)
    
    # Define optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
    
    print("Sprint 2 Baseline Model initialized and ready for training loop.")
    return model, optimizer

if __name__ == "__main__":
    setup_training()