"""src/streaming/visualizations/live_visualizations_case.py.

Project-specific live visualization functions used by the Kafka consumer.

This module creates a live line chart of sale total by message.
The chart opens in a window while the consumer is running and updates
as each message is consumed.

Author: Denise Case
Date: 2026-05

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it live_visualizations_yourname.py,
  and modify your copy for your own charts.
"""

# === DECLARE IMPORTS ===

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

# === DECLARE EXPORTS ===

# Use the built-in __all__ variable to declare a list of
# public objects that this module exports.
# This is a common Python convention that helps other developers understand
# which functions are intended for use outside this module.

__all__ = [
    "close_live_chart",
    "init_live_chart",
    "save_live_chart",
    "update_live_chart",
]


# === DEFINE LIVE CHART HELPERS ===


def init_live_chart() -> tuple[Any, Any, dict[str, float]]:
    """Create and show an empty live chart.

    Returns:
        A tuple of (figure, axis, sales_by_payment).
    """
    # Matplotlib has a ion() function built in for "interactive ON" mode,
    # which allows the chart to update in real time as we modify it.
    # Call this function to turn on interactive mode.
    plt.ion()

    # Call subplots() to create a figure and axis for the chart.
    figure, axis = plt.subplots()

    # Initialize empty lists for x and y values.
    # These will be updated as messages are consumed.
    """
    x_values: list[int] = []
    y_values: list[float] = []
    """
    sales_by_payment: dict[str, float] = {}

    # Set the title and axis labels for the chart.
    axis.set_title("Sales Total by Payment Method")
    axis.set_xlabel("Payment Method")
    axis.set_ylabel("Sale Total ($)")

    # Call the figure.show() method to display the chart window.
    figure.show()

    # Call the figure.canvas.draw() method to
    # ensure the chart is rendered and responsive.
    figure.canvas.draw()

    # Call the figure.canvas.flush_events() method to process any pending GUI events,
    # which helps the chart window to update properly.
    figure.canvas.flush_events()

    # Return the figure, axis, and the sales_by_payment dictionary for later use.
    return figure, axis, sales_by_payment


def update_live_chart(
    *,
    figure: Any,
    axis: Any,
    sales_by_payment: dict[str, float],
    message: dict[str, Any],
) -> None:
    """Update the live chart with one consumed message.

    All arguments after the asterisk (*) must be passed as keyword arguments.

    Arguments:
        figure: Matplotlib figure.
        axis: Matplotlib axis.
        sales_by_payment: Dictionary mapping payment methods to their total sales.
        message: One enriched Kafka message dictionary.

    Returns:
        None.
    """
    # The message offset is a unique integer
    # that increments with each message,
    # so it works great as a simple x-axis value
    # to show the order of messages.
    # Create a new x value from the message offset.

    """
    new_x = int(message["_kafka_offset"])
    x_values.append(new_x)

    # Create a new y value from the "total" field in the message,
    # which contains the sale total for that message.
    new_y = float(message["total"])
    y_values.append(new_y)
    """
    # Update the sales_by_payment dictionary with the new message's payment method and sale total.
    payment_method = str(message["payment_method"])
    sale_total = float(message["total"])

    sales_by_payment[payment_method] = (
        sales_by_payment.get(payment_method, 0.0) + sale_total
    )
    # Clear the axis
    axis.clear()

    # Create new lists of x and y values from the updated sales_by_payment dictionary.
    methods = list(sales_by_payment.keys())
    totals = list(sales_by_payment.values())

    # Re-plot the updated values as a bar chart.
    axis.bar(methods, totals)

    # Set the title and axis labels again after clearing the axis.
    axis.set_title("Sales Total by Payment Method")
    axis.set_xlabel("Payment Method")
    axis.set_ylabel("Sale Total ($)")

    # Add a grid to the chart for better readability.
    axis.grid(True, axis="y")

    # Call the figure.canvas.draw() method to update the chart with the new data.
    figure.canvas.draw()

    # Call the figure.canvas.flush_events() method to process any pending GUI events,
    # which helps the chart to update properly.
    figure.canvas.flush_events()

    # Call plt.pause() with a short time (e.g., 0.05 seconds) to allow the chart to update.
    plt.pause(0.05)


def save_live_chart(
    *,
    figure: Any,
    chart_path: Path,
) -> None:
    """Save the final live chart to an image file.

    All arguments after the asterisk (*) must be passed as keyword arguments.

    Arguments:
        figure: Matplotlib figure.
        chart_path: Output image path.

    Returns:
        None.
    """
    # Ensure the output directory exists before saving the figure.
    chart_path.parent.mkdir(parents=True, exist_ok=True)

    # Use the figure.savefig() method to save the chart to an image file.
    # Use the bbox_inches="tight" argument to ensure the saved image is cropped to the content of the chart.
    figure.savefig(chart_path, bbox_inches="tight")


def close_live_chart() -> None:
    """Turn off interactive chart mode."""
    # Call plt.ioff() to turn off interactive mode when the consumer is finished.
    plt.ioff()
