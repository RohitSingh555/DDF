def get_valid_data_type(column_name):
    # Assigning data types based on column names
    column_name_lower = column_name.lower()
    if 'id' in column_name_lower:
        return 'INT'
    elif 'date' in column_name_lower:
        return 'DATE'
    elif 'price' in column_name_lower or 'fee' in column_name_lower:
        return 'DECIMAL(10, 2)'
    elif 'size' in column_name_lower or 'area' in column_name_lower or 'length' in column_name_lower or 'width' in column_name_lower:
        return 'DECIMAL(8, 2)'
    elif 'room' in column_name_lower or 'level' in column_name_lower:
        return 'VARCHAR(20)'
    elif 'url' in column_name_lower or 'link' in column_name_lower:
        return 'VARCHAR(255)'
    elif 'description' in column_name_lower or 'remarks' in column_name_lower or 'features' in column_name_lower:
        return 'TEXT'
    elif 'latitude' in column_name_lower or 'longitude' in column_name_lower:
        return 'FLOAT'
    else:
        return 'VARCHAR(100)'  # Default data type

def generate_create_table_query(columns1, columns2, table_name):
    # Generating a CREATE TABLE query based on the given columns and table name
    all_columns = set(columns1).union(columns2)
    query = f"CREATE TABLE {table_name} ("
    for i, column in enumerate(all_columns):
        data_type = get_valid_data_type(column)
        query += f"{column} {data_type}"
        if i < len(all_columns) - 1:
            query += ", "
    query += ");"
    return query

