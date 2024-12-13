"""
main program
"""
import warehouse
import item
import warehouseitem


def main():
    """
    CONTOH OPERASI
    """
    # Create the tables
    warehouse.initialize_warehouse_tables()

    # Add some warehouses
    warehouse.add_warehouse("Warehouse M", "This is warehouse A", 1000)
    warehouse.add_warehouse("Warehouse N", "This is warehouse B", 1500)
    warehouse.add_warehouse("Warehouse O", "This is warehouse C", 2000)

    # Initialize item table
    item.initialize_item_table()

    # Add some items
    item.add_item("Item A", "This is item A", 10)
    item.add_item("Item B", "This is item B", 20)
    item.add_item("Item C", "This is item C", 30)

    # Create warehouse items
    warehouseitem.initialize_warehouseitem_table()

    # Add items to warehouse
    warehouseitem.add_item_to_warehouse(1, 1, 5)
    warehouseitem.add_item_to_warehouse(1, 2, 10)
    warehouseitem.add_item_to_warehouse(2, 2, 10)
    warehouseitem.add_item_to_warehouse(2, 3, 20)


if __name__ == "__main__":
    main()
