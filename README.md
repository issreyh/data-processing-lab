# Countries Data Processing

This is a data processing using the information of countries includes latitude, longtitude, and temperature

## File Structure

- `Countries.csv`: csv file of each city's data
- `data_processing.py`: Runs data processing using `DataLoader` and `Table`.

## DataLoader Class

Located in `data_processing.py`, the `DataLoader` class includes:

### Attributes
- `self.base_path`: The file's base path.

### Methods
- `load_csv`: Load csv files and return as list of dictionaries.

## Table Class

Located in `data_processing.py`, the `Table` class includes:

### Attributes
- `name` (str): The table's name.
- `table` (list): The list of dictionaries of the data.

### Methods
- `filter(condition)`: Filtered the table by the condition and return as the new table object.
- `aggregate(aggregation_function, aggregation_key)`: Return aggregated values associated with aggregation key.

##  Testing and Running the code

To run the code, execute `data_processing.py`:

```bash
python3 data_processing.py
