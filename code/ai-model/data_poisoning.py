import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import requests

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define paths for downloading and loading MNIST dataset
mnist_path = "mnist.npz"
base_url = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz"

# Function to download MNIST dataset if not already downloaded
def download_mnist():
    if not os.path.exists(mnist_path):
        print("Downloading MNIST dataset...")
        response = requests.get(base_url)
        with open(mnist_path, "wb") as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("MNIST dataset already exists.")

# Load MNIST dataset from local file
def load_mnist():
    with np.load(mnist_path) as data:
        x_train, y_train = data['x_train'], data['y_train']
        x_test, y_test = data['x_test'], data['y_test']
    return (x_train, y_train), (x_test, y_test)

# Download MNIST if not already downloaded
download_mnist()

# Load and preprocess MNIST dataset
(x_train, y_train), (x_test, y_test) = load_mnist()
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize images

# Convert data to PyTorch tensors
x_train = torch.tensor(x_train, dtype=torch.float32).unsqueeze(1).to(device)
y_train = torch.tensor(y_train, dtype=torch.long).to(device)
x_test = torch.tensor(x_test, dtype=torch.float32).unsqueeze(1).to(device)
y_test = torch.tensor(y_test, dtype=torch.long).to(device)

# Display original data
plt.figure(figsize=(8, 2))
for i in range(10):
    plt.subplot(1, 10, i + 1)
    plt.imshow(x_train[i].squeeze().cpu(), cmap="gray")
    plt.axis("off")
plt.show()
print("Original labels:", y_train[:10].cpu().numpy())

# Step 1: Build a simple model in PyTorch
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Training function
def train_model(model, data, labels, epochs=3):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f"Training loss after epoch {epoch + 1}: {loss.item():.4f}")

# Evaluate function
def evaluate_model(model, data, labels):
    model.eval()
    with torch.no_grad():
        outputs = model(data)
        _, predicted = torch.max(outputs, 1)
        accuracy = (predicted == labels).sum().item() / labels.size(0)
    return accuracy

# Train initial model on clean data
model = SimpleNN().to(device)
train_model(model, x_train, y_train, epochs=3)
clean_accuracy = evaluate_model(model, x_test, y_test)
print(f"Accuracy on clean test data: {clean_accuracy:.2%}")

# Step 2: Poison the training data by flipping some labels
poisoned_x_train = x_train.clone()
poisoned_y_train = y_train.clone()

# Introduce a 10% data poisoning by mislabeling some samples
poisoning_rate = 0.1  # 10% of the data will be poisoned
num_poisoned = int(poisoning_rate * len(poisoned_y_train))
poisoned_indices = np.random.choice(len(poisoned_y_train), num_poisoned, replace=False)

# Flip labels (e.g., make '0' look like '1', '1' look like '2', etc.)
for idx in poisoned_indices:
    poisoned_label = (poisoned_y_train[idx].item() + 1) % 10  # Change to the next class label
    poisoned_y_train[idx] = poisoned_label

# Display some poisoned data to visualize the change
plt.figure(figsize=(8, 2))
for i in range(10):
    plt.subplot(1, 10, i + 1)
    plt.imshow(poisoned_x_train[poisoned_indices[i]].squeeze().cpu(), cmap="gray")
    plt.axis("off")
plt.show()
print("Poisoned labels:", poisoned_y_train[poisoned_indices[:10]].cpu().numpy())

# Step 3: Retrain the model with poisoned data
poisoned_model = SimpleNN().to(device)
train_model(poisoned_model, poisoned_x_train, poisoned_y_train, epochs=3)
poisoned_accuracy = evaluate_model(poisoned_model, x_test, y_test)
print(f"Accuracy on clean test data after poisoning: {poisoned_accuracy:.2%}")

# Compare accuracies
print(f"Performance degradation due to poisoning: {clean_accuracy - poisoned_accuracy:.2%}")
