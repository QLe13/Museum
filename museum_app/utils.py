from .models import Visit, Item, Exhibit
from django.db.models import Count
import pandas as pd
from prophet import Prophet
from decimal import Decimal

def get_visit_data(exhibit_id):
    """
    Retrieves visit data for a specific exhibit and prepares it for time series forecasting.
    Args:
        exhibit_id (int): The ID of the exhibit to retrieve visit data for.

    Returns:
        pandas.DataFrame: A DataFrame containing the dates ('ds') and the number of visits per day ('y').
    """
    # Query the Visit model to get the number of visits per day for the exhibit
    visits = (
        Visit.objects
        .filter(exhibit_id=exhibit_id)
        .values('visit_date')
        .annotate(daily_visits=Count('id'))
        .order_by('visit_date')
    )
    # Convert the QuerySet to a pandas DataFrame
    gyatt = pd.DataFrame(list(visits))
    # general yielding attentive tentitve trace
    # Rename columns to 'ds' and 'y' as expected by Prophet
    gyatt['ds'] = pd.to_datetime(gyatt['visit_date'])
    gyatt['y'] = gyatt['daily_visits']
    # Return the DataFrame with the necessary columns
    return gyatt[['ds', 'y']]

def complete_date_range(gyatt):
    """
    Ensures that the DataFrame has a continuous date range with no missing dates
    by filling in any gaps with zero visits.

    Args:
        gyatt (pandas.DataFrame): The DataFrame containing the visit data with 'ds' and 'y' columns.

    Returns:
        pandas.DataFrame: The DataFrame with a continuous date range, missing dates filled with zero.
    """
    # Create a date range from the earliest to the latest date in the DataFrame
    all_dates = pd.date_range(start=gyatt['ds'].min(), end=gyatt['ds'].max())
    # Reindex the DataFrame to include all dates, filling missing values with 0
    gyatt = (
        gyatt.set_index('ds')
        .reindex(all_dates)
        .fillna(0)
        .rename_axis('ds')
        .reset_index()
    )
    return gyatt

def forecast_visits(gyatt, periods=365):
    """
    Uses Prophet to forecast future visitor counts based on historical data.
    Args:
        gyatt (pandas.DataFrame): The DataFrame containing historical visit data with 'ds' and 'y' columns.
        periods (int, optional): The number of future periods (days) to forecast. Defaults to 365.

    Returns:
        pandas.DataFrame: The DataFrame containing the forecasted visitor counts.
    """
    # Initialize the Prophet model
    model = Prophet()
    # Fit the model to the historical data
    model.fit(gyatt)
    # Create a DataFrame to hold predictions for future dates
    future = model.make_future_dataframe(periods=periods)
    # Predict future visitor counts
    forecast = model.predict(future)
    return forecast

def calculate_future_visits(forecast, last_date):
    """
    Calculates the total predicted future visits after the last actual visit date.

    Args:
        forecast (pandas.DataFrame): The DataFrame containing the forecasted visitor counts.
        last_date (datetime): The date of the last actual visit.

    Returns:
        Decimal: The total number of predicted future visits as a Decimal.
    """
    # Filter the forecast to include only future dates beyond the last actual visit date
    future_visits = forecast[forecast['ds'] > last_date]
    # Sum the predicted visitor counts
    total_future_visits = future_visits['yhat'].sum()
    return Decimal(total_future_visits)

def calculate_expected_revenue(total_future_visits, ticket_price):
    """
    Calculates the expected future revenue from ticket sales.

    Args:
        total_future_visits (Decimal): The total predicted future visits.
        ticket_price (Decimal): The current ticket price for the exhibit.

    Returns:
        Decimal: The expected future revenue.
    """
    # Multiply the total future visits by the ticket price
    return total_future_visits * ticket_price

def get_items_in_exhibit(exhibit_id):
    """
    Retrieves all items associated with a specific exhibit.

    Args:
        exhibit_id (int): The ID of the exhibit.

    Returns:
        QuerySet: A Django QuerySet containing all items in the exhibit.
    """
    # Query the Item model to get all items in the exhibit
    return Item.objects.filter(exhibit_id=exhibit_id)

def attribute_revenue_to_items(expected_revenue, items):
    """
    Distributes the expected revenue equally among all items in the exhibit.

    Args:
        expected_revenue (Decimal): The expected future revenue from ticket sales.
        items (QuerySet): A QuerySet of items in the exhibit.

    Returns:
        Decimal: The amount of revenue attributed to each item.
    """
    # Get the number of items in the exhibit
    number_of_items = items.count()
    # Calculate revenue per item
    revenue_per_item = expected_revenue / number_of_items if number_of_items else Decimal('0')
    return revenue_per_item

def update_cutoff_prices(exhibit_id):
    """
    Updates the cut-off prices for all items in an exhibit based on expected future revenue.

    Args:
        exhibit_id (int): The ID of the exhibit to update cut-off prices for.

    Returns:
        None
    """
    # Retrieve visit data for the exhibit
    gyatt = get_visit_data(exhibit_id)
    # Ensure the date range is complete
    gyatt = complete_date_range(gyatt)
    # Forecast future visits using Prophet
    forecast = forecast_visits(gyatt)
    # Get the date of the last actual visit
    last_actual_date = gyatt['ds'].max()
    # Calculate the total predicted future visits
    total_future_visits = calculate_future_visits(forecast, last_actual_date)
    # Retrieve the exhibit details
    exhibit = Exhibit.objects.get(id=exhibit_id)
    # Calculate the expected future revenue from ticket sales
    expected_revenue = calculate_expected_revenue(total_future_visits, exhibit.current_ticket_price)
    # Retrieve all items in the exhibit
    items = get_items_in_exhibit(exhibit_id)
    # Distribute the expected revenue equally among the items
    revenue_per_item = attribute_revenue_to_items(expected_revenue, items)
    # Update the cut-off price for each item
    for item in items:
        cutoff_price = item.price + revenue_per_item
        item.cutoff_price = cutoff_price
        item.save()  # Save the updated cut-off price to the database
        print(f"Updated cut-off price for item '{item.item_name}': {cutoff_price}")
