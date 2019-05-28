"""
DOCSTRING HOLDER
"""

import pandas as pd
import numpy as np
import requests

from bokeh.models import GMapOptions, ColumnDataSource, HoverTool
from bokeh.plotting import gmap, curdoc
from bokeh.layouts import layout, widgetbox
from bokeh.models.widgets import RangeSlider, Slider, RadioButtonGroup
from bokeh.models.widgets import CheckboxButtonGroup, MultiSelect, TextInput

COLUMNS = ['neighbourhood_cleansed', 'neighbourhood_group_cleansed',
           'latitude', 'longitude', 'property_type', 'room_type',
           'accommodates', 'bathrooms', 'bedrooms', 'beds', 'amenities_TV',
           'amenities_Heating', 'amenities_Air conditioning', 'amenities_Breakfast',
           'amenities_Laptop friendly workspace', 'amenities_Indoor fireplace',
           'amenities_Iron', 'amenities_Hair dryer', 'amenities_Private entrance',
           'amenities_Smoke detector', 'amenities_Carbon monoxide detector',
           'amenities_First aid kit', 'amenities_Fire extinguisher',
           'amenities_Lock on bedroom door', 'amenities_Pool',
           'amenities_Kitchen', 'amenities_Washer', 'amenities_Dryer',
           'amenities_Free parking on premises', 'amenities_Elevator',
           'amenities_Hot tub', 'amenities_Gym', 'amenities_Pets allowed',
           'amenities_Smoking allowed', 'amenities_Suitable for events',
           'amenities_Pets live on this property', 'price']
CITY = "Seattle"
STATE = "WA"
GOOGLE_API_KEY = ''
CLEANED_LISTINGS = pd.read_csv('CleanListings.csv')[COLUMNS]

def get_city_location(city, state, api_key):
    """
    DOCSTRING HOLDER
    """
    lat, long = (None, None)
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='
                            + city + ',+' + state + '&key=' + api_key)
    response = response.json()
    if response['results'] == []:
        print("City, State provided cannot be found.")
    else:
        results = response['results'][0]['geometry']['location']
        lat, long = results.values()
    return lat, long

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

def update_map(attr, old, new, api_key=GOOGLE_API_KEY, source1=ColumnDataSource(CLEANED_LISTINGS)):
    """
    DOCSTRING HOLDER
    """
    attr = attr
    old = old
    city, state = new.split(', ')
    city_la, city_lo = get_city_location(city, state, api_key)
    map_opt = GMapOptions(lat=city_la, lng=city_lo, map_type="roadmap", zoom=11)
    plt = gmap(api_key, map_opt, title=city + ', ' + state)
    plt.circle(x="longitude", y="latitude", size=5, fill_alpha=0.8, source=source1)
    plt.add_tools(HoverTool(tooltips=TOOLTIPS))

    guest_layout = layout([[WIDGETS, plt]], sizing_mode='stretch_both')
    curdoc().clear()
    curdoc().add_root(guest_layout)


def update_layout(attr, old, new):
    """
    DOCSTRING HOLDER
    """
    attr = attr
    old = old
    if new == 1:
        layout_switch = HOST_LAYOUT
    else:
        layout_switch = GUEST_LAYOUT
    curdoc().clear()
    curdoc().add_root(layout_switch)

def update_data(attr, old, new, data=CLEANED_LISTINGS):
    """
    DOCSTRING HOLDER
    """
    room_type_value = ROOM_TYPE_GROUP.active
    price_slider_value = PRICE_SLIDER.value
    accommodates_slider_value = ACCOMMODATES_SLIDER.value
    bedroom_slider_value = BEDROOM_SLIDER.value
    bed_slider_value = BED_SLIDER.value
    bathroom_slider_value = BATHROOM_SLIDER.value
    # property_type_value = property_type_select.value
    amenities_value = AMENITIES_SELECT.value
    neighbourhood_value = NEIGHBOURHOOD_SELECT.value
    neighbourhood_group_value = NEIGHBOURHOOD_GROUP.active

    ng = np.unique(data.neighbourhood_group_cleansed)
    ng_new = []

    rt = np.unique(data.room_type)
    rt_new = []

    if len(neighbourhood_value) == 0:
        neighbourhood_value = list(np.unique(data.neighbourhood_cleansed))

    for amenities in amenities_value:
        amenities = 'amenities_' + amenities
        data = data[data[amenities] == 1]

    for group in neighbourhood_group_value:
        ng_new.append(ng[group])

    for room in room_type_value:
        rt_new.append(rt[room])

    data = data[data.neighbourhood_group_cleansed.isin(ng_new)]
    NEIGHBOURHOOD_SELECT.options = list(np.unique(data.neighbourhood_cleansed))

    indexes = ((data.accommodates >= accommodates_slider_value) &
               (data.bedrooms >= bedroom_slider_value) &
               (data.beds >= bed_slider_value) &
               (data.bathrooms >= bathroom_slider_value) &
               (data.price >= price_slider_value[0]) &
               (data.price <= price_slider_value[1]) &
               (data.room_type.isin(rt_new)))

    new_data = data[indexes]
    new_data = new_data[new_data.neighbourhood_cleansed.isin(neighbourhood_value)]
    new_source = ColumnDataSource(new_data)
    SOURCE.data.update(new_source.data)

