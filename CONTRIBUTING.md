# 🤝 Contributing to Marimo Magic

Thank you for your interest in contributing to Marimo Magic! This guide will help you get started.

## 🚀 Quick Start

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/hublot-io/marimo-magic.git
cd marimo-magic
```

2. **Set up development environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -e .
pip install -e .[dev]
```

3. **Install marimo and uv**
```bash
pip install marimo uv
```

4. **Test your setup**
```python
# Test in Jupyter/IPython
%load_ext marimo_magic
%marimo --diagnose
```

## 📝 Development Workflow

### Making Changes

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Edit code in `src/marimo_magic/`
   - Update documentation in `docs/`
   - Add examples in `examples/`

3. **Test your changes**
```python
# Test basic functionality
%load_ext marimo_magic
%marimo examples/basic_example.py --debug

# Test with inline dependencies
%marimo examples/data_analysis_example.py --debug

# Test diagnostics
%marimo --diagnose
```

4. **Run code quality checks**
```bash
# Format code
black src/
isort src/

# Check linting
flake8 src/
```

### Testing Environments

Test your changes in multiple environments:

- **Local Jupyter**: `jupyter notebook`
- **JupyterLab**: `jupyter lab`
- **Google Colab**: Upload and test
- **VS Code**: Test with Jupyter extension

## 🎯 Areas for Contribution

### High-Priority Areas

1. **Performance Optimization**
   - Faster dependency detection
   - Better caching mechanisms
   - Memory usage optimization

2. **Error Handling**
   - Better error messages
   - Recovery mechanisms
   - Graceful fallbacks

3. **Platform Support**
   - Windows compatibility testing
   - Different Jupyter distributions
   - Cloud platform integrations

4. **Documentation**
   - More examples
   - Video tutorials
   - Best practices guides

### Feature Ideas

- **Notebook Templates**: Pre-built notebook templates
- **Dependency Validation**: Check compatibility before installation
- **Performance Monitoring**: Built-in profiling tools
- **Multi-Server Management**: Easier server lifecycle management
- **Export Capabilities**: Export to static HTML/PDF
- **Integration Plugins**: VS Code extension, JupyterLab extension

## 🐛 Bug Reports

### Before Reporting

1. **Check existing issues**: Search GitHub issues
2. **Test with latest version**: Update to latest code
3. **Run diagnostics**: `%marimo --diagnose`
4. **Try debug mode**: `%marimo --debug`

### Bug Report Template

```markdown
**Bug Description**
A clear description of the bug.

**Environment**
- OS: [e.g., Ubuntu 22.04, Windows 11, macOS]
- Python version: [e.g., 3.11.5]
- Jupyter environment: [e.g., Colab, JupyterLab 4.0, Notebook 7.0]
- UV version: [output of `uv --version`]
- Marimo version: [output of `python -m marimo --version`]

**Reproduction Steps**
1. Load extension: `%load_ext marimo_magic`
2. Run command: `%marimo test.py --debug`
3. See error: [error message]

**Expected Behavior**
What should have happened.

**Actual Behavior**
What actually happened.

**Debug Output**
```
[paste output from %marimo --debug or %marimo --diagnose]
```

**Additional Context**
Any other relevant information.
```

## ✨ Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why would this feature be useful? What problem does it solve?

**Proposed Implementation**
How might this feature be implemented? (Optional)

**Alternatives Considered**
Other ways to achieve the same goal? (Optional)

**Additional Context**
Any other relevant information.
```

## 📋 Code Guidelines

### Python Style

- **Follow PEP 8**: Use black and isort for formatting
- **Type hints**: Add type hints for new functions
- **Docstrings**: Document all public functions
- **Error handling**: Always handle exceptions gracefully

### Code Structure

```python
def new_function(param: str, debug: bool = False) -> bool:
    """
    Brief description of the function.
    
    Args:
        param: Description of param
        debug: Enable debug output
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        RuntimeError: When something goes wrong
    """
    try:
        # Implementation
        if debug:
            print(f"Debug: processing {param}")
        return True
    except Exception as e:
        if debug:
            print(f"Error: {e}")
        return False
```

### Documentation

- **Update README**: Reflect new features
- **Update USAGE.md**: Add usage examples
- **Update examples**: Create relevant examples
- **Inline comments**: Explain complex logic

## 🧪 Testing

### Manual Testing Checklist

- [ ] **Basic functionality**
  - [ ] Load extension: `%load_ext marimo_magic`
  - [ ] Start server: `%marimo --debug`
  - [ ] Stop server: `%marimo --stop <port>`

- [ ] **Run mode**
  - [ ] Default notebook: `%marimo`
  - [ ] Specific file: `%marimo examples/basic_example.py`
  - [ ] Custom dimensions: `%marimo --height 800`

- [ ] **Edit mode**
  - [ ] New notebook: `%marimo --edit`
  - [ ] Edit existing: `%marimo examples/basic_example.py --edit`

- [ ] **Dependencies**
  - [ ] No dependencies: Basic Python files
  - [ ] Inline dependencies: PEP 723 format
  - [ ] Heavy dependencies: torch, transformers

- [ ] **Diagnostics**
  - [ ] Full diagnostics: `%marimo --diagnose`
  - [ ] Connection test: `%marimo --test-connection --port <port>`

- [ ] **Error handling**
  - [ ] Missing file: `%marimo nonexistent.py`
  - [ ] Port conflicts: Multiple servers on same port
  - [ ] Network issues: Simulated connection failures

### Automated Testing (Future)

We plan to add automated testing with:

- **Unit tests**: Core functionality
- **Integration tests**: End-to-end workflows  
- **Environment tests**: Different Jupyter setups
- **Performance tests**: Memory and speed benchmarks

## 📦 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update version**: In `pyproject.toml` and `__init__.py`
2. **Update CHANGELOG**: Document changes
3. **Test thoroughly**: Multiple environments
4. **Create release**: GitHub release with notes
5. **Publish package**: To PyPI (when ready)

## 🏷️ Labels and Project Management

### Issue Labels

- **bug**: Something isn't working
- **enhancement**: New feature or request
- **documentation**: Improvements to docs
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention needed
- **priority/high**: Critical issues
- **platform/colab**: Google Colab specific
- **platform/jupyter**: Jupyter specific

### Pull Request Process

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes** with tests
4. **Update documentation**
5. **Create pull request** with description
6. **Address review feedback**
7. **Merge when approved**

## 💬 Communication

### Getting Help

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Discord/Slack**: Real-time chat (if available)

### Code of Conduct

- **Be respectful**: Treat everyone with courtesy
- **Be inclusive**: Welcome all contributors
- **Be constructive**: Provide helpful feedback
- **Be patient**: Remember we're all learning

## 🎉 Recognition

Contributors will be:

- **Listed in README**: All contributors acknowledged
- **Mentioned in releases**: Notable contributions highlighted
- **Invited to discuss**: Major decisions and roadmap

Thank you for contributing to Marimo Magic! Your contributions help make interactive Python notebooks more accessible to everyone. 🚀 