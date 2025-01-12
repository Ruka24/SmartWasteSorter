# SmartWasteSorter

A smart waste sorting system that uses image classification to identify and sort waste materials into appropriate bins. The project combines computer vision, neural networks, and IoT components to automate waste management.

## Overview

The **Smart Waste Sorter** is designed to classify waste into specific categories (e.g., plastic, paper, metal) using computer vision and a neural network model. It automates the waste disposal process by activating corresponding bins for sorted waste. The system ensures energy efficiency with a dual power management approach.

## Features

- **Image-based Waste Classification**:
  - Neural network model trained using Teachable Machine.
  - Image processing via laptop's CPU.

- **Automated Bin Activation**:
  - Arduino Uno controls servo motors to open the appropriate bin for waste disposal.

- **Power Management**:
  - Powered by a dual-source system (USB and Battery).
  - Includes a voltage regulator for stable operation.

## System Components

### Hardware

- **Camera Module**: Captures waste images.
- **Arduino Uno**: Controls servo motors.
- **CPU**: Processes image data using TensorFlow.
- **Servo Motors**: Operate the waste bins.
- **Power Source**: Combination of USB and 4xAA batteries.

### Software

- Neural network model (`keras_model.h5`) for waste classification.
- TensorFlow for image processing and classification.
- Arduino scripts for bin activation and servo control.

## How It Works

1. Waste is placed in front of the camera module.
2. The **Input Processing Unit** captures and processes the image.
3. The **Waste Classification Module** classifies the waste and sends the result to the Arduino.
4. The Arduino activates the corresponding servo motor to open the correct bin.
5. The **Power Management Module** ensures a stable power supply to all components.


## Getting Started

### Prerequisites

- Install Arduino IDE for hardware programming.
- Install TensorFlow for running the neural network model.
- Use GitHub Desktop or Git for repository management.
