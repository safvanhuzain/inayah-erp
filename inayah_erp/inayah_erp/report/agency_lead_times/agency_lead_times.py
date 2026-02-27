# Copyright (c) 2025, Inayah ERP and contributors
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
			"label": _("Agency"),
			"fieldname": "agency",
			"fieldtype": "Link",
			"options": "Agency",
			"width": 180,
		},
		{
			"label": _("Territory"),
			"fieldname": "territory",
			"fieldtype": "Link",
			"options": "Territory",
			"width": 150,
		},
		{
			"label": _("Is Active"),
			"fieldname": "is_active",
			"fieldtype": "Check",
			"width": 130,
		},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200,
		},
		{
			"label": _("Min Order Qty"),
			"fieldname": "min_order_quantity",
			"fieldtype": "Float",
			"width": 120,
		},
		{
			"label": _("Lead Time"),
			"fieldname": "lead_time_days",
			"fieldtype": "Data",
			"width": 120,
		},
	]


def get_data(filters):
	filters = frappe._dict(filters or {})
	filter_conditions = []
	filter_values = {}

	if filters.get("agency"):
		filter_conditions.append("a.agency = %(agency)s")
		filter_values["agency"] = filters.agency
	if filters.get("item_code"):
		filter_conditions.append("ai.item_code = %(item_code)s")
		filter_values["item_code"] = filters.item_code

	where_clause = " AND " + " AND ".join(filter_conditions) if filter_conditions else ""

	query = f"""
		SELECT
			a.agency,
			a.territory,
			a.is_active,
			ai.item_code,
			ai.min_order_quantity,
			ai.lead_time_days
		FROM `tabAgency` a
		INNER JOIN `tabAgency Item` ai ON ai.parent = a.name
		WHERE a.docstatus < 2
		{where_clause}
		ORDER BY a.agency, ai.item_code
	"""

	rows = frappe.db.sql(query, filter_values, as_dict=True)

	# Build tree: parent row (agency) with indent 0, then child rows (items) with indent 1
	data = []
	current_agency = None

	for row in rows:
		if row.agency != current_agency:
			# Parent row: Agency with Territory and Is Active
			data.append({
				"indent": 0,
				"agency": row.agency,
				"territory": row.territory,
				"is_active": 1 if row.is_active else 0,
				"item_code": None,
				"min_order_quantity": None,
				"lead_time_days": None,
			})
			current_agency = row.agency

		# Child row: Item breakdown (agency, territory, is_active left blank)
		data.append({
			"indent": 1,
			"agency": None,
			"territory": None,
			"is_active": None,
			"item_code": row.item_code,
			"min_order_quantity": row.min_order_quantity,
			"lead_time_days": row.lead_time_days,
		})

	return data
