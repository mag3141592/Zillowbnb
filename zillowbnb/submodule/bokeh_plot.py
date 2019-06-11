"""
DOCSTRING HOLDER
"""
# pylint: disable=no-member
import pandas as pd
import numpy as np
from googlemaps import Client

from bokeh.models import GMapOptions, ColumnDataSource, HoverTool #, Label
from bokeh.plotting import gmap, curdoc #, figure
from bokeh.layouts import layout, widgetbox #, row
from bokeh.models.widgets import RangeSlider, Slider, RadioButtonGroup, Toggle
from bokeh.models.widgets import CheckboxButtonGroup, MultiSelect, TextInput, Select

import submodule.constants as constants
# import price_prediction as dp

GOOGLE_API_KEY = ''
SOURCE_DATA = pd.read_csv(constants.DATA_FOLDER +
                          constants.DATASET_PROPERTIES[constants.CITY].lower() + '_merged.csv')
COLUMNS = [SOURCE_DATA.columns[0]] + constants.LISTING_COLUMNS[1:]

def convert_sentiment(dataframe):
    """
    DOCSTRING HOLDER
    """
    dataframe['sentiment'] = ''
    dataframe.loc[dataframe['mean'] >= 0.05, 'sentiment'] = ':)'
    dataframe.loc[dataframe['mean'] <= -0.05, 'sentiment'] = ':('
    dataframe.loc[dataframe['sentiment'] == '', 'sentiment'] = ':|'
    return dataframe

def color_code_predicted_prices(dataframe):
    """
    DOCSTRING HOLDER
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
    DOCSTRING HOLDER
    """
    gmaps = Client(api_key)
    geocode = gmaps.geocode(address)
    location = list(geocode[0]['geometry']['location'].values())
    return location

