# -*- coding: utf-8 -*-
"""main_part_A.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C9o3skav1tA5QiY6zOxWR7_7piIgXzgF
"""

import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import argparse

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Train neural network with specified hyperparameters.")
parser.add_argument("-e", "--epochs", type=int, default=5, help="Number of epochs to train neural network")
parser.add_argument("-b", "--batch_size", type=int, default=32, help="Batch size used to train neural network")
parser.add_argument("-lr", "--learning_rate", type=float, default=0.001, help="Learning rate")
parser.add_argument("-a", "--activation",  default='relu', choices=["relu", "gelu", "mish"], help="Activation function")
parser.add_argument("-nf", "--num_filters", type=int , default=32, help="Number of filters")
parser.add_argument("-ks", "--kernel_size", type=int , default=5, help="Kernel size")
parser.add_argument("-dp", "--dropout_prob", type=float, default=0, help="dropout probability")
parser.add_argument("-nd", "--neuron_dense", type=int , default=50, help="number of neuron on dense layer")
parser.add_argument("-fo", "--filter_org", default='same', choices=["same", "halve", "double"], help="Filter organisation")
parser.add_argument("-datao", "--data_aug",default=False, choices=[True , False ], help="data augmentation")
parser.add_argument("-bn", "--batch_norm",default=False, choices=[True , False ], help="batch normalisation")
parser.add_argument("-train", "--train_folder", type=str, help="Directory path for the train dataset")
parser.add_argument("-test", "--test_folder", type=str, help="Directory path for the test dataset")


args = parser.parse_args()


def get_transform(data_augmentation):
    if data_augmentation:
        transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1), shear=10),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        # Regular transformations
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    return transform

def load_dataset(train_folder, test_folder, transform):
    train_dataset = datasets.ImageFolder(train_folder, transform=transform)
    test_dataset = datasets.ImageFolder(test_folder, transform=get_transform(False))
    return train_dataset, test_dataset

def train(model, criterion, optimizer, train_loader, val_loader, test_loader, num_epochs):
    for epoch in range(num_epochs):
        model.train()  # Set the model to training mode
        running_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            if torch.cuda.is_available():
                images, labels = images.cuda(), labels.cuda()
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if (i + 1) % 240 == 0:  # Print every 100 batches
                print(f"Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{len(train_loader)}], Loss: {running_loss / 240:.4f}")
                running_loss = 0.0
        # Validation loop
        model.eval()  # Set the model to evaluation mode

        val_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                if torch.cuda.is_available():
                    images, labels = images.cuda(), labels.cuda()

                # Forward pass
                outputs = model(images)

                # Calculate loss
                loss = criterion(outputs, labels)

                # Update validation loss
                val_loss += loss.item()

                # Calculate accuracy
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

        # Calculate average validation loss and accuracy for the epoch
        val_loss /= len(val_loader)
        val_accuracy = correct / total * 100

        print(f"Epoch [{epoch + 1}/{num_epochs}], Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.2f}%")

    with torch.no_grad():
        for images, labels in test_loader:
            if torch.cuda.is_available():
                images, labels = images.cuda(), labels.cuda()

            # Forward pass
            outputs = model(images)

            # Calculate loss
            test_loss = criterion(outputs, labels)

            # Update validation loss
            test_loss += test_loss.item()

            # Calculate accuracy
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    # Calculate average validation loss and accuracy for the epoch
    test_loss /= len(test_loader)
    test_accuracy = correct / total * 100

    print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.2f}%")

