#df = pd.read_excel("C:\Cloud\MSC\IT016-Cost Control INTERMODAL - TEMPLATE - MEDLOG\WEEK 2023\WEEK 01-23\MEDLOG GENOVA WEEK 01.xlsx")[['Call Port','Pre/On Carriage','Date Ref','Bill Of Lading','Container','Inland Locality','MTY Depot','MoT','Dry Port Location','Total Cost']]
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from IPython import display
from shiny import App, ui, render, reactive
display.set_matplotlib_formats("svg")
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


df = pd.read_excel("C:\Cloud\MSC\IT016-Cost Control INTERMODAL - TEMPLATE - MEDLOG\WEEK 2023\WEEK 01-23\MEDLOG GENOVA WEEK 01.xlsx")


app_ui = ui.page_fluid(
    ui.tags.h3("Earthquakes dataset visualizer", class_="app-heading"),
    ui.tags.div(class_="input_container", children=[
        ui.input_slider(
            id="slider_min_magnitude", 
            label="Minimum magnitude:", 
            min=df["Total Cost"].min(), 
            max=df["Total Cost"].max(), 
            value=df["Total Cost"].min(), 
            step=0.1
        ),
        ui.input_text(
            id="in_histogram_title", 
            label="Histogram title",
            value="Distribution of the Richter value"
        )
    ]),
    # Table
    ui.tags.div(class_="card", children=[
        ui.tags.p("Sample of 10 earthquakes", class_="card_title"),
        ui.output_table(id="quake_table", class_="quake_table")
    ]),
    # Histogram
    ui.tags.div(class_="card", children=[
        ui.output_text(id="out_histogram_title"),
        ui.output_plot(id="quake_histogram")
    ])
    
)


def server(input, output, session):
    @reactive.Calc
    def data():
        return df[df["Total Cost"] >= input.slider_min_magnitude()]

    @output
    @render.table
    def quake_table():
        return data().sample(10, replace=True)

    @output
    @render.text
    def out_histogram_title():
        return input.in_histogram_title()

    @output
    @render.plot
    def quake_histogram():
        fig, ax = plt.subplots()
        ax.hist(data()["Total Cost"], ec="#000000", color="#0099F8")
        return fig


www_dir = Path(__file__).parent / "www"
app = App(ui=app_ui, server=server, static_assets=www_dir)