table1_columns = set([
    'ID', 'HeatingType', 'Acreage', 'Franchisor', 'EndDateTime', 'Amenities', 'StartDateTime', 'StreetDirectionSuffix',
    'BasementType', 'BedroomsAboveGround', 'MunicipalId', 'BusinessSubType', 'FenceTotal', 'FireplaceType', 'Designations',
    'BedroomsBelowGround', 'OrganizationType', 'HalfBathTotal', 'Lease', 'Price', 'BedroomsTotal', 'SizeTotal',
    'ViewType', 'PublicRemarks', 'SizeInterior', 'Longitude', 'MaintenanceFeePaymentUnit', 'Width', 'Comments',
    'BathroomTotal', 'Country', 'Age', 'ConstructionStyleSplitLevel', 'SizeIrregular', 'Event', 'StoriesTotal',
    'PostalCode', 'PoolType', 'FarmType', 'WaterFrontType', 'OwnershipType', 'TransactionType', 'Photo', 'CommunityName',
    'SocialMediaWebsite', 'Fixture', 'Designation', 'Phone', 'StreetName', 'ZoningDescription', 'StreetNumber', 'PropertyPhoto',
    'City', 'Description', 'Structure', 'StreetAddress', 'LargePhotoURL', 'Subdivision', 'Address', 'AgentDetails', 'Website',
    'BasementFeatures', 'ThumbnailURL', 'Addressline2', 'CommunicationType', 'Rooms', 'Name', 'RentalEquipmentType',
    'CommunityFeatures', 'Level', 'LeaseType', 'HeatingFuel', 'Franchise', 'RoadType', 'MaintenanceFeeType', 'PhotoURL',
    'Logo', 'LocationDescription', 'MaintenanceFee', 'ArchitecturalStyle', 'Business', 'SizeTotalText', 'Sewer',
    'WaterFrontName', 'Position', 'AmmenitiesNearBy', 'Province', 'SizeExterior', 'Office', 'LeasePerTime', 'Phones',
    'Board', 'Land', 'PropertyType', 'ParkingSpaceTotal', 'Parking', 'FoundationType', 'TotalFinishedArea', 'ManagementCompany',
    'FireProtection', 'SizeDepth', 'AddressLine1', 'Spaces', 'AccessType', 'StreetSuffix', 'ParkingSpaces', 'Type', 'Building',
    'OpenHouse', 'PropertyDetails', 'LeasePerUnit', 'ConstructionMaterial', 'Length', 'Neighbourhood', 'Websites',
    'LandscapeFeatures', 'LogoLastUpdated', 'ConstructionStyleAttachment', 'CoolingType', 'UtilityWater', 'ConstructionStyleOther',
    'Utility', 'ListingID', 'RoofMaterial', 'EquipmentType', 'ListingContractDate', 'SizeFrontage', 'Features', 'ConstructedDate',
    'FireplaceTotal', 'BasementDevelopment', 'Plan', 'LastUpdated', 'Dimension', 'Appliances', 'FlooringType', 'Latitude',
    'PhotoLastUpdated', 'FireplaceFuel', 'UtilitiesAvailable', 'ExteriorFinish', 'SequenceId', 'Room', 'StorageType', 'BusinessType',
    'FireplacePresent', 'RoofStyle', 'FenceType', 'ZoningType'
])
data_columns = """ArchitecturalStyle AssociationFee AssociationFeeFrequency AttachedGarageYN BathroomsHalf BathroomsTotal BedroomsTotal BuildingAreaTotal BuildingAreaUnits CarportSpaces CarportYN City CoListAgentCellPhone CoListAgentDesignation CoListAgentDirectPhone CoListAgentEmail CoListAgentFax CoListAgentFullName CoListAgentKey CoListAgentOfficePhone CoListAgentOfficePhoneExt CoListAgentPager CoListAgentTollFreePhone CoListAgentURL CoListOfficeFax CoListOfficeKey CoListOfficeName CoListOfficePhone CoListOfficePhoneExt CoListOfficeURL CommunityFeatures ConstructionMaterials Cooling CoolingYN Country CoveredSpaces Fencing FireplaceFeatures FireplaceFuel FireplacesTotal Flooring FrontageLength FrontageType GarageSpaces GarageYN GreenBuildingCertification GreenCertificationRating Heating HeatingFuel Latitude Lease LeaseFrequency LeaseTerm Levels ListAgentCellPhone ListAgentDesignation ListAgentDirectPhone ListAgentEmail ListAgentFax ListAgentFullName ListAgentKey ListAgentOfficePhone ListAgentOfficePhoneExt ListAgentPager ListAgentURL ListAOR ListingContractDate ListingId ListingKey ListOfficeFax ListOfficeKey ListOfficeName ListOfficePhone ListOfficePhoneExt ListOfficeURL ListPrice Longitude LotFeatures LotSizeArea LotSizeUnits ModificationTimestamp MoreInformationLink NumberOfUnitsTotal OpenParkingSpaces OpenParkingYN OriginatingSystemKey OriginatingSystemName OwnershipType ParkingTotal PhotosChangeTimestamp PhotosCount PoolFeatures PoolYN PostalCode PropertyType PublicRemarks Roof RoomDimensions1 RoomDimensions10 RoomDimensions11 RoomDimensions12 RoomDimensions13 RoomDimensions14 RoomDimensions15 RoomDimensions16 RoomDimensions17 RoomDimensions18 RoomDimensions19 RoomDimensions2 RoomDimensions20 RoomDimensions3 RoomDimensions4 RoomDimensions5 RoomDimensions6 RoomDimensions7 RoomDimensions8 RoomDimensions9 RoomLength1 RoomLength10 RoomLength11 RoomLength12 RoomLength13 RoomLength14 RoomLength15 RoomLength16 RoomLength17 RoomLength18 RoomLength19 RoomLength2 RoomLength20 RoomLength3 RoomLength4 RoomLength5 RoomLength6 RoomLength7 RoomLength8 RoomLength9 RoomLengthWidthUnits1 RoomLengthWidthUnits10 RoomLengthWidthUnits11 RoomLengthWidthUnits12 RoomLengthWidthUnits13 RoomLengthWidthUnits14 RoomLengthWidthUnits15 RoomLengthWidthUnits16 RoomLengthWidthUnits17 RoomLengthWidthUnits18 RoomLengthWidthUnits19 RoomLengthWidthUnits2 RoomLengthWidthUnits20 RoomLengthWidthUnits3 RoomLengthWidthUnits4 RoomLengthWidthUnits5 RoomLengthWidthUnits6 RoomLengthWidthUnits7 RoomLengthWidthUnits8 RoomLengthWidthUnits9 RoomLevel1 RoomLevel10 RoomLevel11 RoomLevel12 RoomLevel13 RoomLevel14 RoomLevel15 RoomLevel16 RoomLevel17 RoomLevel18 RoomLevel19 RoomLevel2 RoomLevel20 RoomLevel3 RoomLevel4 RoomLevel5 RoomLevel6 RoomLevel7 RoomLevel8 RoomLevel9 RoomType1 RoomType10 RoomType11 RoomType12 RoomType13 RoomType14 RoomType15 RoomType16 RoomType17 RoomType18 RoomType19 RoomType2 RoomType20 RoomType3 RoomType4 RoomType5 RoomType6 RoomType7 RoomType8 RoomType9 RoomWidth1 RoomWidth10 RoomWidth11 RoomWidth12 RoomWidth13 RoomWidth14 RoomWidth15 RoomWidth16 RoomWidth17 RoomWidth18 RoomWidth19 RoomWidth2 RoomWidth20 RoomWidth3 RoomWidth4 RoomWidth5 RoomWidth6 RoomWidth7 RoomWidth8 RoomWidth9 Sewer SocialMediaWebsite StateOrProvince Stories StreetAdditionalInfo StreetDirPrefix StreetDirSuffix StreetName StreetNumber StreetSuffix SubdivisionName UnitNumber UnparsedAddress View ViewYN WaterBodyName WaterfrontYN YearBuilt Zoning""".split()

data_set = set(data_columns)
table2_columns =data_set

table_name = "merged_table"
create_table_query = generate_create_table_query(table1_columns, table2_columns, table_name)
print("CREATE TABLE Query:")
print(create_table_query)

# similar_columns = table1_columns.union(table2_columns)
# different_columns_table1 = table1_columns - similar_columns
# different_columns_table2 = table2_columns - similar_columns

# print("Number of similar column names:", len(similar_columns))
# print("Column names that are different in table1:", different_columns_table1)
# print("Column names that are different in table2:", different_columns_table2)
# union_query = generate_union_query(similar_columns)

# print("\nUnion SQL Query for Similar Columns:")
# print(union_query)
# # Generate union SQL query for similar columns
