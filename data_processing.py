import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

# Print first 5 cities only
for city in cities[:5]:
    print(city)

# Print the average temperature of all the cities
print("The average temperature of all the cities:")
temps = []
for city in cities:
    temps.append(float(city['temperature']))
print(sum(temps)/len(temps))
print()

# Print the average temperature of all the cities
print("The average temperature of all the cities:")
temps = [float(city['temperature']) for city in cities]
print(sum(temps)/len(temps))
print()

# Print all cities in Germany
print("All cities in Germany:")
germany_cities = []
for city in cities:
    if city["country"] == "Germany":
        germany_cities.append(city["city"])
print(', '.join(germany_cities))
print()


# Print all cities in Spain with a temperature above 12°C
print("All cities in Spain with a temperature above 12°C:")
spain_cities = []
for city in cities:
    if city["country"] == "Spain" and float(city["temperature"]) > 12:
        spain_cities.append(city["city"])
print(', '.join(spain_cities))
print()

# Count the number of unique countries
print("Number of unique countries:")
count = 0
counted = []
for city in cities:
    if city["country"] not in counted:
        count += 1
        counted.append(city["country"])
print(count)
print()


# Print the average temperature for all the cities in Germany
print("Average temperature for all the cities in Germany:")
germany_temp = []
for city in cities:
    if city["country"] == "Germany":
        germany_temp.append(float(city["temperature"]))
avg_germany_temp = sum(germany_temp) / len(germany_temp)
print(avg_germany_temp)
print()


# Print the max temperature for all the cities in Italy
print("Max temperature for all the cities in Italy:")
italy_temp = []
for city in cities:
    if city["country"] == "Italy":
        italy_temp.append(float(city["temperature"]))
print(max(italy_temp))