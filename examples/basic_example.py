import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # 🧬 Marimo Magic Demo
        
        This is an example marimo notebook that demonstrates the basic functionality
        of the marimo magic command.
        
        ## Getting Started
        
        Load this notebook in Jupyter/Colab using:
        ```python
        %load_ext marimo_magic
        %marimo basic_example.py
        ```
        """
    )
    return


@app.cell
def __(mo):
    # Interactive slider example
    slider = mo.ui.slider(1, 100, value=50, label="Adjust me:")
    mo.md(f"**Interactive Slider:** {slider}")
    return (slider,)


@app.cell
def __(mo, slider):
    # Reactive computation
    result = slider.value * 2
    mo.md(f"**Reactive Result:** {slider.value} × 2 = **{result}**")
    return (result,)


@app.cell
def __(mo):
    # Code input example
    code_input = mo.ui.code_editor(
        value="print('Hello from marimo!')",
        language="python",
        label="Try editing this code:",
    )
    code_input
    return (code_input,)


@app.cell
def __(code_input):
    # Execute the user's code
    if code_input.value:
        exec(code_input.value)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Features Demonstrated
        
        - ✅ Interactive widgets (slider)
        - ✅ Reactive computation 
        - ✅ Code editor
        - ✅ Dynamic execution
        - ✅ Markdown rendering
        
        ## Next Steps
        
        Try the other examples:
        - `%marimo data_analysis_example.py` - Data science workflow
        - `%marimo --edit` - Create your own notebook
        """
    )
    return


if __name__ == "__main__":
    app.run()
