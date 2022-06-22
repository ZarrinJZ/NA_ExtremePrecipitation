import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

reference_region=gpd.read_file("/Users/jinzhao/Desktop/ATLAS-master/reference-regions/IPCC-WGI-reference-regions-v4_shapefile/IPCC-WGI-reference-regions-v4.shp")
continental_region = gpd.read_file("/Users/jinzhao/Desktop/ATLAS-master/reference-regions/IPCC-WGII-continental-regions_shapefile/IPCC_WGII_continental_regions.shp")
north_america = continental_region[continental_region['Region'] == "North America"]

print("-------------NA-------------------")
region_overlay = gpd.overlay(reference_region, north_america, how='intersection')
print(region_overlay.shape)
print(region_overlay.head())
plt.figure(dpi=300, )
region_overlay.plot(cmap="Blues", edgecolor='grey', figsize=(10, 9))
plt.rc('font', family='Times New Roman')
plt.title(" ", font={'family': 'Times New Roman',
                                 'weight': 'normal',
                                 'size': 20,
                                 })
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
plt.tick_params(which='both', direction='out')
plt.tick_params(which="major", length=7, width=1)
plt.yticks(fontproperties='Times New Roman')
plt.xticks(ticks=[-160, -140, -120, -100, -80, -60], labels=["160 W", "140 W", "120 W", "100 W", "80 W", "60 W"],
           fontproperties='Times New Roman')
plt.grid(color='grey', linewidth=0.5, alpha=0.5, linestyle=(2, (10, 3)))
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d N'))
# plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%d W'))
plt.tick_params(labelsize=24)
plt.tight_layout()
plt.rcParams['axes.unicode_minus'] = True
plt.savefig('StudyArea_NorthAmerica.png', format='png', transparent=True, dpi=300, pad_inches=0.0)
plt.show()

# Export Geopandas into an ESRI shapefile
region_overlay.to_file('/Users/jinzhao/Desktop/NorthAmerica/NorthAmerica.shp',driver="ESRI Shapefile")
