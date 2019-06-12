"""
Displays an interactive Bokeh visualization. View for "guests" to explore listings'
predicted value. View for hosts to detemine value of potential listing.
"""
import os
import pandas as pd
import numpy as np
from googlemaps import Client

from bokeh.models import GMapOptions, ColumnDataSource, HoverTool
from bokeh.plotting import gmap, curdoc
from bokeh.layouts import layout, widgetbox
from bokeh.models.widgets import RangeSlider, Slider, RadioButtonGroup, Toggle, Paragraph
from bokeh.models.widgets import CheckboxButtonGroup, MultiSelect, TextInput, Select

from submodule import constants as c
from submodule import convert_to_matrix as cm
from submodule import host_predict as hp

# Initializes Google Key Prompt
GOOGLE_API_KEY = ''

# Gets relative file path and opens source data (final merged and cleaned dataset)
DATA_FOLDER = os.path.abspath('../data')  + '/'
SOURCE_DATA = pd.read_csv(DATA_FOLDER +
                          c.DATASET_PROPERTIES[c.CITY].lower() + c.MERGE_SUFFIX)
COLUMNS = [SOURCE_DATA.columns[0]] + c.LISTING_COLUMNS[1:]

def convert_sentiment(dataframe):
    """
    Converts VADER sentiment score to feeling using scale found at
    https://github.com/cjhutto/vaderSentiment. Appends new value to input.

    :params dataframe dataframe:
    :returns dataframe dataframe:
    """

    dataframe[c.SENTIMENT] = c.EMPTY_STRING
    dataframe.loc[dataframe[c.MEAN] >= 0.05, c.SENTIMENT] = ':)'
    dataframe.loc[dataframe[c.MEAN] <= -0.05, c.SENTIMENT] = ':('
    dataframe.loc[dataframe[c.SENTIMENT] == c.EMPTY_STRING, c.SENTIMENT] = ':|'
    return dataframe

def color_code_predicted_prices(dataframe):
    """
    Compares listing price and predicted price. Assigns listing value
    and color for good, average, and bad. Appends new values to input.

    :params dataframe dataframe:
    :returns dataframe dataframe:
    """

    color, value = [c.PRICE_COLOR, c.PRICE_VALUE]

    dataframe[color] = c.EMPTY_STRING
    dataframe.loc[(dataframe[c.PRICE] > 1.1 *
                   dataframe[c.PREDICTED_PRICE], color)] = c.VALUE_DICT[c.BAD]
    dataframe.loc[(dataframe[c.PRICE] < .9 *
                   dataframe[c.PREDICTED_PRICE], color)] = c.VALUE_DICT[c.GOOD]
    dataframe.loc[dataframe[color] == '', color] = c.VALUE_DICT[c.AVERAGE]

    dataframe[value] = c.EMPTY_STRING
    dataframe.loc[dataframe[color] == c.VALUE_DICT[c.BAD], value] = c.BAD
    dataframe.loc[dataframe[color] == c.VALUE_DICT[c.GOOD], value] = c.GOOD
    dataframe.loc[dataframe[color] == c.VALUE_DICT[c.AVERAGE], value] = c.AVERAGE

    dataframe[c.PREDICTED_PRICE] = round(dataframe[c.PREDICTED_PRICE]).astype(int)
    return dataframe

def format_filters(dataframe, feature_list):
    """
    Finds the unique values, minimums, and maximums of each filter property in
    dataframe to initialize filter options and bounds.

    :params dataframe dataframe:
    :params feature_list list:
    :returns filter_dict dictionary:
    """

    data_frame = dataframe[feature_list]
    datatypes = np.unique(data_frame.dtypes)
    filter_dict = {}
    amenities = []

    # Splits dictionary value type by feature datatype.
    # Objects = get unique list
    # Ints and floats = get list of upper and lower bounds.
    for dtype in datatypes:
        columns = data_frame.select_dtypes([dtype])
        if dtype == np.object:
            for col in columns:
                values = list(np.unique(data_frame[col]))
                filter_dict[col] = values
        elif dtype in (np.int, np.float):
            for col in columns:
                if c.PREFIX in col:
                    amenities.append(col.replace(c.PREFIX, c.EMPTY_STRING))
                else:
                    min_c = min(data_frame[col])
                    max_c = max(data_frame[col])
                    values = [min_c, max_c]
                    filter_dict[col] = values
        else:
            pass

    filter_dict[c.AMENITIES] = sorted(amenities)
    return filter_dict

