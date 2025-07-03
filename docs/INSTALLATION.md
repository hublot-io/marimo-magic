# 🚀 Installation Guide

## Quick Installation (Recommended for Colab)

### Option 1: Direct File Copy
Perfect for Google Colab and Jupyter environments:

```python
# Download the magic files directly
!wget -q https://raw.githubusercontent.com/hublot-io/marimo-magic/main/src/marimo_magic/__init__.py
!wget -q https://raw.githubusercontent.com/hublot-io/marimo-magic/main/src/marimo_magic/magic.py

# Create the package structure
!mkdir -p marimo_magic
!mv __init__.py magic.py marimo_magic/

# Load the extension
%load_ext marimo_magic
```

### Option 2: Git Clone
For development or local usage:

```bash
git clone https://github.com/hublot-io/marimo-magic.git
cd marimo-magic
```

Then in Python:
```python
import sys
sys.path.append('src')
%load_ext marimo_magic
```

## Package Installation (Future)

When published to PyPI:

```bash
pip install marimo-magic
```

```python
%load_ext marimo_magic
```

## Prerequisites

### Required Dependencies
- **Python 3.8+**
- **IPython/Jupyter** (comes with Colab)
- **marimo**: `pip install marimo`

### Optional Dependencies
- **uv** (recommended): `pip install uv`
  - Enables automatic dependency management
  - Better isolation for inline dependencies
  - Faster package installation

### Verification

Test your installation:

```python
%load_ext marimo_magic
%marimo --diagnose
```

This will check:
- ✅ UV availability
- ✅ Marimo installation
- ✅ Port allocation
- ✅ Environment detection

## Environment-Specific Setup

### Google Colab
Works out of the box! Colab provides:
- Python 3.10+
- IPython environment
- GPU access (if enabled)

```python
# Install marimo and uv
!pip install marimo uv

# Download and load marimo magic
!wget -q https://raw.githubusercontent.com/hublot-io/marimo-magic/main/src/marimo_magic/__init__.py
!wget -q https://raw.githubusercontent.com/hublot-io/marimo-magic/main/src/marimo_magic/magic.py
!mkdir -p marimo_magic && mv __init__.py magic.py marimo_magic/

%load_ext marimo_magic
```

### JupyterLab
```bash
pip install marimo uv marimo-magic
jupyter lab
```

```python
%load_ext marimo_magic
```

### Local Jupyter
```bash
pip install marimo uv marimo-magic
jupyter notebook
```

```python
%load_ext marimo_magic
```

### VS Code Jupyter
Works with VS Code's Jupyter extension:

```python
%load_ext marimo_magic
%marimo my_notebook.py
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: marimo_magic` | Ensure files are in Python path |
| `marimo command not found` | Install marimo: `pip install marimo` |
| `uv command not found` | Install uv: `pip install uv` (optional) |
| Server won't start | Run `%marimo --diagnose` |

### Debug Mode
Always use debug mode when troubleshooting:

```python
%marimo --debug --diagnose
```

### Manual Testing
Test marimo installation manually:

```bash
# Test marimo directly
python -m marimo --version

# Test uv (optional)
uv --version

# Test in Python
python -c "import marimo; print('✅ Marimo works')"
```

## Advanced Configuration

### Custom Python Path
If you have marimo in a custom location:

```python
import sys
sys.path.append('/path/to/marimo')
%load_ext marimo_magic
```

### Virtual Environments
Works with any Python environment:

```bash
# Create environment
python -m venv marimo_env
source marimo_env/bin/activate  # or marimo_env\Scripts\activate on Windows

# Install dependencies
pip install marimo uv marimo-magic

# Use in Jupyter
jupyter notebook
```

### Docker
```dockerfile
FROM python:3.11-slim

RUN pip install marimo uv jupyter marimo-magic

# Copy your notebooks
COPY . /workspace
WORKDIR /workspace

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
```

## Next Steps

After installation:

1. **Test basic functionality**: `%marimo --diagnose`
2. **Try the examples**: `%marimo basic_example.py`
3. **Create your first notebook**: `%marimo --edit`
4. **Read the usage guide**: See `docs/USAGE.md`

## Getting Help

- **Diagnostics**: `%marimo --diagnose`
- **Debug mode**: `%marimo --debug`
- **GitHub Issues**: [Report bugs](https://github.com/hublot-io/marimo-magic/issues)
- **Marimo Docs**: [Official Documentation](https://docs.marimo.io) 