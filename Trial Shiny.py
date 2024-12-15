import shiny
from shiny import App, ui, render, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.chdir("E:/1 M A B A/Mining Gan/FinaPro/FP-DataMining")
data = pd.read_csv("osi.csv")

data = data.astype({
    'OperatingSystems': 'object',
    'Browser': 'object',
    'Region': 'object',
    'TrafficType': 'object'
})

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h1("Online Shoppers Purchasing Intention"),
            ui.input_select("variable", "Select Variable", choices=data.columns.tolist()),
            ui.output_table("summary")
        ),
        ui.page_fixed(
            ui.output_plot("plot")  
        )
    )
)

def server(input, output, session):

    @reactive.Calc
    def selected_data():
        return data[input.variable()]  

    @output
    @render.table  
    def summary():
        selected = selected_data()
        if selected.dtype == 'object':  
            return selected.value_counts().reset_index().rename(columns={'index': 'Category', 0: 'Count'})
        elif selected.dtype == 'bool':  
            return selected.value_counts().reset_index().rename(columns={'index': 'Category', 0: 'Count'})
        else:  
            return selected.describe().reset_index().rename(columns={'index': 'Statistic', 0: 'Value'})

    @output
    @render.plot
    def plot():
        selected = selected_data()
        
        plt.figure(figsize=(6, 4))
        
        if selected.dtype == 'bool' or selected.nunique() == 2:
            sns.countplot(x=selected)
            plt.title(f"Bar Plot of {input.variable()} (0 vs 1)")

        elif selected.dtype == 'object':  
            sns.countplot(x=selected)
            plt.title(f"Bar Plot of {input.variable()}")

        else:  
            sns.histplot(selected, kde=True)
            plt.title(f"Histogram of {input.variable()}")

        plt.tight_layout()
        return plt.gcf()  
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
