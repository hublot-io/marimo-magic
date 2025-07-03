# 📖 Usage Guide

## Basic Commands

### Load Extension
```python
%load_ext marimo_magic
```

### Quick Start
```python
# Start with temporary notebook (run mode)
%marimo

# Create/edit notebooks (edit mode)
%marimo --edit

# Load specific notebook
%marimo my_notebook.py

# Custom dimensions
%marimo my_notebook.py --height 800 --width 90%
```

## Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `%marimo` | Start temporary notebook | `%marimo` |
| `%marimo <file>` | Load specific notebook | `%marimo analysis.py` |
| `%marimo --edit` | Create/edit notebooks | `%marimo --edit` |
| `%marimo <file> --edit` | Edit specific notebook | `%marimo analysis.py --edit` |
| `%marimo --stop <port>` | Stop server | `%marimo --stop 8080` |
| `%marimo --diagnose` | Run diagnostics | `%marimo --diagnose` |

### Detailed Options

```python
%marimo [notebook_path] [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `notebook_path` | str | None | Path to marimo notebook file |
| `--edit` | flag | False | Run in edit mode (vs run mode) |
| `--port` | int | auto | Server port number |
| `--height` | int | 600 | Iframe height in pixels |
| `--width` | str | "100%" | Iframe width |
| `--debug` | flag | False | Enable debug output |
| `--stop` | int | None | Stop server on specified port |
| `--test-connection` | flag | False | Test server connection |
| `--diagnose` | flag | False | Run comprehensive diagnostics |

## Run Mode vs Edit Mode

### 🔄 Run Mode (Default)
**Purpose**: Interactive execution and exploration

```python
%marimo my_notebook.py
```

**Features**:
- ✅ Execute cells interactively
- ✅ Interact with widgets
- ✅ View results and outputs
- ✅ Great for demos and presentations
- ❌ Cannot modify notebook structure

**Use Cases**:
- Presenting results to colleagues
- Interactive demos
- Exploring existing notebooks
- Teaching with pre-built content

### ✏️ Edit Mode
**Purpose**: Notebook development and modification

```python
%marimo my_notebook.py --edit
```

**Features**:
- ✅ Add, edit, delete cells
- ✅ Modify code and markdown
- ✅ Full IDE experience
- ✅ Save changes automatically
- ✅ Create new notebooks from scratch

**Use Cases**:
- Developing new notebooks
- Debugging existing code
- Rapid prototyping
- Learning marimo syntax

## Inline Dependencies (PEP 723)

Marimo magic automatically handles inline dependencies:

```python
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "marimo",
#     "pandas>=1.3.0",
#     "matplotlib>=3.5.0",
#     "seaborn>=0.11.0",
# ]
# ///

import marimo
# ... rest of notebook
```

**Automatic Features**:
- 🔍 **Detection**: Automatically detects PEP 723 headers
- 📦 **Sandbox**: Adds `--sandbox` flag to avoid terminal prompts
- ⏳ **Timeout**: Extends timeout to 5 minutes for installation
- 📊 **Progress**: Shows installation progress indicators
- 🔄 **UV Integration**: Uses `uv run marimo` when available

**Manual Override**:
```python
# Force sandbox mode
%marimo heavy_deps.py --debug

# This automatically:
# 1. Detects inline dependencies
# 2. Uses uv if available
# 3. Adds --sandbox flag
# 4. Extends timeout to 5 minutes
```

## Google Colab Integration

### Automatic Colab Detection
Marimo magic automatically detects Colab and:

- 🔗 **Proxy URLs**: Uses `google.colab.output.eval_js()` for proper proxy URLs
- 🖼️ **Smart Fallbacks**: Provides iframe + direct link options
- 🚀 **Auto-Open**: Opens in new tab if iframe fails
- 🔒 **Auth Bypass**: Uses `--no-token` to bypass authentication

### Colab-Specific Features

```python
# Enhanced display with Colab optimizations
%marimo my_notebook.py --height 800
```

**What you get**:
- Iframe embedding with Colab proxy URLs
- "Open Marimo Notebook" fallback button
- Automatic error handling for iframe restrictions
- Copy URL functionality
- Reload iframe button

### Iframe Issues in Colab
If iframe appears empty (common in Colab):

1. **Use the fallback button**: Click "Open Marimo Notebook"
2. **Direct URL**: Copy the proxy URL manually
3. **New tab**: Auto-opens in new tab after 3 seconds
4. **Debug mode**: Use `--debug` to see proxy URL details

## Performance Optimization

### Heavy Dependencies
For notebooks with large packages (torch, transformers, etc.):

```python
# First run (may take 3-5 minutes)
%marimo heavy_model.py --debug

