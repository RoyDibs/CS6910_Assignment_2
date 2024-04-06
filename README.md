# CS6910_Assignment_-2

This repository contains the Python files used to generate the results presented in the accompanying report. For detailed insights, please refer to the report available [here](https://api.wandb.ai/links/dibakar/s0xfcb15).

### Instruction to run the py file:

#### train_partA

## Usage

To run the program, you can use the following command-line arguments:

```bash
python your_script.py -e <epochs> -b <batch_size> -lr <learning_rate> -a <activation> -nf <num_filters> -ks <kernel_size> -dp <dropout_prob> -nd <neuron_dense> -fo <filter_org> -datao <data_aug> -bn <batch_norm> -train <train_folder> -test <test_folder>

## Command-line Arguments

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
- `-train`, `--train_folder`: Directory path for the train dataset.
- `-test`, `--test_folder`: Directory path for the test dataset.

**Note**: Replace `<epochs>`, `<batch_size>`, `<learning_rate>`, and other placeholders with appropriate values.

