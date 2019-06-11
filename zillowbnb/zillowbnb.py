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

GOOGLE_API_KEY = ''
DATA_FOLDER = os.path.abspath('../data')  + '/'
SOURCE_DATA = pd.read_csv(DATA_FOLDER +
                          c.DATASET_PROPERTIES[c.CITY].lower() + '_merged.csv')
COLUMNS = [SOURCE_DATA.columns[0]] + c.LISTING_COLUMNS[1:]

def convert_sentiment(dataframe):
    """
    Converts VADER sentiment score to feeling using scale found at
    https://github.com/cjhutto/vaderSentiment. Appends new value to input.

    :params dataframe dataframe:
    :returns dataframe dataframe:
    """

    dataframe['sentiment'] = ''
    dataframe.loc[dataframe['mean'] >= 0.05, 'sentiment'] = ':)'
    dataframe.loc[dataframe['mean'] <= -0.05, 'sentiment'] = ':('
    dataframe.loc[dataframe['sentiment'] == '', 'sentiment'] = ':|'
    return dataframe

def color_code_predicted_prices(dataframe):
    """
    Compares listing price and predicted price. Assigns listing value
    and color for good, average, and bad. Appends new values to input.

    :params dataframe dataframe:
    :returns dataframe dataframe:
    """

    color, value = ['price_color', 'price_value']
    dataframe[color] = ''
    dataframe.loc[dataframe['price'] > 1.1 * dataframe['predicted_price'], color] = 'red'
    dataframe.loc[dataframe['price'] < .9 * dataframe['predicted_price'], color] = 'green'
    dataframe.loc[dataframe[color] == '', color] = 'yellow'

    dataframe[value] = ''
    dataframe.loc[dataframe[color] == 'red', value] = 'Bad'
    dataframe.loc[dataframe[color] == 'green', value] = 'Good'
    dataframe.loc[dataframe[color] == 'yellow', value] = 'Average'

    dataframe['predicted_price'] = round(dataframe['predicted_price']).astype(int)
    return dataframe

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
    attr = attr
    old = old
    global GOOGLE_API_KEY #pylint: disable=W0603
    try:
        GOOGLE_API_KEY = new
        initiate_guest_view(GOOGLE_API_KEY)
        return GOOGLE_API_KEY
    except:
        raise ValueError(GOOGLE_API_KEY + ' is an invalid Google API Key.')

def initiate_guest_view(api_key, map_start=c.ADDRESS):
    """
    DOCSTRING HOLDER
    """

    city_lat, city_long = get_city_location(map_start, api_key)
    map_options = GMapOptions(lat=city_lat, lng=city_long, map_type='roadmap', zoom=11)
    plt = gmap(api_key, map_options, title=map_start)
    plt.circle(x='longitude', y='latitude', size=4, fill_color='price_color',
               fill_alpha=0.8, source=SOURCE, legend='price_value')

    tooltips = [
                ('Price', '$' + '@price'),
                ('Valued at', '$' + '@predicted_price'.split('.')[0]),
                ('Value', '@price_value'),
                ('Sentiment Score', '@sentiment')
                ]
    plt.add_tools(HoverTool(tooltips=tooltips))

    guest_layout = layout([[WIDGETS_GUEST, plt]], sizing_mode='stretch_both')
    curdoc().clear()
    curdoc().add_root(guest_layout)

def format_filters(dataframe, feature_list):
    """
    DOCSTRING HOLDER
    """
    data_frame = dataframe[feature_list]
    datatypes = np.unique(data_frame.dtypes)
    filter_dict = {}
    amenities = []

    for dtype in datatypes:
        columns = data_frame.select_dtypes([dtype])
        if dtype == np.object:
            for col in columns:
                values = list(np.unique(data_frame[col]))
                filter_dict[col] = values
        elif dtype in (np.int, np.float):
            for col in columns:
                if 'amenities_' in col:
                    amenities.append(col.replace('amenities_', ''))
                else:
                    min_c = min(data_frame[col])
                    max_c = max(data_frame[col])
                    values = [min_c, max_c]
                    filter_dict[col] = values
        else:
            pass

    filter_dict['amenities'] = sorted(amenities)
    return filter_dict

def update_data(attr, old, new, data=SOURCE_DATA):
    """
    DOCSTRING HOLDER
    """
    # pylint: disable=W0613,R0914
    attr = attr
    old = old
    new = new
    if USER_TYPE.active == 0:
        price_slider_value = list(PRICE_SLIDER.value)
        property_type = PROPERTY_TYPE_SELECT.value
        if property_type == []:
            property_type = np.unique(data.property_type)

        neighbourhoods = NEIGHBOURHOOD_SELECT.value
        if neighbourhoods == []:
            neighbourhoods = list(np.unique(data.neighbourhood_cleansed))

        for amenities in AMENITIES_SELECT.value: #pylint: disable=E1133
            amenities = 'amenities_' + amenities
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
    else:
        pass

def update_layout(attr, old, new):
    """
    DOCSTRING HOLDER
    """
    attr = attr
    old = old
    if new == 1:
        layout_switch = layout([[WIDGETS_HOST, HOST_PRICE]], sizing_mode='stretch_both')
        curdoc().clear()
        curdoc().add_root(layout_switch)
    else:
        initiate_guest_view(GOOGLE_API_KEY, CITY_INPUT.value)

