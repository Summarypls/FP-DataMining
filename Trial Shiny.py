import shiny
from shiny import App, ui, render, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the working directory and load the data
os.chdir("E:/1 M A B A/Mining Gan/FinaPro")
data = pd.read_csv("osi.csv")

data = data.astype({
    'OperatingSystems': 'object',
    'Browser': 'object',
    'Region': 'object',
    'TrafficType': 'object'
})

# Define UI
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h1("Online Shoppers Purchasing Intention"),
            ui.input_select("variable", "Select Variable", choices=data.columns.tolist()),
            ui.output_table("summary")
        ),
        ui.page_fixed(
            ui.output_plot("plot")  # Main area to display the plot
        )
    )
)


# Define Server logic
def server(input, output, session):

    # Reactive expression to return selected data
    @reactive.Calc
    def selected_data():
        return data[input.variable()]  # Input variable selection

    # Summary Statistics (output as a table)
    @output
    @render.table  # Use render.table to show data in a table format
    def summary():
        selected = selected_data()
        if selected.dtype == 'object':  # For categorical data (strings)
            return selected.value_counts().reset_index().rename(columns={'index': 'Category', 0: 'Count'})
        elif selected.dtype == 'bool':  # For boolean data (True/False)
            return selected.value_counts().reset_index().rename(columns={'index': 'Category', 0: 'Count'})
        else:  # For numerical data
            return selected.describe().reset_index().rename(columns={'index': 'Statistic', 0: 'Value'})

    # Visualization (Bar plot for 0 and 1 and histogram for numerical data)
    @output
    @render.plot
    def plot():
        selected = selected_data()
        
        plt.figure(figsize=(6, 4))
        
        # Handle categorical data with 0 and 1 (binary data)
        if selected.dtype == 'bool' or selected.nunique() == 2:  # Handle binary or boolean data
            sns.countplot(x=selected)
            plt.title(f"Bar Plot of {input.variable()} (0 vs 1)")

        # Handle other categorical data (strings)
        elif selected.dtype == 'object':  # For categorical data
            sns.countplot(x=selected)
            plt.title(f"Bar Plot of {input.variable()}")

        # Handle numerical data (histogram)
        else:  # For numerical data
            sns.histplot(selected, kde=True)
            plt.title(f"Histogram of {input.variable()}")

        plt.tight_layout()
        return plt.gcf()  # Return the current figure to display in the plot
# Create the Shiny app
app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()
