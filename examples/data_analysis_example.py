# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "marimo",
#     "pandas>=1.3.0",
#     "matplotlib>=3.5.0",
#     "seaborn>=0.11.0",
#     "numpy>=1.21.0",
# ]
# ///

import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    # Set style
    plt.style.use("default")
    sns.set_palette("husl")

    return mo, pd, plt, sns, np


@app.cell
def __(mo):
    mo.md(
        r"""
        # 📊 Data Analysis with Marimo Magic
        
        This example demonstrates a complete data analysis workflow using marimo
        with inline dependencies (PEP 723).
        
        ## Features
        - **Inline Dependencies**: Automatic package management
        - **Interactive Widgets**: Dynamic data exploration  
        - **Reactive Plots**: Charts that update with user input
        - **Pandas Integration**: Seamless data manipulation
        """
    )
    return


@app.cell
def __(pd, np):
    # Generate sample data
    np.random.seed(42)
    n_samples = 1000

    data = pd.DataFrame(
        {
            "category": np.random.choice(["A", "B", "C", "D"], n_samples),
            "value1": np.random.normal(50, 15, n_samples),
            "value2": np.random.exponential(2, n_samples),
            "date": pd.date_range("2023-01-01", periods=n_samples, freq="H"),
        }
    )

    # Add some derived columns
    data["value_ratio"] = data["value1"] / data["value2"]
    data["month"] = data["date"].dt.month

    data.head()
    return data, n_samples


@app.cell
def __(mo):
    # Interactive controls
    category_filter = mo.ui.dropdown(
        options=["All", "A", "B", "C", "D"], value="All", label="Filter by category:"
    )

    chart_type = mo.ui.radio(
        options=["histogram", "boxplot", "scatter"],
        value="histogram",
        label="Chart type:",
    )

    mo.md(f"""
    **Interactive Controls:**
    
    {category_filter} {chart_type}
    """)
    return category_filter, chart_type


@app.cell
def __(data, category_filter):
    # Filter data based on selection
    if category_filter.value == "All":
        filtered_data = data
    else:
        filtered_data = data[data["category"] == category_filter.value]

    # Show summary
    summary = filtered_data.describe()
    summary
    return filtered_data, summary


@app.cell
def __(mo, filtered_data, chart_type, plt, sns):
    # Create reactive plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    if chart_type.value == "histogram":
        ax1.hist(filtered_data["value1"], bins=30, alpha=0.7, color="skyblue")
        ax1.set_title("Value1 Distribution")
        ax1.set_xlabel("Value1")
        ax1.set_ylabel("Frequency")

        ax2.hist(filtered_data["value2"], bins=30, alpha=0.7, color="lightcoral")
        ax2.set_title("Value2 Distribution")
        ax2.set_xlabel("Value2")
        ax2.set_ylabel("Frequency")

    elif chart_type.value == "boxplot":
        sns.boxplot(data=filtered_data, x="category", y="value1", ax=ax1)
        ax1.set_title("Value1 by Category")

        sns.boxplot(data=filtered_data, x="category", y="value2", ax=ax2)
        ax2.set_title("Value2 by Category")

    elif chart_type.value == "scatter":
        scatter = ax1.scatter(
            filtered_data["value1"],
            filtered_data["value2"],
            c=filtered_data["month"],
            cmap="viridis",
            alpha=0.6,
        )
        ax1.set_xlabel("Value1")
        ax1.set_ylabel("Value2")
        ax1.set_title("Value1 vs Value2 (colored by month)")

        plt.colorbar(scatter, ax=ax1, label="Month")

        # Time series on second plot
        monthly_avg = filtered_data.groupby("month")["value1"].mean()
        ax2.plot(monthly_avg.index, monthly_avg.values, marker="o")
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Average Value1")
        ax2.set_title("Monthly Average Value1")

    plt.tight_layout()
    mo.mpl.figure(fig)
    return ax1, ax2, fig


@app.cell
def __(mo, filtered_data):
    # Statistics table
    stats = (
        filtered_data.groupby("category")
        .agg({"value1": ["mean", "std", "count"], "value2": ["mean", "std", "count"]})
        .round(2)
    )

    mo.md(f"""
    ## Summary Statistics
    
    Filtered data contains **{len(filtered_data)}** rows.
    """)
    return (stats,)


@app.cell
def __(stats):
    stats
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Key Features Demonstrated
        
        ✅ **PEP 723 Dependencies**: Automatic package installation  
        ✅ **Interactive Filtering**: Dynamic data exploration  
        ✅ **Reactive Visualizations**: Charts update with controls  
        ✅ **Pandas Integration**: Seamless data manipulation  
        ✅ **Statistical Analysis**: Automated summary statistics  
        
        ## Usage with Marimo Magic
        
        ```python
        # The magic command automatically detects inline dependencies
        %marimo data_analysis_example.py --debug
        
        # Extended timeout for package installation
        # Uses --sandbox flag automatically
        # Shows installation progress
        ```
        
        This notebook showcases how marimo magic handles complex dependencies
        and provides a seamless data science workflow in Jupyter/Colab.
        """
    )
    return


if __name__ == "__main__":
    app.run()
