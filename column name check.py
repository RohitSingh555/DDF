
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

table2_columns = {
    'ID', 'ThumbnailURL', 'FireplaceType', 'Designations', 'SizeFrontage', 'AgentDetails', 'MaintenanceFee', 'Price',
    'MunicipalId', 'RoadType', 'BedroomsAboveGround', 'Websites', 'SizeIrregular', 'BasementDevelopment', 'SizeTotal',
    'Board', 'ListingContractDate', 'PublicRemarks', 'StreetSuffix', 'OwnershipType', 'FlooringType', 'StartDateTime',
    'LargePhotoURL', 'Franchise', 'Country', 'HalfBathTotal', 'PoolFeatures', 'SurfaceWater', 'OrganizationType',
    'Building', 'RoofStyle', 'TotalFinishedArea', 'BasementFeatures', 'Structure', 'CommunityFeatures', 'ListingID',
    'Address', 'TransactionType', 'VideoLink', 'OpenHouse', 'Spaces', 'PoolType', 'StreetName', 'LandscapeFeatures',
    'Photo', 'Plan', 'Name', 'Amenities', 'BrochureLink', 'LogoLastUpdated', 'Logo', 'Land', 'Acreage', 'PhotoLink',
    'AlternateURL', 'Width', 'FenceTotal', 'ZoningDescription', 'SizeInterior', 'Website', 'Length', 'StoriesTotal',
    'Parking', 'MaintenanceFeePaymentUnit', 'Sewer', 'Province', 'RoofMaterial', 'PropertyDetails', 'StreetAddress',
    'UtilityWater', 'Position', 'LastUpdated', 'BusinessSubType', 'CoolingType', 'ConstructedDate', 'Longitude',
    'FoundationType', 'AccessType', 'FireplaceTotal', 'PhotoURL', 'Lease', 'FireProtection', 'FireplacePresent',
    'UnitNumber', 'CommunicationType', 'PhotoLastUpdated', 'ConstructionStyleAttachment', 'StreetNumber', 'Franchisor',
    'Business', 'LeasePerTime', 'Appliances', 'BasementType', 'FireplaceFuel', 'ParkingSpaceTotal', 'Type', 'FenceType',
    'MaintenanceFeeType', 'UtilitiesAvailable', 'City', 'Office', 'Comments', 'ZoningType', 'StreetDirectionSuffix',
    'HeatingType', 'ExteriorFinish', 'Phones', 'StreetDirectionPrefix', 'SizeTotalText', 'Event', 'SocialMediaWebsite',
    'SequenceId', 'Room', 'StorageType', 'PropertyType', 'Neighbourhood', 'BusinessType', 'Level', 'Addressline2',
    'LeasePerUnit', 'AmmenitiesNearBy', 'CommunityName', 'Description', 'Features', 'ViewType', 'Latitude',
    'AddressLine1', 'ConstructionMaterial', 'BathroomTotal', 'Rooms', 'PostalCode', 'Fixture', 'Subdivision', 'Phone',
    'Utility', 'Age', 'WaterFrontType', 'Designation', 'BedroomsTotal', 'ManagementCompany', 'EndDateTime',
    'PropertyPhoto', 'ArchitecturalStyle', 'MoreInformationLink', 'Dimension', 'ParkingSpaces', 'HeatingFuel'
}


similar_columns = table1_columns.intersection(table2_columns)
different_columns_table1 = table1_columns - similar_columns
different_columns_table2 = table2_columns - similar_columns

print("Number of similar column names:", len(similar_columns))
print("Column names that are different in table1:", different_columns_table1)
print("Column names that are different in table2:", different_columns_table2)