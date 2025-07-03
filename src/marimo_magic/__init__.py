"""
Marimo Magic for Jupyter/Colab
==============================

A custom IPython magic command to run marimo servers embedded in Jupyter notebooks.
Perfect for Google Colab integration with support for inline dependencies.

Usage:
    %load_ext marimo_magic
    %marimo experiments/my_notebook.py
    %marimo --edit
    %marimo --port 8080 --height 800
"""

__version__ = "1.0.0"
__author__ = "Nathan"
__email__ = ""
__description__ = (
    "IPython magic command for embedding marimo notebooks in Jupyter/Colab"
)

from .magic import (
    MarimoMagics,
    load_ipython_extension,
    unload_ipython_extension,
    register_marimo_magic,
)

__all__ = [
    "MarimoMagics",
    "load_ipython_extension",
    "unload_ipython_extension",
    "register_marimo_magic",
    "__version__",
]