SOURCE_DATA = convert_sentiment(SOURCE_DATA)
SOURCE_DATA = color_code_predicted_prices(SOURCE_DATA)
SOURCE_DATA_FINAL = SOURCE_DATA.dropna()
SOURCE = ColumnDataSource(SOURCE_DATA_FINAL)

FILTER_PROPERTIES = format_filters(SOURCE_DATA_FINAL, COLUMNS)

def get_city_location(address, api_key=GOOGLE_API_KEY):
    """
    Uses Google's API to convert location to latitude and longitude.
    Used in centering the map.

    :params address string:
    :returns location list:
    """

    gmaps = Client(api_key)
    geocode = gmaps.geocode(address)
    location = list(geocode[0]['geometry']['location'].values())
    return location

def update_key(attr, old, new):
    """
    Validates provided Google API key, updates global API key and changes view
    if valid. Throws error and display doesn't change when invalid.

    :params attr string (changed attr's name):
    :params old string (old value):
    :params new string (new value):
    :returns GOOGLE_API_KEY string:
    """
    # ignore unused required bokeh parameters
    # pylint: disable = W0613

    global GOOGLE_API_KEY #pylint: disable=W0603
    try:
        GOOGLE_API_KEY = new
        initiate_guest_view(GOOGLE_API_KEY)
        update_data(attr, old, new, data=SOURCE_DATA_FINAL)
        return GOOGLE_API_KEY
    except:
        raise ValueError(GOOGLE_API_KEY + ' is an invalid Google API Key.')

def initiate_guest_view(api_key, map_start=c.ADDRESS):
    """
    Generates and updates visualization layout for guest users

    :params api_key string:
    :params map_start string:
    """

    # Centers map and plots listing locations
    city_lat, city_long = get_city_location(map_start, api_key)
    map_options = GMapOptions(lat=city_lat, lng=city_long, map_type='roadmap', zoom=11)
    plt = gmap(api_key, map_options, title=map_start)
    plt.circle(x=c.LONGITUDE, y=c.LATITIUDE, size=4, fill_color=c.PRICE_COLOR,
               fill_alpha=0.8, source=SOURCE, legend=c.PRICE_VALUE)

    # Configures hover display
    tooltips = [
                ('Price', '$' + '@price'),
                ('Valued at', '$' + '@predicted_price'.split('.')[0]),
                ('Value', '@price_value'),
                ('Sentiment Score', '@sentiment')
                ]
    plt.add_tools(HoverTool(tooltips=tooltips))

    guest_layout = layout([[WIDGETS_GUEST, plt]], sizing_mode=c.STRETCH_BOTH)
    curdoc().clear()
    curdoc().add_root(guest_layout)

def update_map(attr, old, new):
    """
    Centers the map based on location change on guest layouts

    :params attr string (changed attr's name):
    :params old string (old value):
    :params new string (new value):
    """
    # ignore unused required bokeh parameters
    # pylint: disable = W0613

    # Checks the filter changes where in the guest layout
    if USER_TYPE.active == 0:
        api_key = GOOGLE_API_KEY
        map_start = new
        initiate_guest_view(api_key, map_start)