# Subsequent runs (much faster)
%marimo heavy_model.py
```

**Tips**:
- Use `--debug` to see installation progress
- Be patient on first run with heavy packages
- UV caches dependencies for faster subsequent runs
- Consider pre-installing heavy packages manually

### Memory Management
```python
# Stop unused servers to free memory
%marimo --stop 8080
%marimo --stop 2718

# Check running servers
!ps aux | grep marimo
```

## Workflow Examples

### Data Science Workflow
```python
# 1. Start with exploration
%marimo --edit --height 700

# 2. Load existing analysis
%marimo data_analysis.py --edit

# 3. Present results
%marimo data_analysis.py --height 900

# 4. Share with team
%marimo data_analysis.py --port 8080
# Share the Colab link with colleagues
```

### ML Model Development
```python
# 1. Prototype in edit mode
%marimo model_dev.py --edit --debug

# 2. Test with different parameters
%marimo model_dev.py --port 3000

# 3. Demo to stakeholders
%marimo model_demo.py --height 800

# 4. Clean up
%marimo --stop 3000
```

### Teaching/Learning
```python
# Student exploration
%marimo --edit --height 600

# Instructor demo
%marimo lesson.py

# Interactive exercises
%marimo exercises.py --edit
```

## Debugging and Troubleshooting

### Debug Mode
Always start with debug mode when troubleshooting:

```python
%marimo my_notebook.py --debug
```

**Debug output includes**:
- Command being executed
- UV availability detection
- Environment variables set
- Server startup progress
- URL validation results

### Comprehensive Diagnostics
```python
%marimo --diagnose
```

**Checks performed**:
- ✅ UV installation and version
- ✅ Marimo installation (via UV and Python)
- ✅ Port allocation testing
- ✅ Server startup tests (run and edit modes)
- ✅ Environment detection (Colab vs Jupyter)
- ✅ Proxy URL generation (Colab)

### Connection Testing
```python
# Test specific server
%marimo --test-connection --port 8080
```

**Tests performed**:
- Socket connection to port
- HTTP request validation
- Content verification
- Process status check

### Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Server won't start** | Timeout errors | Run `%marimo --diagnose` |
| **Dependencies not installing** | Import errors | Ensure UV is installed, check `--debug` output |
| **Iframe empty in Colab** | Blank white box | Click "Open Marimo Notebook" button |
| **Edit mode timeout** | Long startup time | Wait 3-5 minutes for heavy dependencies |
| **Port conflicts** | Connection refused | Use different port: `--port 3000` |
| **Memory issues** | Slow performance | Stop unused servers: `--stop <port>` |

### Manual Verification
Test components individually:

```bash
# Test marimo directly
python -m marimo --version

# Test UV
uv --version

# Test in isolated environment
python -c "import marimo; print('OK')"
```

## Advanced Usage

### Custom Ports
```python
# Use specific port
%marimo my_notebook.py --port 3000

# Multiple notebooks simultaneously
%marimo notebook1.py --port 3000
%marimo notebook2.py --port 3001
```

### Custom Dimensions
```python
# Tall notebook for data exploration
%marimo analysis.py --height 1000

# Wide notebook for dashboards
%marimo dashboard.py --width 95%

# Compact for quick demos
%marimo demo.py --height 400 --width 80%
```

### Batch Operations
```python
# Start multiple notebooks
notebooks = ['analysis.py', 'model.py', 'viz.py']
ports = [3000, 3001, 3002]

for notebook, port in zip(notebooks, ports):
    %marimo {notebook} --port {port}
```

### Server Management
```python
# List all marimo processes
!ps aux | grep marimo

# Stop all marimo servers
!pkill -f marimo

# Stop specific servers
for port in [3000, 3001, 3002]:
    %marimo --stop {port}
```

## Best Practices

### Development
1. **Use edit mode for development**: `%marimo --edit`
2. **Use debug mode when troubleshooting**: `%marimo --debug`
3. **Test with simple notebooks first**: Start with basic examples
4. **Save frequently**: Edit mode auto-saves, but use Ctrl+S

### Presentation
1. **Use run mode for demos**: `%marimo notebook.py`
2. **Optimize dimensions**: Adjust `--height` and `--width`
3. **Test in target environment**: Verify in Colab if presenting there
4. **Prepare fallback links**: Have direct URLs ready

### Collaboration
1. **Share Colab notebooks**: Include marimo magic setup
2. **Document dependencies**: Use PEP 723 headers
3. **Test in clean environment**: Verify dependencies install correctly
4. **Provide examples**: Include sample notebooks

### Performance
1. **Use UV when possible**: Faster dependency management
2. **Pre-install heavy packages**: Avoid timeouts
3. **Stop unused servers**: Free up memory and ports
4. **Monitor resource usage**: Check RAM and CPU in Colab 