import torch
import random
import torchvision.transforms as transforms
from torchvision.datasets import MNIST
import time
import torch.nn as nn

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load MNIST test dataset
mnist_path = "./mnist_data"
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
test_dataset = MNIST(root=mnist_path, train=False, transform=transform)

# Load pre-trained model
model_path = "./cnn_mnist_model.pth"

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = CNN().to(device)
model.load_state_dict(torch.load(model_path))
model.eval()
print("Loaded model for inference.")

# Randomly classify samples from test data
try:
    while True:
        # Randomly select a sample
        index = random.randint(0, len(test_dataset) - 1)
        image, true_label = test_dataset[index]
        
        # Prepare image for model input
        image = image.unsqueeze(0).to(device)
        
        # Run inference
        with torch.no_grad():
            output = model(image)
            _, predicted_label = torch.max(output, 1)
        
        # Print result
        print(f"True Label: {true_label}, Predicted Label: {predicted_label.item()}")
        
        # Wait before the next inference
        time.sleep(1)
except KeyboardInterrupt:
    print("\nInference stopped by user.")
