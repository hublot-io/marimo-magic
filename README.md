# 🧬 Marimo Magic for Jupyter/Colab

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Google Colab](https://img.shields.io/badge/Google-Colab-blue.svg)](https://colab.research.google.com/)

A custom IPython magic command that embeds [marimo](https://marimo.io) notebooks directly in Jupyter notebooks and Google Colab, similar to `%tensorboard`. Perfect for interactive development, presentations, and sharing reactive Python notebooks.

## ✨ Features

- **🔄 UV Integration**: Automatic dependency management with `uv` support
- **🛡️ Colab Compatibility**: Seamless integration with Google Colab's iframe restrictions
- **📝 Edit & Run Modes**: Full development in edit mode, presentations in run mode
- **🎯 Smart Fallbacks**: Robust iframe embedding with direct link alternatives
- **🔧 Advanced Debugging**: Comprehensive diagnostics and connection testing
- **📦 Inline Dependencies**: Supports PEP 723 script dependencies out of the box

## 🚀 Quick Start

### Installation

#### Option 1: Copy files directly (recommended for Colab)
1. Download `magic.py` and `__init__.py` from this repository
2. Upload to your Jupyter/Colab session
3. Load the extension:

```python
%load_ext marimo_magic
```

#### Option 2: Install via pip (when package is published)
```bash
pip install marimo-magic
```

### Basic Usage

```python
# Load the extension
%load_ext marimo_magic

# Start marimo with default settings (creates temp notebook in run mode)
%marimo

# Run an existing notebook
%marimo my_notebook.py

# Edit mode for development
%marimo my_notebook.py --edit

# Custom dimensions and port
%marimo my_notebook.py --port 8080 --height 800 --width 90%
```

## 📖 Usage Guide

### Run Mode vs Edit Mode

| Mode | Purpose | Features | Use Cases |
|------|---------|----------|-----------|
| **Run** (default) | Interactive execution | View outputs, interact with widgets | Demos, presentations, exploration |
| **Edit** | Development | Add/edit/delete cells, full IDE | Notebook development, debugging |

```python
# Development workflow
%marimo analysis.py --edit --debug

# Presentation mode  
%marimo analysis.py --height 900

# Quick exploration with temporary notebook
%marimo --edit
```

### Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `notebook_path` | Path to marimo notebook file | `%marimo my_notebook.py` |
| `--edit` | Run in edit mode | `%marimo --edit` |
| `--port PORT` | Specify server port | `%marimo --port 8080` |
| `--height HEIGHT` | Iframe height in pixels | `%marimo --height 800` |
| `--width WIDTH` | Iframe width | `%marimo --width 80%` |
| `--debug` | Enable debug output | `%marimo --debug` |
| `--stop PORT` | Stop server on port | `%marimo --stop 8080` |
| `--diagnose` | Run diagnostics | `%marimo --diagnose` |

### Inline Dependencies (PEP 723)

Your marimo notebooks can include dependencies directly in the script:

```python
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "marimo",
#     "torch>=2.0.0",
#     "transformers>=4.20.0",
#     "pandas",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.14.9"
app = marimo.App()

@app.cell
def __():
    import torch
    import transformers
    # Your code here...
```

The magic command automatically detects inline dependencies and:
- Uses `uv run marimo` when available for isolated environments
- Adds `--sandbox` flag to avoid terminal interactions
- Extends timeout for package installation
- Shows progress indicators for heavy packages

## 🛠️ Troubleshooting

### Debug Mode
```python
%marimo my_notebook.py --debug
```

### Connection Testing
```python
%marimo --diagnose
```

This runs comprehensive checks:
- ✅ UV and marimo installation
- ✅ Port availability
- ✅ Server startup testing
- ✅ Environment detection (Colab vs Jupyter)

### Common Issues

| Issue | Solution |
|-------|----------|
| Iframe appears empty in Colab | Click "Open Marimo Notebook" button |
| Server won't start | Check `%marimo --diagnose` |
| Dependencies not installing | Ensure `uv` is available or install packages manually |
| Edit mode timeout | Files with heavy dependencies need 3-5 minutes |

## 🏗️ Architecture

The magic command:
1. **Detects environment**: Colab vs regular Jupyter
2. **Chooses runner**: `uv run marimo` vs `python -m marimo`
3. **Starts server**: Headless mode with auto-port selection
4. **Handles dependencies**: Automatic sandbox mode for PEP 723 scripts
5. **Creates display**: Smart iframe embedding with fallbacks

### Google Colab Integration

Special handling for Colab's security restrictions:
- Uses `google.colab.output.eval_js()` for proper proxy URLs
- Provides iframe + direct link fallbacks
- Auto-opens in new tab when iframe fails
- Handles authentication bypass with `--no-token`

## 📝 Example Workflows

### Data Science Notebook
```python
# Create a new analysis notebook
%marimo analysis.py --edit

# Present results
%marimo analysis.py --height 900

# Share with colleagues (generates shareable link)
%marimo analysis.py --port 8080
```

### ML Model Development
```python
# Work on model with heavy dependencies
%marimo model_training.py --edit --debug

# Quick inference demo
%marimo model_inference.py

# Stop all servers
%marimo --stop 8080
%marimo --stop 2718
```

### Interactive Teaching
```python
# Student exploration mode
%marimo --edit --height 700

# Instructor presentation mode
%marimo lesson_notebook.py --width 100%
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
```bash
git clone https://github.com/hublot-io/marimo-magic.git
cd marimo-magic
pip install -e .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [marimo](https://marimo.io) - The reactive Python notebook framework
- [Jupyter](https://jupyter.org/) - The foundation for interactive computing
- [Google Colab](https://colab.research.google.com/) - Free GPU access for everyone

## 🔗 Related Projects

- [marimo](https://github.com/marimo-team/marimo) - The main marimo project
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [Jupyter](https://github.com/jupyter/jupyter) - The Jupyter ecosystem 