def update_data(attr, old, new, data=SOURCE_DATA_FINAL):
    """
    Updates the listings displayed based on the guest filter selections.

    :params attr string (changed attr's name):
    :params old string (old value):
    :params new string (new value):
    :params data dataframe:
    """

    # ignore unused required bokeh parameters and too many local parameters
    # pylint: disable=W0613,R0914

    # Checks the filter changes where in the guest layout
    if USER_TYPE.active == 0:
        price_slider_value = list(PRICE_SLIDER.value)
        property_type = PROPERTY_TYPE_SELECT.value
        if property_type == []:
            property_type = np.unique(data.property_type)

        neighbourhoods = NEIGHBOURHOOD_SELECT.value
        if neighbourhoods == []:
            neighbourhoods = list(np.unique(data.neighbourhood_cleansed))

        for amenities in AMENITIES_SELECT.value: #pylint: disable=E1133
            amenities = c.PREFIX + amenities
            data = data[data[amenities] == 1]

        n_group = np.unique(data.neighbourhood_group_cleansed)
        ng_new = []
        for group in list(NEIGHBOURHOOD_GROUP.active):
            ng_new.append(n_group[group])

        r_type = np.unique(data.room_type)
        rt_new = []
        for room in list(ROOM_TYPE_GROUP.active):
            rt_new.append(r_type[room])

        data = data[data.neighbourhood_group_cleansed.isin(ng_new)]
        NEIGHBOURHOOD_SELECT.options = list(np.unique(data.neighbourhood_cleansed))

        indexes = ((data.accommodates >= ACCOMMODATES_SLIDER.value) &
                   (data.bedrooms >= BEDROOM_SLIDER.value) &
                   (data.beds >= BED_SLIDER.value) &
                   (data.bathrooms >= BATHROOM_SLIDER.value) &
                   (data.price >= price_slider_value[0]) &
                   (data.price <= price_slider_value[1]) &
                   (data.room_type.isin(rt_new)) &
                   (data.minimum_nights <= NIGHTS_SLIDER.value) &
                   (data.maximum_nights >= NIGHTS_SLIDER.value) &
                   (data.property_type.isin(property_type)))

        new_data = data[indexes]
        new_data = new_data[new_data.neighbourhood_cleansed.isin(neighbourhoods)]
        new_source = ColumnDataSource(new_data)
        SOURCE.data.update(new_source.data)

def update_layout(attr, old, new):
    """
    Updates displayed layout based on Host/Guest selection

    :params attr string (changed attr's name):
    :params old string (old value):
    :params new string (new value):
    """
    # ignore unused required bokeh parameters
    # pylint: disable = W0613

    # Initialize filter values
    ACCOMMODATES_SLIDER.value = ACCOM[0]
    AMENITIES_SELECT.value = []
    BATHROOM_SLIDER.value = BATHROOM[0]
    BED_SLIDER.value = BED[0]
    BEDROOM_SLIDER.value = BEDROOM[0]
    CITY_INPUT.value = c.ADDRESS
    HOST_PRICE.text = """Select all listing values and press
                          submit to view your listings valued price."""
    MIN_NIGHT_INPUT.value = c.EMPTY_STRING
    MAX_NIGHT_INPUT.value = c.EMPTY_STRING
    N_HOST.value = c.EMPTY_STRING
    NEIGHBOURHOOD_GROUP.active = list(range(0, len(NG_LIST)))
    NEIGHBOURHOOD_SELECT.options = FILTER_PROPERTIES[c.NC]
    NEIGHBOURHOOD_SELECT.value = []
    NG_HOST.value = c.EMPTY_STRING
    NIGHTS_SLIDER.value = NIGHTS[0]
    PRICE_SLIDER.value = (PRICE[0], PRICE[1])
    PROPERTY_TYPE_HOST.value = c.EMPTY_STRING
    PROPERTY_TYPE_SELECT.value = []
    ROOM_TYPE_GROUP.active = list(range(0, len(RT_LIST)))
    ROOM_TYPE_HOST.value = c.EMPTY_STRING

    # SOURCE.data.update(new_source.data)
    # new_source = ColumnDataSource(SOURCE_DATA_FINAL)

    if new == 1:
        layout_switch = layout([[WIDGETS_HOST, HOST_PRICE]], sizing_mode=c.STRETCH_BOTH)
        curdoc().clear()
        curdoc().add_root(layout_switch)
    else:
        initiate_guest_view(GOOGLE_API_KEY, CITY_INPUT.value)
        update_data(attr, old, new, data=SOURCE_DATA_FINAL)

