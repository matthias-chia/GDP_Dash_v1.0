import plotly.graph_objects as go
import pandas as pd

def plot_time_series(df, x_col, y_cols, title="Time Series Plot", x_title="Date", y_title="Values"):
    """
    Plots a time series DataFrame using Plotly.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing time series data.
        x_col (str): The column name to be used as the x-axis.
        y_cols (list): A list of column names to be plotted on the y-axis.
        title (str): The title of the plot.
        x_title (str): The label for the x-axis.
        y_title (str): The label for the y-axis.

    Returns:
        None: Displays the plot.
    """
    # Initialize the Plotly figure
    fig = go.Figure()

    # Add a trace for each y-axis column
    for y_col in y_cols:
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode="lines+markers",
                name=y_col,
            )
        )

    # Customize the layout
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template="plotly_white",
        legend=dict(title="Legend"),
    )

    # Show the plot
    fig.show()
'''
# Example usage:
# Create a sample DataFrame
data = {
    "Date": pd.date_range(start="2020-01-01", periods=10, freq="M"),
    "Value1": [10, 15, 14, 20, 22, 25, 24, 28, 30, 35],
    "Value2": [5, 7, 6, 9, 11, 15, 13, 17, 18, 20],
}
df = pd.DataFrame(data)

# Plot the DataFrame
plot_time_series(df, x_col="Date", y_cols=["Value1", "Value2"], title="Sample Time Series")
'''