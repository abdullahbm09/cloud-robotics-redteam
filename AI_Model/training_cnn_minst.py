import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, precision_recall_curve
import seaborn as sns
import pandas as pd

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define paths for MNIST dataset and saved model
mnist_path = "./mnist_data"
model_path = "./cnn_mnist_model.pth"
results_dir = "./results"

# Create results directory if it doesn't exist
os.makedirs(results_dir, exist_ok=True)

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
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Training and evaluation functions with accuracy, loss tracking
def train_model(model, train_loader, epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    model.train()
    train_losses, val_accuracies = [], []
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
        avg_loss = running_loss / len(train_loader)
        train_losses.append(avg_loss)
        val_accuracy, _, _ = evaluate_model(model, test_loader)
        val_accuracies.append(val_accuracy)
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}, Validation Accuracy: {val_accuracy:.2%}")
    return train_losses, val_accuracies

# Evaluate model and return accuracy and predictions
def evaluate_model(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    accuracy = correct / total
    return accuracy, all_preds, all_labels

# Plot training and validation accuracy/loss and save
def plot_training_metrics(train_losses, val_accuracies):
    epochs = range(1, len(train_losses) + 1)
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_losses, label='Training Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training Loss per Epoch')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(epochs, val_accuracies, label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Validation Accuracy per Epoch')
    plt.legend()
    plt.savefig(os.path.join(results_dir, 'training_metrics.png'))
    plt.show()

# Confusion matrix and classification report
def plot_confusion_matrix(all_labels, all_preds):
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=range(10), yticklabels=range(10))
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(results_dir, 'confusion_matrix.png'))
    plt.show()
    report = classification_report(all_labels, all_preds, output_dict=True)
    pd.DataFrame(report).transpose().to_csv(os.path.join(results_dir, 'classification_report.csv'))

# ROC and Precision-Recall curves for multi-class
def plot_roc_pr_curves(all_labels, all_probs, num_classes=10):
    fpr, tpr, roc_auc, precision, recall, pr_auc = {}, {}, {}, {}, {}, {}
    for i in range(num_classes):
        fpr[i], tpr[i], _ = roc_curve(all_labels == i, all_probs[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
        precision[i], recall[i], _ = precision_recall_curve(all_labels == i, all_probs[:, i])
        pr_auc[i] = auc(recall[i], precision[i])

    # Plot ROC curve
    plt.figure(figsize=(12, 5))
    for i in range(num_classes):
        plt.plot(fpr[i], tpr[i], label=f"Class {i} (AUC = {roc_auc[i]:.2f})")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.savefig(os.path.join(results_dir, 'roc_curve.png'))
    plt.show()

    # Plot Precision-Recall curve
    plt.figure(figsize=(12, 5))
    for i in range(num_classes):
        plt.plot(recall[i], precision[i], label=f"Class {i} (AUC = {pr_auc[i]:.2f})")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.legend()
    plt.savefig(os.path.join(results_dir, 'precision_recall_curve.png'))
    plt.show()

# Main execution
if os.path.exists(model_path):
    model = CNN().to(device)
    model.load_state_dict(torch.load(model_path))
    print("Loaded pre-trained model.")
else:
    model = CNN().to(device)
    print("Training model from scratch...")
    train_losses, val_accuracies = train_model(model, train_loader, epochs=10)
    plot_training_metrics(train_losses, val_accuracies)
    pd.DataFrame({"Epoch": range(1, len(train_losses) + 1), "Train Loss": train_losses, "Val Accuracy": val_accuracies}).to_csv(os.path.join(results_dir, 'training_metrics.csv'), index=False)
    torch.save(model.state_dict(), model_path)

# Evaluate and plot final metrics
accuracy, all_preds, all_labels = evaluate_model(model, test_loader)
print(f"Test Accuracy: {accuracy:.2%}")
plot_confusion_matrix(all_labels, all_preds)

# Obtain probabilities for ROC and PR curves
all_probs = []
model.eval()
with torch.no_grad():
    for images, _ in test_loader:
        images = images.to(device)
        outputs = model(images)
        all_probs.append(torch.softmax(outputs, dim=1).cpu().numpy())
all_probs = np.concatenate(all_probs, axis=0)

plot_roc_pr_curves(np.array(all_labels), all_probs)
