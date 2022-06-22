import geopandas as gpd
import matplotlib.pyplot as plt


#Importing an ESRI Shapefile and plotting it using GeoPandas
reference_region=gpd.read_file("/Users/jinzhao/Desktop/ATLAS-master/reference-regions/IPCC-WGI-reference-regions-v4_shapefile/IPCC-WGI-reference-regions-v4.shp")
print(reference_region.shape)
print(reference_region.head())
# where jet comes from----matplotlib library
reference_region.plot(cmap='jet',edgecolor='black',column='Continent')
plt.show()


continental_region = gpd.read_file("/Users/jinzhao/Desktop/ATLAS-master/reference-regions/IPCC-WGII-continental-regions_shapefile/IPCC_WGII_continental_regions.shp")
print(continental_region.shape)
print(continental_region.head())
continental_region.plot(cmap='jet',column='Region')
plt.show()

north_america = continental_region[continental_region['Region'] == "North America"]
#north_america.plot(cmap='jet',edgecolor='black')

# # plot the fugures side by side
# #fig, (ax1,ax2) = plt.subplots(ncols=2,figsize=(10,8))
# fig, (ax1,ax2) = plt.subplots(nrows=2)
# reference_region.plot(ax = ax1,cmap='jet',edgecolor='black',column='Continent')
# continental_region.plot(ax=ax2,cmap='jet',column='Region')
# plt.show()
#
#plot multiple layers
# fig, ax = plt.subplots(figsize=(10,8))
# reference_region.plot(ax = ax,cmap='jet',edgecolor='red',column='Continent')
# north_america.plot(ax=ax,color='none',edgecolor="black")
# plt.show()

# #reprojecting Geopandas GeoDataFrames (change coordinate reference system to another) units are in meters
# north_america=north_america.to_crs(epsg=32629)
# north_america.plot()
# plt.show(figsize=(10,8))

#Intersectering layers
print("-------------NA-------------------")
region_overlay=gpd.overlay(reference_region,north_america,how='intersection')
print(region_overlay.shape)
print(region_overlay.head())
# region_overlay.plot(color='PuBu',edgecolor="black")
# region_overlay.plot(cmap='RdBu_r', edgecolor='black')
fig,ax = plt.subplots(figsize=(15,15))
plt.show()

# GIC = region_overlay[region_overlay['Acronym'] == "GIC"]
# GIC.plot(cmap='hsv_r', edgecolor='black')
# plt.show()

#north_america.plot(cmap='jet',edgecolor='black')

#Calculating the areas of NA+ICPP area
# region_overlay['area'] = region_overlay.area

#Export Geopandas into an ESRI shapefile
# region_overlay.to_file('/Users/jinzhao/Desktop/NorthAmerica/NorthAmerica.shp',driver="ESRI Shapefile")