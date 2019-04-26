import pandas
import folium
import geopy
import math 
from tqdm import tqdm

DATADIR = "./data/"

# read csv files containing largest cities populations
austria_cities_and_population  = pandas.read_csv(DATADIR + "AustriaLargestCitiesAndPopulation.csv")
croatia_cities_and_population  = pandas.read_csv(DATADIR + "CroatiaLargestCitiesAndPopulation.csv")
hungary_cities_and_population  = pandas.read_csv(DATADIR + "HungaryLargestCitiesAndPopulation.csv")
romania_cities_and_population  = pandas.read_csv(DATADIR + "RomaniaLargestCitiesAndPopulation.csv")
slovakia_cities_and_population = pandas.read_csv(DATADIR + "SlovakiaLargestCitiesAndPopulation.csv")
slovenia_cities_and_population = pandas.read_csv(DATADIR + "SloveniaLargestCitiesAndPopulation.csv")
cities_and_population = pandas.DataFrame(columns=["City", "Population"])
cities_and_population = cities_and_population.append(other=austria_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=croatia_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=hungary_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=romania_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=slovenia_cities_and_population, ignore_index=True)
cities_and_population = cities_and_population.append(other=slovakia_cities_and_population, ignore_index=True)

# create list of locations by geomapping
print("Geocoding...")
locations = []
arcGIS = geopy.ArcGIS()
with tqdm(total=len(cities_and_population)) as pbar:
    for _, city_row in cities_and_population.iterrows():
        location = arcGIS.geocode(city_row["City"])
        locations.append((location.latitude, location.longitude))
        pbar.update(1)

# create folium map, center on Budapest
map = folium.Map(
    location=[47.4979, 19.0402],
    tiles="Mapbox Bright",
    zoom_start=3)

fg = folium.FeatureGroup(name="Population of Largest Cities in Hungary and the Surrounding Countries")

for city_index, city_row in cities_and_population.iterrows():
    folium.Circle(
        location=locations[city_index],
        radius=int(math.sqrt( int(city_row["Population"])*200 )),
        color='crimson',
        popup="{} ({})".format(city_row["City"], city_row["Population"]),
        tooltip="{} ({})".format(city_row["City"], city_row["Population"]),
        fill=True,
        fill_color='crimson').add_to(fg)


fg.add_to(map)

# render the map
map.save("HungaryAndSurroundingCountruesLargestCitiesPopulations.html")
