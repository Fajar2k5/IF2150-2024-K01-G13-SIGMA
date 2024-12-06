"""
main program
"""
from warehouse import initialize_warehouse_tables, add_warehouse
from warehouse import total_volume_used, print_all_warehouse

if __name__ == "__main__":
    # Create the tables
    initialize_warehouse_tables()

    # Add some warehouses
    add_warehouse("Warehouse A", "This is warehouse A", 1000)
    add_warehouse("Warehouse B", "This is warehouse B", 1500)
    add_warehouse("Warehouse C", "This is warehouse C", 2000)

    # Print all warehouses
    print_all_warehouse()

    # Calculate the total volume used in Warehouse B
    total_volume_used(2)  # Warehouse B
