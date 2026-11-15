import csv, os
from pathlib import Path

class DataLoader:
    """Handles loading CSV data files."""
    
    def __init__(self, base_path=None):
        """Initialize the DataLoader with a base path for data files.
        """
        if base_path is None:
            self.base_path = Path(__file__).parent.resolve()
        else:
            self.base_path = Path(base_path)
    
    def load_csv(self, filename):
        """Load a CSV file and return its contents as a list of dictionaries.
        """
        filepath = self.base_path / filename
        data = []
        
        with filepath.open() as f:
            rows = csv.DictReader(f)
            for row in rows:
                data.append(dict(row))
        return data
    
class Table:
    def __init__(self, name ,dict_list):
        self._name = name
        self.table = dict_list

    def filter(self, condition):
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

        filtered = []
        for dict in self.table:
            if condition(dict):
                filtered.append(dict)
        return Table("filtered table", filtered)


    def aggregate(self, aggregation_function, aggregation_key):
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
        value_list = []
        for dict in self.table:
            try:
                value_list.append(float(dict[aggregation_key]))
            except ValueError:
                value_list.append(dict[aggregation_key])
        return aggregation_function(value_list)


loader = DataLoader()
cities = loader.load_csv('Cities.csv')
my_table1 = Table('cities', cities)

# Print the average temperature of all the cities
my_value = my_table1.aggregate(lambda x: sum(x)/len(x), 'temperature')
print("Average temperature of all the cities:")
print(my_value)
print()

# Print all cities in Germany
my_cities = my_table1.filter(lambda x: x['country'] == 'Germany')
cities_list = [[city['city'], city['country']] for city in my_cities.table]
print("All the cities in Germany:")
for city in cities_list:
    print(city)
print()

# Print all cities in Spain with a temperature above 12°C
my_cities = my_table1.filter(lambda x: x['country'] == 'Spain' and float(x['temperature']) > 12.0)
cities_list = [[city['city'], city['country'], city['temperature']] for city in my_cities.table]
print("All the cities in Spain with temperature above 12°C:")
for city in cities_list:
    print(city)
print()

# Count the number of unique countries
my_countries = my_table1.aggregate(lambda x: len(set(x)), 'country')
print("The number of unique countries is:")
print(my_countries)
print()

# Print the average temperature for all the cities in Germany
my_value = my_table1.filter(lambda x: x['country'] == 'Germany').aggregate(lambda x: sum(x)/len(x), 'temperature')
print("The average temperature of all the cities in Germany:")
print(my_value)
print()

# Print the max temperature for all the cities in Italy
my_value = my_table1.filter(lambda x: x['country'] == 'Italy').aggregate(lambda x: max(x), 'temperature')
print("The max temperature of all the cities in Italy:")
print(my_value)
print()