def predict_price(new):
    """
    Predicts value of potential host listing based on selected values. updates
    text displayed in host layout

    :params new string (new value):
    """

    # ignore unused required bokeh parameters and too many local parameters
    # pylint: disable=W0613,R0914

    # Check submit was toggled on
    if PREDICT_VALUE.active is True:

        # Checks all model features have a value
        # pylint: disable=R0916
        if (CITY_INPUT.value == c.EMPTY_STRING
                or ROOM_TYPE_HOST.value == c.EMPTY_STRING
                or NG_HOST.value == c.EMPTY_STRING
                or N_HOST.value == c.EMPTY_STRING
                or PROPERTY_TYPE_HOST.value == c.EMPTY_STRING
                or MIN_NIGHT_INPUT.value == c.EMPTY_STRING
                or MAX_NIGHT_INPUT.value == c.EMPTY_STRING):

            PREDICT_VALUE.active = False
            HOST_PRICE.text = ('Check all single selection filters have a value.')

        # Checks string input for min and max nights can be conveted to integers.
        elif ((MIN_NIGHT_INPUT.value).isdigit() is False
              or (MAX_NIGHT_INPUT.value).isdigit() is False):

            PREDICT_VALUE.active = False
            HOST_PRICE.text = ('Min. and max. nights must be integers.')

        else:
            # Converts filter parameters to values and datatypes needed to feed into model
            listing_lat, listing_long = get_city_location(CITY_INPUT.value, API_KEY_INPUT.value)
            amenities = []
            for amenity in AMENITIES_SELECT.value: #pylint: disable=E1133
                amenities.append(c.PREFIX + amenity)

            amenities_converted = []
            list_amenities = []
            for col in c.LISTING_COLUMNS:
                if c.PREFIX in col:
                    list_amenities.append(col)
                    if col in amenities:
                        amenities_converted.append(1.0)
                    else:
                        amenities_converted.append(0.0)

            data = np.array([int(1), N_HOST.value, NG_HOST.value, listing_lat,
                             listing_long, PROPERTY_TYPE_HOST.value, ROOM_TYPE_HOST.value,
                             int(MIN_NIGHT_INPUT.value), int(MAX_NIGHT_INPUT.value),
                             int(ACCOMMODATES_SLIDER.value), BATHROOM_SLIDER.value,
                             BEDROOM_SLIDER.value, BED_SLIDER.value] +
                            amenities_converted + [1.0])

            listing_df = pd.DataFrame(columns=[c.LISTING_ID] + c.LISTING_COLUMNS[1:])
            listing_df.loc[0] = data

            ints = [c.LISTING_ID, c.MINIMUM_NIGHTS, c.MAXIMUM_NIGHTS]
            listing_df[ints] = listing_df[ints].astype(int)

            floats = [c.LATITIUDE, c.LONGITUDE, c.ACCOMMODATES,
                      c.BATHROOMS, c.BEDROOMS, c.BED] + list_amenities + [c.PRICE]
            listing_df[floats] = listing_df[floats].astype(float)

            converted = cm.to_matrix(listing_df, c.LISTING_COLUMNS)
            predicted_price = hp.predict_input(converted[0], c.DATASET_PROPERTIES[c.CITY])

            PREDICT_VALUE.active = False
            HOST_PRICE.text = ('Your listing is valued at: $' +
                               str(predicted_price[0]).split('.')[0] + ' per night')

# INPUT WIDGETS
API_KEY_INPUT = TextInput(value=GOOGLE_API_KEY, title='Google API Key')
API_KEY_INPUT.on_change(c.VALUE, update_key)

CITY_INPUT = TextInput(value=c.ADDRESS, title='Location:')
CITY_INPUT.on_change(c.VALUE, update_map)

MIN_NIGHT_INPUT = TextInput(value=c.EMPTY_STRING, title='Min. Nights:')
MAX_NIGHT_INPUT = TextInput(value=c.EMPTY_STRING, title='Max. Nights:')

# Slider Widget
ACCOM = FILTER_PROPERTIES[c.ACCOMMODATES]
ACCOMMODATES_SLIDER = Slider(start=ACCOM[0], end=ACCOM[1],
                             value=ACCOM[0], step=1, title='Accommodates')
ACCOMMODATES_SLIDER.on_change(c.VALUE, update_data)

BED = FILTER_PROPERTIES[c.BED]
BED_SLIDER = Slider(start=BED[0], end=BED[1], value=BED[0], step=1, title=c.BED)
BED_SLIDER.on_change(c.VALUE, update_data)

BEDROOM = FILTER_PROPERTIES[c.BEDROOMS]
BEDROOM_SLIDER = Slider(start=BEDROOM[0], end=BEDROOM[1],
                        value=BEDROOM[0], step=1, title='Bedrooms')
BEDROOM_SLIDER.on_change(c.VALUE, update_data)

BATHROOM = FILTER_PROPERTIES[c.BATHROOMS]
BATHROOM_SLIDER = Slider(start=BATHROOM[0], end=BATHROOM[1],
                         value=BATHROOM[0], step=0.5, title='Bathrooms')
BATHROOM_SLIDER.on_change(c.VALUE, update_data)

NIGHTS = FILTER_PROPERTIES[c.MINIMUM_NIGHTS]
NIGHTS_SLIDER = Slider(start=NIGHTS[0], end=NIGHTS[1],
                       value=NIGHTS[0], step=1, title='Nights')
