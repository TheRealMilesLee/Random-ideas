# Random Ideas - Personal Coding Projects Collection

[中文版本](README_zh.md) | **English**

A comprehensive collection of personal coding experiments, learning projects, and implementations across multiple programming languages and technology domains. This repository represents a journey through various programming concepts, from basic algorithms to advanced machine learning applications.

## 📋 Overview

This repository is a diverse playground of coding projects that includes:
- **Python** applications for machine learning, computer vision, algorithms, and automation scripts
- **Swift** iOS applications including calculator and concentration game
- **Objective-C** learning materials and iOS development projects
- **C/C++** algorithm implementations and multithreading experiments
- **Go** interview preparation and learning materials
- **JavaScript/Electron** desktop application projects
- **Deep Learning** models using TensorFlow, Keras, and PyTorch
- **Computer Vision** projects with OpenCV
- **Firmware Analysis** tools for router firmware reverse engineering
- **Web Development** projects including personal website

## 📁 Repository Structure

```
Random-ideas/
├── Python相关/                    # Python Projects (~191MB)
│   ├── Fun_Code/                  # Fun Python scripts
│   ├── Python Examples/           # Collection of useful Python examples
│   ├── Python_CookBook/           # Python cookbook implementations
│   ├── Python下的凯撒加密/         # Caesar cipher implementation
│   ├── Python学习入门/             # Python learning basics
│   ├── Python小项目/               # Small Python projects
│   ├── TensorFlow图片学习/         # TensorFlow image learning
│   └── 算法图解/                   # Algorithm visualizations
│
├── Swift学习/                     # Swift Learning Projects (~396KB)
│   ├── Calculator/                # iOS Calculator app
│   └── Concentraction/            # Concentration card game
│
├── Objective-C_Study/             # Objective-C Study Materials (~744KB)
│   └── 知乎专栏/                   # Zhihu column articles
│
├── Objective-C Source Code/       # Objective-C Code Examples (~5.5MB)
│   └── [Various chapter materials from Objective-C book]
│
├── Tensorflow与Keras相关/         # TensorFlow & Keras Projects (~33MB)
│   ├── Keras测试程序.py           # Keras test programs
│   ├── Pytorch深度学习入门.py      # PyTorch deep learning intro
│   ├── Tensorflow 2.0.py          # TensorFlow 2.0 examples
│   └── satellite/                 # Satellite image processing
│
├── DeepLearning-Watermark/        # Deep Learning Watermark Project (~1.5MB)
│   ├── PreprocessC++/             # C++ preprocessing tools
│   ├── Try on my own/             # Custom implementations
│   ├── WaterMarkCore_TorchC/      # PyTorch C++ watermark core
│   └── watermarkFakerCore/        # Watermark generation
│
├── ElectronLatex/                 # Electron LaTeX Editor (~2.9MB)
│   ├── ContentView.js             # Main view component
│   ├── MathSymbol.js              # Math symbol handler
│   └── package.json               # Node.js dependencies
│
├── HengyiLi.github.io/            # Personal Website (~712KB)
│   └── [Blazor web application files]
│
├── OpenCV/                        # OpenCV Projects (~200KB)
│   └── [Computer vision experiments]
│
├── Golang-Learning/               # Go Learning Projects
│   └── day1-simple-program/       # Basic Go programs
│
├── GoInterview/                   # Go Interview Preparation
│   └── interview.go               # Go interview questions
│
├── MultiThreadIdea/               # Multithreading Concepts
│   └── [Multithreading experiments]
│
├── MultiThreadSort/               # Multithreaded Sorting
│   ├── MultiThreadSort.cpp        # Parallel sorting implementation
│   └── OriginalSort.cpp           # Sequential sorting baseline
│
├── Encyption/                     # Encryption Examples
│   └── Encyption.cpp              # C++ encryption implementations
│
├── ComplierTestFolder/            # Compiler Testing
│   └── [Compiler experiments]
│
├── Tree/                          # Tree Data Structure
│   └── tree.py                    # Tree implementation
│
├── TabularAlgorithm/              # Tabular Algorithms
│   └── TabularAlgorithm.py        # Tabular data processing
│
├── SpamFilter/                    # Spam Filtering System
│   └── [Spam detection implementations]
│
├── UsefulScripts/                 # Utility Scripts
│   ├── evictPods.sh               # Kubernetes pod eviction
│   ├── producer.py                # Message producer
│   └── spamMessages.sh            # Spam message generator
│
├── 路由器固件相关/                 # Router Firmware Tools
│   └── [Binwalk firmware analysis tools]
│
└── 电影彩蛋/                       # Movie Easter Eggs
    └── [Movie-related resources]
```

## 🚀 Technologies & Tools

