# Copyright (c) 2026, Inayah ERP and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Manufacturer"),
			"fieldname": "manufacturer",
			"fieldtype": "Link",
			"options": "Manufacturer",
			"width": 150,
		},
		{
			"label": _("Full Name"),
			"fieldname": "full_name",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 180,
		},
		{
			"label": _("Part Number"),
			"fieldname": "part_number",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("GTIN"),
			"fieldname": "gtin",
			"fieldtype": "Data",
			"width": 120,
		},
	]


def get_data(filters):
	filters = frappe._dict(filters or {})
	filter_conditions = []
	filter_values = {}

	if filters.get("manufacturer"):
		filter_conditions.append("mi.manufacturer = %(manufacturer)s")
		filter_values["manufacturer"] = filters.manufacturer
	if filters.get("item_code"):
		filter_conditions.append("mi.item_code = %(item_code)s")
		filter_values["item_code"] = filters.item_code

	where_clause = " AND " + " AND ".join(filter_conditions) if filter_conditions else ""

	query = f"""
		SELECT
			m.short_name AS manufacturer,
			m.full_name,
			mi.item_code,
			mi.part_number,
			mi.gtin
		FROM `tabManufacturer Item` mi
		INNER JOIN `tabManufacturer` m ON m.name = mi.manufacturer
		WHERE 1=1
		{where_clause}
		ORDER BY m.short_name, mi.item_code
	"""

	rows = frappe.db.sql(query, filter_values, as_dict=True)

	# Build tree: parent row (manufacturer) with indent 0, then child rows (items) with indent 1
	data = []
	current_manufacturer = None

	for row in rows:
		if row.manufacturer != current_manufacturer:
			# Parent row: Manufacturer with Full Name
			data.append({
				"indent": 0,
				"manufacturer": row.manufacturer,
				"full_name": row.full_name,
				"item_code": None,
				"part_number": None,
				"gtin": None,
			})
			current_manufacturer = row.manufacturer

		# Child row: Item breakdown (manufacturer, full_name left blank)
		data.append({
			"indent": 1,
			"manufacturer": None,
			"full_name": None,
			"item_code": row.item_code,
			"part_number": row.part_number,
			"gtin": row.gtin,
		})

	return data