NIGHTS_SLIDER.on_change(c.VALUE, update_data)

# Range Slider Widget
PRICE = FILTER_PROPERTIES[c.PRICE]
PRICE_SLIDER = RangeSlider(start=PRICE[0], end=PRICE[1],
                           value=(PRICE[0], PRICE[1]), step=50, title='Nightly Price')
PRICE_SLIDER.on_change(c.VALUE, update_data)

# Multi Select Widgets
AMENITIES_SELECT = MultiSelect(title='Amenities:', value=[],
                               options=FILTER_PROPERTIES[c.AMENITIES])
AMENITIES_SELECT.on_change(c.VALUE, update_data)

PROPERTY_TYPE_SELECT = MultiSelect(title='Property Type:', value=[],
                                   options=FILTER_PROPERTIES[c.PT])
PROPERTY_TYPE_SELECT.on_change(c.VALUE, update_data)

NEIGHBOURHOOD_SELECT = MultiSelect(title='Neighbourhood:', value=[],
                                   options=FILTER_PROPERTIES[c.NC])
NEIGHBOURHOOD_SELECT.on_change(c.VALUE, update_data)

# Checkbox Group (Multi Select) Widgets
NG_LIST = FILTER_PROPERTIES[c.NGC]
NEIGHBOURHOOD_GROUP = CheckboxButtonGroup(labels=NG_LIST,
                                          active=list(range(0, len(NG_LIST))))
NEIGHBOURHOOD_GROUP.on_change(c.ACTIVE, update_data)

RT_LIST = FILTER_PROPERTIES[c.RT]
ROOM_TYPE_GROUP = CheckboxButtonGroup(labels=FILTER_PROPERTIES[c.RT],
                                      active=list(range(0, len(RT_LIST))))
ROOM_TYPE_GROUP.on_change(c.ACTIVE, update_data)

# Single Select Widgets
PROPERTY_TYPE_HOST = Select(title='Property Type:', value=c.EMPTY_STRING,
                            options=[c.EMPTY_STRING] + FILTER_PROPERTIES[c.PT])
N_HOST = Select(title='Neighbourhood:', value=c.EMPTY_STRING,
                options=[c.EMPTY_STRING] + FILTER_PROPERTIES[c.NC])
NG_HOST = Select(title='Neighbourhood Group:', value=c.EMPTY_STRING,
                 options=[c.EMPTY_STRING] + NG_LIST)
ROOM_TYPE_HOST = Select(title='Room Type:', value=c.EMPTY_STRING,
                        options=[c.EMPTY_STRING] + RT_LIST)

# Radio Button Widget
USER_TYPE = RadioButtonGroup(labels=['Guest', 'Host'], active=0)
USER_TYPE.on_change(c.ACTIVE, update_layout)

# Button Toggle Widget
PREDICT_VALUE = Toggle(label='Submit', button_type='success')
PREDICT_VALUE.on_click(predict_price)

# Text Widget
HOST_PRICE = Paragraph(text="""Select all listing values and press
                        submit to view your listings valued price.""",
                       width=500, height=500)

WIDGETS_BOTH_1 = [USER_TYPE, CITY_INPUT]
WIDGETS_BOTH_2 = [ACCOMMODATES_SLIDER, BEDROOM_SLIDER, BED_SLIDER, BATHROOM_SLIDER]
WIDGETS_BOTH_3 = [AMENITIES_SELECT]

WIDGETS_GUEST = widgetbox(WIDGETS_BOTH_1 + [ROOM_TYPE_GROUP, PRICE_SLIDER] + WIDGETS_BOTH_2 +
                          [PROPERTY_TYPE_SELECT] + WIDGETS_BOTH_3 +
                          [NEIGHBOURHOOD_GROUP, NEIGHBOURHOOD_SELECT, NIGHTS_SLIDER])
WIDGETS_HOST = widgetbox(WIDGETS_BOTH_1 + [ROOM_TYPE_HOST, NG_HOST, N_HOST] + WIDGETS_BOTH_2 +
                         [PROPERTY_TYPE_HOST] + WIDGETS_BOTH_3 +
                         [MIN_NIGHT_INPUT, MAX_NIGHT_INPUT, PREDICT_VALUE])

INITIAL_LAYOUT = layout(API_KEY_INPUT)

curdoc().add_root(INITIAL_LAYOUT)