class CNN(nn.Module):
    def __init__(self, hparams):
        super(CNN, self).__init__()
        self.hparams = hparams
        num_conv_layers = hparams['num_conv_layers']
        in_channels = 3
        num_filters = hparams['num_filters']
        kernel_size = hparams['kernel_size']  # Single integer value
        num_classes = 10
        num_neurons_dense = hparams['num_neurons_dense']
        input_size = 224
        filter_organization = hparams['filter_organization']
        batch_normalization = hparams['batch_normalization']
        dropout_prob = hparams['dropout_prob']
        conv_activation = hparams['conv_activation']

        self.conv_layers = nn.ModuleList()
        self.num_conv_layers = num_conv_layers

        # Add convolution layers
        for i in range(num_conv_layers):
            # Determine the number of filters for this layer based on filter_organization
            if filter_organization == 'same':
                out_channels = num_filters
            elif filter_organization == 'double':
                out_channels = num_filters * (2 ** i)
            elif filter_organization == 'halve':
                out_channels = num_filters // (2 ** i)
            else:
                raise ValueError("Invalid filter organization")

            # Determine padding value to maintain spatial dimensions
            padding = kernel_size // 2 if kernel_size % 2 == 1 else (kernel_size - 1) // 2

            # Add convolution layer with the same kernel size for all layers
            conv_layer = nn.Conv2d(in_channels, out_channels, kernel_size, padding=padding)
            self.conv_layers.append(conv_layer)

            # Add batch normalization if enabled
            if batch_normalization:
                bn_layer = nn.BatchNorm2d(out_channels)
                self.conv_layers.append(bn_layer)

            in_channels = out_channels

        # Add dropout layer after the last convolution layer
        self.dropout_conv = nn.Dropout2d(p=dropout_prob)

        # Calculate input size for dense layer
        dense_input_size = out_channels * (input_size // (2 ** num_conv_layers)) ** 2

        # Dense layer
        self.dense = nn.Linear(dense_input_size, num_neurons_dense)

        # Output layer
        self.output = nn.Linear(num_neurons_dense, num_classes)

    def forward(self, x):
        # Convolution layers
        for i, layer in enumerate(self.conv_layers):
            x = layer(x)
            if isinstance(layer, nn.Conv2d):
                # Apply activation function dynamically
                if self.hparams['conv_activation'] == 'relu':
                    x = F.relu(x)
                elif self.hparams['conv_activation'] == 'gelu':
                    x = F.gelu(x)
                elif self.hparams['conv_activation'] == 'mish':
                    x = F.mish(x)
                else:
                    raise ValueError("Invalid convolutional activation function")

                x = F.max_pool2d(x, 2)

        # Flatten
        x = torch.flatten(x, 1)

        # Dense layer
        x = F.relu(self.dense(x))

        # Output layer (raw scores)
        x = self.output(x)
        return x

def main(hparams):

        train_folder = args.train_folder
        test_folder = args.test_folder
        transform = get_transform(hparams['data_augmentation'])
        train_dataset, test_dataset = load_dataset(train_folder, test_folder, transform)

        # Define batch size for DataLoader
        batch_size = hparams['batch_size']

        # Split train dataset into train and validation sets
        train_indices, val_indices = train_test_split(list(range(len(train_dataset))), test_size=0.2, shuffle=True, stratify=train_dataset.targets)
        train_sampler = torch.utils.data.SubsetRandomSampler(train_indices)
        val_sampler = torch.utils.data.SubsetRandomSampler(val_indices)

        # Create DataLoader for train and validation datasets
        train_loader = DataLoader(train_dataset, batch_size=batch_size, sampler=train_sampler)
        val_loader = DataLoader(train_dataset, batch_size=batch_size, sampler=val_sampler)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        # Print the number of samples in train and validation sets after splitting
        print("Number of samples in train set after splitting:", len(train_indices))
        print("Number of samples in validation set after splitting:", len(val_indices))

        for images, labels in train_loader:
            # Get the shape of the image tensor (batch_size, channels, height, width)
            batch_size, in_channels, height, width = images.shape
            # Get the number of unique classes in the dataset
            num_classes = len(train_dataset.classes)
            # Input size is the height and width of the image
            input_size = height, width
            break  # Break after processing the first batch

        print("In channels:", in_channels)
        print("Number of classes:", num_classes)
        print("Input size (height, width):", input_size)


        # Create the model
        model = CNN(hparams)
        # Define loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
        # checking if GPU is available
        if torch.cuda.is_available():
            model = model.cuda()
            criterion = criterion.cuda()
        train(model,criterion,optimizer,train_loader,val_loader, test_loader, hparams['max_epoch'])


hparams = {
    'num_conv_layers': 5,
    'num_filters': args.num_filters,
    'kernel_size': args.kernel_size,
    'num_neurons_dense': args.neuron_dense,
    'filter_organization': args.filter_org,
    'data_augmentation': args.data_aug,
    'batch_normalization': args.batch_norm,
    'dropout_prob': args.dropout_prob,
    'conv_activation': args.activation,
    'max_epoch': args.epochs,
    'batch_size': args.batch_size
}

main(hparams)