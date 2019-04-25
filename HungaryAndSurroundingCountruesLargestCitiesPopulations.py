import pandas
import folium
import geopy

# read csv file containing Austria's largest cities populations
austria_cities_and_population = pandas.read_csv("AustriaLargestCitiesAndPopulation.csv")
print(austria_cities_and_population)

# read csv file containing Austria's largest cities populations
croatia_cities_and_population = pandas.read_csv("CroatiaLargestCitiesAndPopulation.csv")
print(croatia_cities_and_population)

# read csv file containing Hungary's largest cities populations
hungary_cities_and_population = pandas.read_csv("HungaryLargestCitiesAndPopulation.csv")
print(hungary_cities_and_population)

# read csv file containing Romania's largest cities populations
romania_cities_and_population = pandas.read_csv("RomaniaLargestCitiesAndPopulation.csv")
print(romania_cities_and_population)

# read csv file containing Romania's largest cities populations
slovakia_cities_and_population = pandas.read_csv("SlovakiaLargestCitiesAndPopulation.csv")
print(slovakia_cities_and_population)

# read csv file containing Romania's largest cities populations
slovenia_cities_and_population = pandas.read_csv("SloveniaLargestCitiesAndPopulation.csv")
print(slovenia_cities_and_population)

# create list of locations by geomapping
locations = []
cities_and_population = pandas.DataFrame(columns=["City", "Population"])
arcGIS = geopy.ArcGIS()

cities_and_population = cities_and_population.append(other=austria_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=croatia_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=hungary_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=romania_cities_and_population,  ignore_index=True)
cities_and_population = cities_and_population.append(other=slovenia_cities_and_population, ignore_index=True)
cities_and_population = cities_and_population.append(other=slovakia_cities_and_population, ignore_index=True)
print(cities_and_population)

for _, city_row in cities_and_population.iterrows():
    location = arcGIS.geocode(city_row["City"])
    locations.append((location.latitude, location.longitude))

# create folium map, center on Budapest
map = folium.Map(
    location=[47.4979, 19.0402],
    tiles="Mapbox Bright",
    zoom_start=3)

fg = folium.FeatureGroup(name="My Map")

for city_index, city_row in cities_and_population.iterrows():
    folium.Circle(
        location=locations[city_index],
        radius=int(city_row["Population"])//30,
        color='crimson',
        popup="{} ({})".format(city_row["City"], city_row["Population"]),
        tooltip="{} ({})".format(city_row["City"], city_row["Population"]),
        fill=True,
        fill_color='crimson').add_to(fg)
    print("{} added".format(city_index))

fg.add_to(map)

# render the map
map.save("HungaryAndSurroundingCountruesLargestCitiesPopulations.html")