def predict_price(new):
    """
    Holder
    """
    new = new
    if PREDICT_VALUE.active is True:
        listing_lat, listing_long = get_city_location(CITY_INPUT.value, API_KEY_INPUT.value)
        amenities = []
        for amenity in AMENITIES_SELECT.value: #pylint: disable=E1133
            amenities.append('amenities_' + amenity)

        amenities_converted = []
        list_amenities = []
        for col in c.LISTING_COLUMNS:
            if 'amenities_' in col:
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
        listing_df = pd.DataFrame(columns=['listing_id'] + c.LISTING_COLUMNS[1:])
        listing_df.loc[0] = data
        ints = ['listing_id', 'minimum_nights', 'maximum_nights']
        listing_df[ints] = listing_df[ints].astype(int)
        floats = ['latitude', 'longitude', 'accommodates',
                  'bathrooms', 'bedrooms', 'beds'] + list_amenities + ['price']
        listing_df[floats] = listing_df[floats].astype(float)

        converted = cm.to_matrix(listing_df, c.LISTING_COLUMNS)
        predicted_price = hp.predict_input(converted[0], c.DATASET_PROPERTIES[c.CITY])

        PREDICT_VALUE.active = False
        HOST_PRICE.text = ('Your listing is valued at: $' +
                           str(predicted_price[0]).split('.')[0] + ' per night')

SOURCE_DATA = convert_sentiment(SOURCE_DATA)
SOURCE_DATA = color_code_predicted_prices(SOURCE_DATA)
SOURCE_DATA = SOURCE_DATA.dropna()
SOURCE = ColumnDataSource(SOURCE_DATA)

FILTER_PROPERTIES = format_filters(SOURCE_DATA, COLUMNS)

# INPUT WIDGETS
API_KEY_INPUT = TextInput(value=GOOGLE_API_KEY, title='Google API Key')
API_KEY_INPUT.on_change('value', update_key)

CITY_INPUT = TextInput(value=c.ADDRESS, title='Location:')
# CITY_INPUT.on_change("value", update_map)

MIN_NIGHT_INPUT = TextInput(value='', title='Min. Nights:')
MAX_NIGHT_INPUT = TextInput(value='', title='Max. Nights:')

# Slider Widget
ACCOM = FILTER_PROPERTIES['accommodates']
ACCOMMODATES_SLIDER = Slider(start=ACCOM[0], end=ACCOM[1],
                             value=ACCOM[0], step=1, title='Accommodates')
ACCOMMODATES_SLIDER.on_change('value', update_data)

BED = FILTER_PROPERTIES['beds']
BED_SLIDER = Slider(start=BED[0], end=BED[1], value=BED[0], step=1, title='Beds')
BED_SLIDER.on_change('value', update_data)

BEDROOM = FILTER_PROPERTIES['bedrooms']
BEDROOM_SLIDER = Slider(start=BEDROOM[0], end=BEDROOM[1],
                        value=BEDROOM[0], step=1, title='Bedrooms')
BEDROOM_SLIDER.on_change('value', update_data)

BATHROOM = FILTER_PROPERTIES['bathrooms']
BATHROOM_SLIDER = Slider(start=BATHROOM[0], end=BATHROOM[1],
                         value=BATHROOM[0], step=0.5, title='Bathrooms')
BATHROOM_SLIDER.on_change('value', update_data)

NIGHTS = FILTER_PROPERTIES['minimum_nights']
NIGHTS_SLIDER = Slider(start=NIGHTS[0], end=NIGHTS[1],
                       value=NIGHTS[0], step=1, title='Nights')
NIGHTS_SLIDER.on_change('value', update_data)

# Range Slider Widget
PRICE = FILTER_PROPERTIES['price']
PRICE_SLIDER = RangeSlider(start=PRICE[0], end=PRICE[1],
                           value=(PRICE[0], PRICE[1]), step=50, title='Nightly Price')
PRICE_SLIDER.on_change('value', update_data)

# Multi Select Widgets
AMENITIES_SELECT = MultiSelect(title='Amenities:', value=[],
                               options=FILTER_PROPERTIES['amenities'])
AMENITIES_SELECT.on_change('value', update_data)

PROPERTY_TYPE_SELECT = MultiSelect(title='Property Type:', value=[],
                                   options=FILTER_PROPERTIES['property_type'])
PROPERTY_TYPE_SELECT.on_change('value', update_data)

NEIGHBOURHOOD_SELECT = MultiSelect(title='Neighbourhood:', value=[],
                                   options=FILTER_PROPERTIES['neighbourhood_cleansed'])
NEIGHBOURHOOD_SELECT.on_change('value', update_data)

# Checkbox Group (Multi Select) Widgets
NG_LIST = FILTER_PROPERTIES['neighbourhood_group_cleansed']
NEIGHBOURHOOD_GROUP = CheckboxButtonGroup(labels=NG_LIST,
                                          active=list(range(0, len(NG_LIST))))
NEIGHBOURHOOD_GROUP.on_change('active', update_data)

RT_LIST = FILTER_PROPERTIES['room_type']
ROOM_TYPE_GROUP = CheckboxButtonGroup(labels=FILTER_PROPERTIES['room_type'],
                                      active=list(range(0, len(RT_LIST))))
ROOM_TYPE_GROUP.on_change('active', update_data)

# Single Select Widgets
PROPERTY_TYPE_HOST = Select(title='Property Type:', value='',
                            options=[''] + FILTER_PROPERTIES['property_type'])
N_HOST = Select(title='Neighbourhood:', options=[''] + FILTER_PROPERTIES['neighbourhood_cleansed'])
NG_HOST = Select(title='Neighbourhood Group:', options=[''] + NG_LIST)
ROOM_TYPE_HOST = Select(title='Room Type:', value='', options=[''] + RT_LIST)

# Radio Button Widget
USER_TYPE = RadioButtonGroup(labels=['Guest', 'Host'], active=0)
USER_TYPE.on_change("active", update_layout)

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