### Programming Languages
- **Python** (371 files) - Primary language for ML, CV, and scripting
- **Objective-C** (195 .m files, 119 .h files) - iOS development
- **C/C++** (21 .c files, 16 .cpp files) - System programming and algorithms
- **Swift** - Modern iOS application development
- **Go** - Backend services and interview prep
- **JavaScript** - Electron apps and web development
- **C#** - Blazor web application

### Frameworks & Libraries
- **Machine Learning**: TensorFlow, Keras, PyTorch
- **Computer Vision**: OpenCV
- **iOS Development**: UIKit, SwiftUI
- **Web Development**: Electron, Blazor
- **Data Processing**: NumPy, Pandas

### Development Tools
- **Xcode** - iOS/macOS development
- **Visual Studio Code** - Multi-language IDE
- **Git** - Version control
- **npm** - JavaScript package management
- **pip** - Python package management

## 💡 Key Projects Highlight

### 1. **Deep Learning Watermark System**
Advanced watermarking system using deep learning for image protection
- C++ preprocessing pipeline
- PyTorch implementation with LibTorch C++ API
- Watermark detection and generation

### 2. **Electron LaTeX Editor**
Desktop LaTeX editor built with Electron
- Math symbol support
- Real-time preview
- Cross-platform compatibility

### 3. **Swift iOS Applications**
- **Calculator**: Full-featured iOS calculator
- **Concentration Game**: Memory card matching game

### 4. **Router Firmware Analysis**
Tools for analyzing and reverse engineering router firmware using Binwalk

### 5. **Python Examples Collection**
Extensive collection of practical Python scripts including:
- File batch renaming
- YouTube video downloader
- Image downloader
- Server monitoring tools
- Log management utilities

### 6. **Multithreading Experiments**
C++ implementations exploring:
- Parallel sorting algorithms
- Thread synchronization
- Performance benchmarking

## 📚 Getting Started

### Prerequisites

#### For Python Projects
```bash
# Install Python 3.8+
python --version

# Install common dependencies
pip install numpy pandas tensorflow keras opencv-python torch
```

#### For Swift/Objective-C Projects
- macOS with Xcode 14.0 or later
- iOS SDK 15.0+
- CocoaPods (for dependency management)

#### For C/C++ Projects
```bash
# Install GCC/Clang
gcc --version
g++ --version

# Install build tools
sudo apt-get install build-essential  # Linux
brew install gcc                       # macOS
```

#### For Go Projects
```bash
# Install Go 1.16+
go version
```

#### For Electron Projects
```bash
# Install Node.js and npm
node --version
npm --version

# Navigate to ElectronLatex and install dependencies
cd ElectronLatex
npm install
```

### Running Projects

#### Python Projects
```bash
# Navigate to specific Python project
cd Python相关/Python\ Examples/

# Run a script
python calculator.py
```

#### Swift Projects
```bash
# Open in Xcode
cd Swift学习/Calculator
open Calculator.xcodeproj

# Build and run from Xcode
```

#### Electron Project
```bash
cd ElectronLatex
npm start
```

#### C/C++ Projects
```bash
# Compile and run
cd MultiThreadSort
g++ -std=c++11 -pthread MultiThreadSort.cpp -o multithread_sort
./multithread_sort
```

#### Go Projects
```bash
cd Golang-Learning/day1-simple-program
go run simple.go
```

## 🧪 Testing

Most projects are experimental and learning-focused. Testing approaches vary by project:
- Python projects may include inline tests or separate test files
- iOS projects use XCTest framework
- C/C++ projects typically include manual testing

## 📖 Documentation

Individual subdirectories may contain their own README files with specific instructions:
- `Python相关/Python Examples/README.md` - Detailed Python examples documentation
- `路由器固件相关/README.md` - Binwalk firmware analysis guide
- `HengyiLi.github.io/README.md` - Personal website documentation

## 🤝 Contributing

This is a personal learning and experimentation repository. While contributions are not actively sought, feel free to:
1. **Fork** the repository for your own experiments
2. **Open issues** for bugs or questions
3. **Share ideas** for improvements

If you do submit pull requests:
- Follow existing code style in the respective language
- Add comments for complex logic
- Update documentation as needed

## 📝 Notes

- **Repository Size**: ~250MB (mostly due to Python projects and TensorFlow datasets)
- **Mixed Languages**: Code quality and style vary as this represents learning progression
- **Experimental Nature**: Many projects are works-in-progress or educational experiments
- **Chinese Naming**: Some directories use Chinese names (中文目录名) reflecting the bilingual nature of content
- **External Code**: The `Python相关/Python Examples/` directory contains code examples from external sources for learning purposes

## 📄 License

This project contains a mix of:
- Original personal code
- Educational examples and exercises
- Third-party code snippets for learning (with appropriate attribution where applicable)

Most original code is available for personal and educational use. Please check individual project directories for specific licenses.

## 📧 Contact

For questions or discussions about any project in this repository, feel free to open an issue.

---

**Last Updated**: January 2026
