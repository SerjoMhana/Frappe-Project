frappe.query_reports["report for items and there Warehouse"] = {
    "filters": [
        {
            "fieldname": "item_code",
            "label": __("Item Code"),
            "fieldtype": "Data",
            "options": "Item",
            "width": 150
        },
        {
            "fieldname": "item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 150
        },
        {
            "fieldname": "brand",
            "label": __("Brand"),
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150
        },
        {
            "fieldname": "stock_uom",
            "label": __("Stock UOM"),
            "fieldtype": "Link",
            "options": "UOM",
            "width": 100
        }
    ]
};
