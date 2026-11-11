import csv, os

def filter_items(condition, dict_list):
    """
    Return a new list containing only the dictionaries that satisfy
    the given condition function.

    Args:
        condition: A function that takes a dictionary and returns True or False.
        dict_list: A list of dictionaries.

    Returns:
        A list of dictionaries for which condition(item) is True.

    Examples:
        >>> students = [
        ...     {"name": "Alice", "score": 90},
        ...     {"name": "Bob", "score": 70},
        ...     {"name": "Charlie", "score": 85}
        ... ]
        >>> filter_items(lambda s: s["score"] >= 85, students)
        [{'name': 'Alice', 'score': 90}, {'name': 'Charlie', 'score': 85}]

        >>> filter_items(lambda s: s["name"].startswith("A"), students)
        [{'name': 'Alice', 'score': 90}]

        >>> filter_items(lambda s: s["score"] > 100, students)
        []
    """
    # YOUR CODE HERE
    filtered = []
    for dict in dict_list:
        if condition(dict):
            filtered.append(dict)
    return filtered


def aggregate(aggregation_key, aggregation_function, dict_list):
    """
    Aggregate values associated with aggregation_key using the
    provided aggregation function.

    Args:
        aggregation_key: The dictionary key whose values should be aggregated.
        aggregation_function: A function such as sum, max, min, etc.
        dict_list: A list of dictionaries.

    Returns:
        The aggregated result.

    Examples:
        >>> students = [
        ...     {"name": "Alice", "score": 90},
        ...     {"name": "Bob", "score": 70},
        ...     {"name": "Charlie", "score": 85}
        ... ]

        >>> aggregate("score", sum, students)
        245

        >>> aggregate("score", max, students)
        90

        >>> aggregate("score", min, students)
        70

        >>> aggregate(
        ...     "score",
        ...     lambda scores: sum(scores) / len(scores),
        ...     students
        ... )
        81.66666666666667
    """
    # YOUR CODE HERE
    value_list = []
    for dict in dict_list:
        value_list.append(float(dict[aggregation_key]))
    return aggregation_function(value_list)


def show_column_list(dict_list, key):
    showed = []
    for dict in dict_list:
        showed.append(dict[key])
    print(", ".join(showed))


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
average_temp = aggregate("temperature", sum, cities) / len(cities)
print(average_temp)
print()

# Print all cities in Germany
print("All cities in Germany:")
germany_cities = filter_items(lambda c: c["country"] == "Germany", cities)
show_column_list(germany_cities, "city")
print()
# germany_city_names = []
# for city in germany_cities:
#     germany_city_names.append(city["city"])
# print(", ".join(germany_city_names))

# Print all cities in Spain with a temperature above 12°C
print("All cities in Spain with a temperature above 12°C:")
spain_cities = filter_items(lambda c: c["country"] == "Spain" 
                            and float(c["temperature"]) > 12, cities)
show_column_list(spain_cities, "city")
print()

# Count the number of unique countries
print("Number of unique countries:")
counted = []
for city in cities:
    if city["country"] not in counted:
        counted.append(city["country"])
print(len(counted))
print()

# Print the average temperature for all the cities in Germany
print("Average temperature for all the cities in Germany:")
print(aggregate("temperature", sum, germany_cities) / len(germany_cities))
print()

# Print the max temperature for all the cities in Italy
print("Max temperature for all the cities in Italy:")
italy_cities = filter_items(lambda c: c["country"] == "Italy", cities)
max_italy_temp = aggregate("temperature", max, italy_cities)
print(max_italy_temp)
print()