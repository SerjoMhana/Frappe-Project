import frappe

def execute(filters=None):
    columns, data = [], []
    
    # Adding the columns, including UOM
    columns = [
        {"fieldname": "item_code", "label": "Item Code", "fieldtype": "Data", "width": 150},
        {"fieldname": "item_name", "label": "Item Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "description", "label": "Description", "fieldtype": "Data", "width": 250},
        {"fieldname": "item_group", "label": "Item Group", "fieldtype": "Data", "width": 150},
        {"fieldname": "brand", "label": "Brand", "fieldtype": "Data", "width": 150},
        {"fieldname": "warehouse", "label": "Warehouse", "fieldtype": "Data", "width": 150},
        {"fieldname": "actual_qty", "label": "Actual Qty", "fieldtype": "Float", "width": 100},
        {"fieldname": "planned_qty", "label": "Planned Qty", "fieldtype": "Float", "width": 100},
        {"fieldname": "requested_qty", "label": "Requested Qty", "fieldtype": "Float", "width": 100},
        {"fieldname": "ordered_qty", "label": "Ordered Qty", "fieldtype": "Float", "width": 100},
        {"fieldname": "reserved_qty", "label": "Reserved Qty", "fieldtype": "Float", "width": 100},
        {"fieldname": "stock_uom", "label": "Stock UOM", "fieldtype": "Data", "width": 100},  # UOM column
    ]

    # Query to fetch the required data
    query = """
        SELECT
            i.item_code, i.item_name, i.description, i.item_group, i.brand, i.stock_uom,  -- Fetching UOM
            b.warehouse, b.actual_qty, b.planned_qty, b.reserved_qty, b.ordered_qty, b.reserved_qty
        FROM
            `tabItem` i
        LEFT JOIN
            `tabBin` b ON i.item_code = b.item_code
        WHERE
            i.disabled = 0
    """

    # Adding filters dynamically based on user input
    if filters.get("item_code"):
        query += " AND i.item_code = %(item_code)s"
    if filters.get("item_group"):
        query += " AND i.item_group = %(item_group)s"
    if filters.get("brand"):
        query += " AND i.brand = %(brand)s"
    if filters.get("warehouse"):
        query += " AND b.warehouse = %(warehouse)s"
    if filters.get("stock_uom"):
        query += " AND i.stock_uom = %(stock_uom)s"

    # Executing the query with the provided filters
    data = frappe.db.sql(query, filters, as_dict=True)

    return columns, data