def update_key(attr, old, new):
    """
    DOCSTRING HOLDER
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

def initiate_guest_view(api_key, map_start=constants.ADDRESS):
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
    # attr = attr
    # old = old
    # new = new
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
        layout_switch = layout([[WIDGETS_HOST, API_KEY_INPUT]], sizing_mode='stretch_both')
        curdoc().clear()
        curdoc().add_root(layout_switch)
    else:
        initiate_guest_view(GOOGLE_API_KEY, CITY_INPUT.value)

def predict_price(new):
    """
    Holder
    """
    new = new
    # listing_lat, listing_long = get_city_location(CITY_INPUT.value, API_KEY_INPUT.value)
    # print(AMENITIES_SELECT.value)
    # amenities = []
    # for amenity in AMENITIES_SELECT.value: #pylint: disable=E1133
    #     amenities.append('amenities_' + amenity)
    # listing_df = pd.DataFrame(columns=constants.LISTING_COLUMNS)
    # data = np.array([1, N_HOST.value, NG_HOST.value],
    #       constants.LISTING_COLUMNS[3]: [listing_lat],
    #      constants.LISTING_COLUMNS[4]: [listing_long],
    #      constants.LISTING_COLUMNS[5]: [PROPERTY_TYPE_HOST.value],
    #       constants.LISTING_COLUMNS[6]: [ROOM_TYPE_HOST.value],
    #       constants.LISTING_COLUMNS[7]: [MIN_NIGHT_INPUT.value],
    #       constants.LISTING_COLUMNS[8]: [MAX_NIGHT_INPUT.value],
    #       constants.LISTING_COLUMNS[9]: [ACCOMMODATES_SLIDER.value],
    #       constants.LISTING_COLUMNS[10]: [BATHROOM_SLIDER.value],
    #       constants.LISTING_COLUMNS[11]: [BEDROOM_SLIDER.value],
    #       constants.LISTING_COLUMNS[12]: [BED_SLIDER.value],
    #       constants.LISTING_COLUMNS[13]: [1] if constants.LISTING_COLUMNS[13] in amenities else 0,
    #       constants.LISTING_COLUMNS[14]: [1] if constants.LISTING_COLUMNS[14] in amenities else 0,
    #       constants.LISTING_COLUMNS[15]: [1] if constants.LISTING_COLUMNS[15] in amenities else 0,
    #       constants.LISTING_COLUMNS[16]: [1] if constants.LISTING_COLUMNS[16] in amenities else 0,
    #       constants.LISTING_COLUMNS[17]: [1] if constants.LISTING_COLUMNS[17] in amenities else 0,
    #       constants.LISTING_COLUMNS[18]: [1] if constants.LISTING_COLUMNS[18] in amenities else 0,
    #       constants.LISTING_COLUMNS[19]: [1] if constants.LISTING_COLUMNS[19] in amenities else 0,
    #       constants.LISTING_COLUMNS[20]: [1] if constants.LISTING_COLUMNS[20] in amenities else 0,
    #       constants.LISTING_COLUMNS[21]: [1] if constants.LISTING_COLUMNS[21] in amenities else 0,
    #       constants.LISTING_COLUMNS[22]: [1] if constants.LISTING_COLUMNS[22] in amenities else 0,
    #      constants.LISTING_COLUMNS[23]: [1] if constants.LISTING_COLUMNS[23] in amenities else 0,
    #       constants.LISTING_COLUMNS[24]: [1] if constants.LISTING_COLUMNS[24] in amenities else 0,
    #       constants.LISTING_COLUMNS[25]: [1] if constants.LISTING_COLUMNS[25] in amenities else 0,
    #      constants.LISTING_COLUMNS[26]: [1] if constants.LISTING_COLUMNS[26] in amenities else 0,
    #       constants.LISTING_COLUMNS[27]: [1] if constants.LISTING_COLUMNS[27] in amenities else 0,
    #      constants.LISTING_COLUMNS[28]: [1] if constants.LISTING_COLUMNS[28] in amenities else 0,
    #       constants.LISTING_COLUMNS[29]: [1] if constants.LISTING_COLUMNS[29] in amenities else 0,
    #      constants.LISTING_COLUMNS[30]: [1] if constants.LISTING_COLUMNS[30] in amenities else 0,
    #       constants.LISTING_COLUMNS[31]: [1] if constants.LISTING_COLUMNS[31] in amenities else 0,
    #       constants.LISTING_COLUMNS[32]: [1] if constants.LISTING_COLUMNS[32] in amenities else 0,
    #       constants.LISTING_COLUMNS[33]: [1] if constants.LISTING_COLUMNS[33] in amenities else 0,
    #       constants.LISTING_COLUMNS[34]: [1] if constants.LISTING_COLUMNS[34] in amenities else 0,
    #       constants.LISTING_COLUMNS[35]: [1] if constants.LISTING_COLUMNS[35] in amenities else 0,
    #       constants.LISTING_COLUMNS[36]: [1] if constants.LISTING_COLUMNS[36] in amenities else 0,
    #       constants.LISTING_COLUMNS[37]: [1] if constants.LISTING_COLUMNS[37] in amenities else 0,
    #       constants.LISTING_COLUMNS[38]: [1] if constants.LISTING_COLUMNS[38] in amenities else 0,
    #       constants.LISTING_COLUMNS[39]: [0]}
    # listing_df = pd.DataFrame(data=data)
    # # PREDICT_VALUE.active = False
    # print(listing_lat, listing_long, NG_HOST.value, N_HOST.value, listing_df)
    # test = dp.prediction(listing_df, constants.LISTING_COLUMNS)
    # print(test)

SOURCE_DATA = convert_sentiment(SOURCE_DATA)
SOURCE_DATA = color_code_predicted_prices(SOURCE_DATA)
SOURCE_DATA = SOURCE_DATA.dropna()
SOURCE = ColumnDataSource(SOURCE_DATA)

FILTER_PROPERTIES = format_filters(SOURCE_DATA, COLUMNS)

# INPUT WIDGETS
API_KEY_INPUT = TextInput(value=GOOGLE_API_KEY, title='Google API Key')
API_KEY_INPUT.on_change('value', update_key)

USER_TYPE = RadioButtonGroup(labels=['Guest', 'Host'], active=0)
USER_TYPE.on_change("active", update_layout)

CITY_INPUT = TextInput(value=constants.ADDRESS, title='Location:')
# CITY_INPUT.on_change("value", update_map)

MIN_NIGHT_INPUT = TextInput(value='', title='Min. Nights:')
MAX_NIGHT_INPUT = TextInput(value='', title='Max. Nights:')

# SLIDER WIDGETS
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

PRICE = FILTER_PROPERTIES['price']
PRICE_SLIDER = RangeSlider(start=PRICE[0], end=PRICE[1],
                           value=(PRICE[0], PRICE[1]), step=50, title='Nightly Price')
PRICE_SLIDER.on_change('value', update_data)

AMENITIES_SELECT = MultiSelect(title='Amenities:', value=[],
                               options=FILTER_PROPERTIES['amenities'])
AMENITIES_SELECT.on_change('value', update_data)

PROPERTY_TYPE_SELECT = MultiSelect(title='Property Type:', value=[],
                                   options=FILTER_PROPERTIES['property_type'])
PROPERTY_TYPE_SELECT.on_change('value', update_data)
PROPERTY_TYPE_HOST = Select(title='Property Type:', value='',
                            options=[''] + FILTER_PROPERTIES['property_type'])

NEIGHBOURHOOD_SELECT = MultiSelect(title='Neighbourhood:', value=[],
                                   options=FILTER_PROPERTIES['neighbourhood_cleansed'])
NEIGHBOURHOOD_SELECT.on_change('value', update_data)
N_HOST = Select(title='Neighbourhood:', options=[''] + FILTER_PROPERTIES['neighbourhood_cleansed'])

NG_LIST = FILTER_PROPERTIES['neighbourhood_group_cleansed']
NEIGHBOURHOOD_GROUP = CheckboxButtonGroup(labels=NG_LIST,
                                          active=list(range(0, len(NG_LIST))))
NEIGHBOURHOOD_GROUP.on_change('active', update_data)
NG_HOST = Select(title='Neighbourhood Group:', options=[''] + NG_LIST)

RT_LIST = FILTER_PROPERTIES['room_type']
ROOM_TYPE_GROUP = CheckboxButtonGroup(labels=FILTER_PROPERTIES['room_type'],
                                      active=list(range(0, len(RT_LIST))))
ROOM_TYPE_GROUP.on_change('active', update_data)
ROOM_TYPE_HOST = Select(title='Room Type:', value='', options=[''] + RT_LIST)

PREDICT_VALUE = Toggle(label='Submit', button_type='success')
PREDICT_VALUE.on_click(predict_price)

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
