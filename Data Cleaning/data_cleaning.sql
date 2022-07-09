Select *
From Nashville_Housing_Data_csv

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, COALESCE(a.PropertyAddress, b.PropertyAddress)
From Nashville_Housing_Data_csv a
JOIN Nashville_Housing_Data_csv b
	on a.ParcelID = b.ParcelID
	AND a.[UniqueID] <> b.[UniqueID]
Where a.PropertyAddress is null

-- create 'address_query_csv' table from previous query


Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, COALESCE(a.PropertyAddress, b.PropertyAddress)
From Nashville_Housing_Data_csv a
JOIN Nashville_Housing_Data_csv b
	on a.ParcelID = b.ParcelID
	AND a.[UniqueID] <> b.[UniqueID]
Where a.PropertyAddress is null

-- fill in missing addresses with addresses with matching ParcelID
Update Nashville_Housing_Data_csv
SET PropertyAddress = (Select b.PropertyAddress
From Nashville_Housing_Data_csv a
JOIN Nashville_Housing_Data_csv b
	on a.ParcelID = b.ParcelID
	AND a.[UniqueID] <> b.[UniqueID]
	Where a.PropertyAddress is null)
Where PropertyAddress is null;

-- format PropertyAddress - splits into Address and City - using substring
select SUBSTRING(PropertyAddress, 1, CharIndex(',', PropertyAddress) -1) as Address
, SUBSTRING(PropertyAddress, CharIndex(',', PropertyAddress) + 2, LENGTH(PropertyAddress)) as City
from Nashville_Housing_Data_csv

-- alter the table with the new columns
ALTER TABLE Nashville_Housing_Data_csv
Add PropertySplitAddress Nvarchar(255);

Update Nashville_Housing_Data_csv
SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CharIndex(',', PropertyAddress) -1 )


ALTER TABLE Nashville_Housing_Data_csv
Add PropertySplitCity Nvarchar(255);

Update Nashville_Housing_Data_csv
SET PropertySplitCity = SUBSTRING(PropertyAddress, CharIndex(',', PropertyAddress) + 1 , LENGTH(PropertyAddress))

-- format OwnerAddress- splits into Address | City | State - using substring

ALTER TABLE Nashville_Housing_Data_csv
Add OwnerSplitAddress Nvarchar(255);

Update Nashville_Housing_Data_csv
Set OwnerSplitAddress = SUBSTRING(OwnerAddress, 1, CharIndex(',', OwnerAddress) -1 );

ALTER TABLE Nashville_Housing_Data_csv
Add OwnerSplitCity Nvarchar(255);

Update Nashville_Housing_Data_csv
Set OwnerSplitCity = SUBSTRING(OwnerAddress, CharIndex(',', OwnerAddress) +1 , LENGTH(OwnerAddress));

ALTER TABLE Nashville_Housing_Data_csv
Add OwnerSplitState Nvarchar(255);

Update Nashville_Housing_Data_csv
Set OwnerSplitState = SUBSTRING(OwnerSplitCity, CharIndex(',', OwnerSplitCity) +2 , LENGTH(OwnerSplitCity));

Update Nashville_Housing_Data_csv
Set OwnerSplitCity = SUBSTRING(OwnerSplitCity, 1, CharIndex(',', OwnerSplitCity) -1)