FILTER_PROPERTIES = format_filters(CLEANED_LISTINGS, COLUMNS)

USER_TYPE = RadioButtonGroup(labels=["Guest", "Host"], active=0)
USER_TYPE.on_change("active", update_layout)

CITY_INPUT = TextInput(value=CITY + ', ' + STATE, title="Location: (City, State)")
CITY_INPUT.on_change("value", update_map)

ACCOM = FILTER_PROPERTIES['accommodates']
ACCOMMODATES_SLIDER = Slider(start=ACCOM[0], end=ACCOM[1],
                             value=ACCOM[0], step=1, title="Accommodates")
ACCOMMODATES_SLIDER.on_change("value", update_data)

BED = FILTER_PROPERTIES['beds']
BED_SLIDER = Slider(start=BED[0], end=BED[1], value=BED[0], step=1, title="Beds")
BED_SLIDER.on_change("value", update_data)

BEDROOM = FILTER_PROPERTIES['bedrooms']
BEDROOM_SLIDER = Slider(start=BEDROOM[0], end=BEDROOM[1],
                        value=BEDROOM[0], step=1, title="Bedrooms")
BEDROOM_SLIDER.on_change("value", update_data)

BATHROOM = FILTER_PROPERTIES['bathrooms']
BATHROOM_SLIDER = Slider(start=BATHROOM[0], end=BATHROOM[1],
                         value=BATHROOM[0], step=0.5, title="Bathrooms")
BATHROOM_SLIDER.on_change("value", update_data)

PRICE = FILTER_PROPERTIES['price']
PRICE_SLIDER = RangeSlider(start=PRICE[0], end=PRICE[1],
                           value=(PRICE[0], PRICE[1]), step=50, title="Price")
PRICE_SLIDER.on_change("value", update_data)

AMENITIES_SELECT = MultiSelect(title="Amenities:", value=[],
                               options=FILTER_PROPERTIES['amenities'])
AMENITIES_SELECT.on_change("value", update_data)

PROPERTY_TYPE_SELECT = MultiSelect(title="Property_type:", value=[],
                                   options=FILTER_PROPERTIES['property_type'])
NEIGHBOURHOOD_SELECT = MultiSelect(title="Neighbourhood:", value=[],
                                   options=FILTER_PROPERTIES['neighbourhood_cleansed'])
NEIGHBOURHOOD_SELECT.on_change('value', update_data)

NG_LIST = FILTER_PROPERTIES['neighbourhood_group_cleansed']
NEIGHBOURHOOD_GROUP = CheckboxButtonGroup(labels=NG_LIST,
                                          active=list(range(0, len(NG_LIST))))
NEIGHBOURHOOD_GROUP.on_change("active", update_data)
RT_LIST = FILTER_PROPERTIES['room_type']
ROOM_TYPE_GROUP = CheckboxButtonGroup(labels=FILTER_PROPERTIES['room_type'],
                                      active=list(range(0, len(RT_LIST))))
ROOM_TYPE_GROUP.on_change('active', update_data)

SOURCE = ColumnDataSource(CLEANED_LISTINGS)
CITY_LAT, CITY_LONG = get_city_location(CITY, STATE, GOOGLE_API_KEY)
MAP_OPTIONS = GMapOptions(lat=CITY_LAT, lng=CITY_LONG, map_type="roadmap", zoom=11)
MAIN_PLT = gmap(GOOGLE_API_KEY, MAP_OPTIONS, title=CITY + ', ' + STATE)
MAIN_PLT.circle(x="longitude", y="latitude", size=5, fill_alpha=0.8, source=SOURCE)

TOOLTIPS = [
    ('Price', '$' + '@price'),
    ('Valued at', '$'),
    ('Value', ''),
    ('Sentiment Score', '')
]
MAIN_PLT.add_tools(HoverTool(tooltips=TOOLTIPS))


WIDGETS = widgetbox([USER_TYPE, CITY_INPUT, ROOM_TYPE_GROUP, PRICE_SLIDER,
                     ACCOMMODATES_SLIDER, BEDROOM_SLIDER, BED_SLIDER, BATHROOM_SLIDER,
                     PROPERTY_TYPE_SELECT, AMENITIES_SELECT, NEIGHBOURHOOD_GROUP,
                     NEIGHBOURHOOD_SELECT])
HOST_LAYOUT = layout([WIDGETS], sizing_mode='stretch_both')
GUEST_LAYOUT = layout([[WIDGETS, MAIN_PLT]], sizing_mode='stretch_both')
curdoc().add_root(GUEST_LAYOUT)
