"""Converts cleaned listings dataframe into matrix. It also provides metadata for said dataframe"""

def metadata(data_frame):
    """
    Creates metadata.
    :params dataframe data_frame:
    :returns dict:
    """
    if str(type(data_frame)) != "<class 'pandas.core.frame.DataFrame'>":
        raise ValueError("input must be a pandas Dataframe")

    if len(data_frame.columns) != 296:
        raise ValueError("Dataframe must have 296 columns")

    neighborhood = data_frame.neighbourhood_cleansed.unique()
    neighborhood.sort()
    neighborhood_group = data_frame.neighbourhood_group_cleansed.unique()
    neighborhood_group.sort()
    property_type = data_frame.property_type.unique()
    property_type.sort()
    room_type = data_frame.room_type.unique()
    room_type.sort()

    dict_n = {neighborhood[i]:i for i in range(len(neighborhood))}
    dict_ng = {neighborhood_group[i]:i for i in range(len(neighborhood_group))}
    dict_pt = {property_type[i]:i for i in range(len(property_type))}
    dict_rt = {room_type[i]:i for i in range(len(room_type))}
    columns = ['neighbourhood_cleansed', 'neighbourhood_group_cleansed',
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

    return {'neighborhood' : dict_n, 'neighborhood group' : dict_ng, "property type" : dict_pt,
            "room type" : dict_rt, "columns" : columns}

def to_matrix(data_frame):
    """
    Converts cleaned dataframe into matrix
    :params dataframe data_frame:
    :return matrix:
    """
    if str(type(data_frame)) != "<class 'pandas.core.frame.DataFrame'>":
        raise ValueError("input must be a pandas Dataframe")

    if len(data_frame.columns) != 296:
        raise ValueError("Dataframe must have 296 columns")

    df2 = data_frame[metadata(data_frame)['columns']]
    df2 = df2.dropna()

    df2["neighbourhood_cleansed"].replace(metadata(data_frame)['neighborhood'], inplace=True)
    df2["neighbourhood_group_cleansed"].replace(metadata(data_frame)['neighborhood group'],
                                                inplace=True)
    df2["property_type"].replace(metadata(data_frame)['property type'], inplace=True)
    df2["room_type"].replace(metadata(data_frame)['room type'], inplace=True)

    return df2.values
