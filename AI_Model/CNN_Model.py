import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define paths for MNIST dataset and saved model
mnist_path = "./mnist_data"
model_path = "./cnn_mnist_model.pth"

# Download MNIST if not already downloaded
def download_mnist():
    if not os.path.exists(mnist_path):
        os.makedirs(mnist_path)
    if len(os.listdir(mnist_path)) == 0:
        print("Downloading MNIST dataset...")
        _ = MNIST(root=mnist_path, train=True, download=True)
        _ = MNIST(root=mnist_path, train=False, download=True)
        print("Download complete.")
    else:
        print("MNIST dataset already exists.")

download_mnist()

# Load MNIST dataset
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
train_dataset = MNIST(root=mnist_path, train=True, transform=transform)
test_dataset = MNIST(root=mnist_path, train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

# Define a CNN model with high accuracy for MNIST
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # Adjusted to match the output shape after pooling
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)  # Flatten the tensor to match fully connected layer
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Training function
def train_model(model, train_loader, epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {running_loss / len(train_loader):.4f}")

# Evaluation function
def evaluate_model(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = correct / total
    return accuracy

# Check if a trained model exists
if os.path.exists(model_path):
    # Load the pre-trained model
    model = CNN().to(device)
    model.load_state_dict(torch.load(model_path))
    print("Loaded pre-trained model.")

    # Check its accuracy
    clean_accuracy = evaluate_model(model, test_loader)
    print(f"Accuracy of the pre-trained model on clean test data: {clean_accuracy:.2%}")

    # Proceed only if accuracy is very high (e.g., above 98%)
    if clean_accuracy < 0.98:
        print("Pre-trained model accuracy is too low. Re-training model...")
        model = CNN().to(device)
        train_model(model, train_loader, epochs=5)
        clean_accuracy = evaluate_model(model, test_loader)
        print(f"Re-trained model accuracy on clean test data: {clean_accuracy:.2%}")
        # Save the trained model
        torch.save(model.state_dict(), model_path)
else:
    # Train the model from scratch if no pre-trained model is found
    model = CNN().to(device)
    print("Training model from scratch...")
    train_model(model, train_loader, epochs=5)
    clean_accuracy = evaluate_model(model, test_loader)
    print(f"Trained model accuracy on clean test data: {clean_accuracy:.2%}")
    # Save the trained model
    torch.save(model.state_dict(), model_path)

# Step 2: Data Poisoning on Inference Data
print("Starting data poisoning on inference (test) data...")

# Create poisoned test data by flipping labels
poisoned_test_dataset = list(test_dataset)
poisoning_rate = 0.1  # 10% of the data will be poisoned
num_poisoned = int(poisoning_rate * len(poisoned_test_dataset))
poisoned_indices = np.random.choice(len(poisoned_test_dataset), num_poisoned, replace=False)

# Flip labels (e.g., make '0' look like '1', '1' look like '2', etc.)
for idx in poisoned_indices:
    img, label = poisoned_test_dataset[idx]
    poisoned_label = (label + 1) % 10  # Change to the next class label
    poisoned_test_dataset[idx] = (img, poisoned_label)

# Create a DataLoader from the poisoned test dataset
poisoned_test_loader = DataLoader(poisoned_test_dataset, batch_size=1000, shuffle=False)

# Evaluate model on poisoned inference data
poisoned_accuracy = evaluate_model(model, poisoned_test_loader)
print(f"Accuracy on poisoned test data: {poisoned_accuracy:.2%}")

# Compare accuracies
print(f"Performance degradation due to poisoning: {clean_accuracy - poisoned_accuracy:.2%}")
