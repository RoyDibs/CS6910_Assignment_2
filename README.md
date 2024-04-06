# CS6910_Assignment_-2

This repository contains the Python files used to generate the results presented in the accompanying report. For detailed insights, please refer to the report available [here](https://api.wandb.ai/links/dibakar/s0xfcb15).

## Instruction to run the py file:

### Usage

#### train_partA
To run the train_partA.py file, you can use the following command-line arguments:

```bash
python train_partA.py -e <epochs> -b <batch_size> -lr <learning_rate> -a <activation> -nf <num_filters> -ks <kernel_size> -dp <dropout_prob> -nd <neuron_dense> -fo <filter_org> -datao <data_aug> -bn <batch_norm> -train <train_folder> -test <test_folder>
```
##### Command-line Arguments

- `-e`, `--epochs`: Number of epochs to train the neural network (default: 5).
- `-b`, `--batch_size`: Batch size used to train the neural network (default: 32).
- `-lr`, `--learning_rate`: Learning rate (default: 0.001).
- `-a`, `--activation`: Activation function (default: 'relu'). Choices: "relu", "gelu", "mish".
- `-nf`, `--num_filters`: Number of filters (default: 32).
- `-ks`, `--kernel_size`: Kernel size (default: 5).
- `-dp`, `--dropout_prob`: Dropout probability (default: 0).
- `-nd`, `--neuron_dense`: Number of neurons on the dense layer (default: 50).
- `-fo`, `--filter_org`: Filter organization (default: 'same'). Choices: "same", "halve", "double".
- `-datao`, `--data_aug`: Data augmentation (default: False). Choices: True, False.
- `-bn`, `--batch_norm`: Batch normalization (default: False). Choices: True, False.
- `-train`, `--train_folder`: Directory path for the training dataset.
- `-test`, `--test_folder`: Directory path for the test dataset.

**Note**: Replace `<epochs>`, `<batch_size>`, `<learning_rate>`, and other placeholders with appropriate values.

#### train_partB
To run the train_partB.py file, you can use the following command-line arguments:

```bash
python train_partB.py -e <epochs> -b <batch_size> -lr <learning_rate> -train <train_folder> -test <test_folder>
```
##### Command-line Arguments

- `-e`, `--epochs`: Number of epochs to train the neural network (default: 5).
- `-b`, `--batch_size`: Batch size used to train the neural network (default: 32).
- `-lr`, `--learning_rate`: Learning rate (default: 0.001).
- `-train`, `--train_folder`: Directory path for the training dataset.
- `-test`, `--test_folder`: Directory path for the test dataset.

**Note**: Replace `<epochs>`, `<batch_size>`, `<learning_rate>`, and other placeholders with appropriate values.


## Content overview:
The repository is divided into two parts Part A and Part B and jupyter notebooks are given for the respective questions of the assignment. 

### Part A
1. **Question_1**: 
   - This notebook is dedicated to creating a Convolutional Neural Network (CNN) model with the following architecture: five convolutional layers, each followed by activation and max-pooling, a dense layer,        and finally, an output layer with ten classes.
   
2. **Question_2**: 
   - This notebook demonstrates the process of running a hyperparameter sweep to explore specific configurations and optimize model performance.

3. **Question_4**: 
   - The notebook executes the model with the best hyperparameter configuration obtained from the sweep and reports the accuracy for the test dataset. Additionally, it generates a plot to visualize the model's predictions and compares them with the original labels.

### Part B
4. **Question_3**: 
   - The notebook demonstrates the implementation of a pre-trained model, which is fine-tuned by freezing all layers except the last one and then training only the last layer. Additionally, it reports the accuracy achieved on the test dataset.

