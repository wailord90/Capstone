# import things
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')

# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Or, more likely, load items from your database with something like
items = ItemModel.query.all()

# Populate the table
table = ItemTable(items)

# Print the html
print(table.__html__())
# or just {{ table }} from within a Jinja template