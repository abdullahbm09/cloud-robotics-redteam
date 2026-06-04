import os
import torch
import random
import torchvision.transforms as transforms
from torchvision.datasets import MNIST
import time
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
import pandas as pd

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

# Load model
model = CNN().to(device)
model.load_state_dict(torch.load(model_path))
model.eval()
print("Loaded model for inference.")

# Directory paths
without_attack_dir = "./inference_results/without_attack"
with_attack_dir = "./inference_results/with_attack"
os.makedirs(without_attack_dir, exist_ok=True)
os.makedirs(with_attack_dir, exist_ok=True)

# Functions for benchmarking and plotting
def calculate_and_save_metrics(all_labels, all_preds, inference_times, poisoned_labels, poisoned_preds, save_dir):
    # Calculate accuracy, confusion matrix, and average inference time
    accuracy = sum(np.array(all_preds) == np.array(all_labels)) / len(all_labels)
    cm = confusion_matrix(all_labels, all_preds)
    avg_inference_time = np.mean(inference_times)
    
    # Calculate poisoned sample accuracy only if poisoned samples exist
    if poisoned_labels:
        poisoned_accuracy = sum(np.array(poisoned_preds) == np.array(poisoned_labels)) / len(poisoned_labels)
    else:
        poisoned_accuracy = None  # No poisoned samples, set accuracy to None or 0

    # Print and save metrics
    print(f"Final Results - Overall Accuracy: {accuracy:.2%}, Average Inference Time: {avg_inference_time:.6f} seconds")
    if poisoned_accuracy is not None:
        print(f"Poisoned Sample Accuracy: {poisoned_accuracy:.2%}")
    
    # Save confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=range(10), yticklabels=range(10))
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'))
    plt.close()
    
    # Save accuracy and inference time
    metrics = {
        "Total Iterations": [len(all_labels)],
        "Overall Accuracy": [accuracy],
        "Average Inference Time": [avg_inference_time],
        "Poisoned Sample Accuracy": [poisoned_accuracy if poisoned_accuracy is not None else "N/A"]
    }
    df = pd.DataFrame(metrics)
    df.to_csv(os.path.join(save_dir, "final_metrics.csv"), index=False)


# FGSM-based data poisoning function
def fgsm_attack(image, epsilon, data_grad):
    # Create perturbed image by adjusting each pixel
    sign_data_grad = data_grad.sign()
    perturbed_image = image + epsilon * sign_data_grad
    perturbed_image = torch.clamp(perturbed_image, 0, 1)
    return perturbed_image

def poison_image_with_fgsm(model, image, label, epsilon=0.3):
    image.requires_grad = True
    output = model(image)
    loss = nn.CrossEntropyLoss()(output, torch.tensor([label]).to(device))
    model.zero_grad()
    loss.backward()
    data_grad = image.grad.data
    poisoned_image = fgsm_attack(image, epsilon, data_grad)
    return poisoned_image

# Run inference without attack and with FGSM attack on 50 random samples
for attack in [False, True]:
    all_preds, all_labels, inference_times = [], [], []
    poisoned_preds, poisoned_labels = [], []
    save_dir = with_attack_dir if attack else without_attack_dir
    print(f"\nRunning inference with{'out' if not attack else ''} attack...")

    # Select 50 random indices for poisoning if attack is True
    poison_indices = random.sample(range(1000), 50) if attack else []

    for i in range(1000):  # 1000 iterations
        # Randomly select a sample
        index = random.randint(0, len(test_dataset) - 1)
        image, true_label = test_dataset[index]
        
        # Apply poisoning attack if the index is in poison_indices
        if attack and i in poison_indices:
            image = poison_image_with_fgsm(model, image.unsqueeze(0).to(device), true_label)
            poisoned_labels.append(true_label)
        else:
            image = image.unsqueeze(0).to(device)
        
        # Measure inference time
        start_time = time.time()
        with torch.no_grad():
            output = model(image)
            _, predicted_label = torch.max(output, 1)
        inference_time = time.time() - start_time
        inference_times.append(inference_time)
        
        # Store results
        all_preds.append(predicted_label.item())
        all_labels.append(true_label)
        
        # Track results for poisoned samples
        if attack and i in poison_indices:
            poisoned_preds.append(predicted_label.item())

    # Calculate and save metrics after 1000 iterations
    calculate_and_save_metrics(all_labels, all_preds, inference_times, poisoned_labels, poisoned_preds, save_dir)

print("\nInference with and without attack completed.")

# Compare results
def compare_results():
    print("\nComparison between Without Attack and With Attack:")
    without_attack_metrics = pd.read_csv(os.path.join(without_attack_dir, "final_metrics.csv"))
    with_attack_metrics = pd.read_csv(os.path.join(with_attack_dir, "final_metrics.csv"))
    
    print(f"\nWithout Attack - Overall Accuracy: {without_attack_metrics['Overall Accuracy'].iloc[0]:.2%}, "
          f"Average Inference Time: {without_attack_metrics['Average Inference Time'].iloc[0]:.6f} seconds")
    
    print(f"With Attack    - Overall Accuracy: {with_attack_metrics['Overall Accuracy'].iloc[0]:.2%}, "
          f"Average Inference Time: {with_attack_metrics['Average Inference Time'].iloc[0]:.6f} seconds")
    print(f"Poisoned Sample Accuracy (With Attack): {with_attack_metrics['Poisoned Sample Accuracy'].iloc[0]:.2%}")

# Run comparison
compare_results()
