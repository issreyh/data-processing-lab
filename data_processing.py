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

class DB:
    def __init__(self):
        self._db = []

    def insert(self, table):
        if table not in self._db:
            self._db.append(table)

    def search(self, name):
        for table in self._db:
            if table.table_name == name:
                return table


class Table:
    def __init__(self, name ,dict_list):
        self.table_name = name
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
        return Table("countries_filteres", filtered)


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

    def join(self, table_join, joined_key):
        new = []
        for i in range(len(self.table)):
            new_dict = self.table[i].copy()
            key = self.table[i][joined_key]
            for j in range(len(table_join.table)):
                if key == table_join.table[j][joined_key]:
                    new_dict.update(table_join.table[j])
            new.append(new_dict)
        return Table("joined table", new)


    def __str__(self):
        return self.table_name + ':' + str(self.table)

loader = DataLoader()
cities = loader.load_csv('Cities.csv')
table1 = Table('cities', cities)
countries = loader.load_csv('Countries.csv')
table2 = Table('countries', countries)

my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)

my_table1 = my_DB.search('cities')
print("List all cities in Italy:") 
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
print(my_table1_filtered)
print()

print("Average temperature for all cities in Italy:")
print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
print()

my_table2 = my_DB.search('countries')
print("List all non-EU countries:") 
my_table2_filtered = my_table2.filter(lambda x: x['EU'] == 'no')
print(my_table2_filtered)
print()

print("Number of countries that have coastline:")
print(my_table2.filter(lambda x: x['coastline'] == 'yes').aggregate(lambda x: len(x), 'coastline'))
print()

my_table3 = my_table1.join(my_table2, 'country')
print("First 5 entries of the joined table (cities and countries):")
for item in my_table3.table[:5]:
    print(item)
print()

print("Cities whose temperatures are below 5.0 in non-EU countries:")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)
print()

print("The min and max temperatures for cities in EU countries that do not have coastlines")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
print()