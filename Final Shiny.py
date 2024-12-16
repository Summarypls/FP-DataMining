from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_plotly
import pandas as pd
import plotly.express as px
import os

os.chdir("E:/1 M A B A/Mining Gan/FinaPro/FP-DataMining")
data = pd.read_csv("osi.csv")

data = data.astype({
    'OperatingSystems': 'object',
    'Browser': 'object',
    'Region': 'object',
    'TrafficType': 'object',
    'Administrative': 'int',
    'Informational': 'int',
    'ProductRelated': 'int'
})

numerical_cols = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration','BounceRates','ExitRates','PageValues','SpecialDay']
categorical_cols = ['Administrative','Informational','ProductRelated','OperatingSystems', 'Browser', 'Region', 'TrafficType','Month','VisitorType','Weekend','Revenue']

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h2("Online Shoppers Purchasing Intention"),
            ui.input_slider("rows", "Number of Rows to Display", min=0, max=len(data), value=len(data)),
            ui.input_select("kontinu_x", "X-axis (Numerical)", choices=numerical_cols),
            ui.input_select("kontinu_y", "Y-axis (Numerical)", choices=numerical_cols),
            ui.input_select("kategori", "Categorical Variable", choices=categorical_cols),
        ),
        ui.layout_columns(
            ui.card(
                ui.output_text("header_x"),
                ui.output_text("avg_x")
            ),
            ui.card(
                ui.output_text("header_y"),
                ui.output_text("avg_y")
            ),
            ui.card(
                ui.h5("Number of Rows"),
                ui.output_text("n_records")
            )
        ),
        output_widget("scatter_plot")
    )
)

def server(input, output, session):

    @reactive.Calc
    def filtered_data():
        return data.iloc[:input.rows()]

    @output
    @render.text
    def header_x():
        return f"Average of {input.kontinu_x()}"

    @output
    @render.text
    def header_y():
        return f"Average of {input.kontinu_y()}"

    @output
    @render.text
    def avg_x():
        selected_x = input.kontinu_x()
        return f"{filtered_data()[selected_x].mean():.2f}"

    @output
    @render.text
    def avg_y():
        selected_y = input.kontinu_y()
        return f"{filtered_data()[selected_y].mean():.2f}"

    @output
    @render.text
    def n_records():
        return f"{len(filtered_data())}"

    @output
    @render_plotly
    def scatter_plot():
        df = filtered_data()
        fig = px.scatter(
            df, 
            x=input.kontinu_x(), 
            y=input.kontinu_y(),
            color=input.kategori(),
            title=f"Scatter Plot: {input.kontinu_x()} vs {input.kontinu_y()}",
            marginal_x="box",
            marginal_y="box",
            template="plotly_white"
        )
        return fig

app = App(app_ui, server)
app.run()