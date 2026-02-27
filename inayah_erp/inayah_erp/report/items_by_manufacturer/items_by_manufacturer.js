// Copyright (c) 2026, safvanhuzain and contributors
// For license information, please see license.txt

frappe.query_reports["Items by Manufacturer"] = {
	"filters": [
		{
			fieldname: "manufacturer",
			label: __("Manufacturer"),
			fieldtype: "Link",
			options: "Manufacturer",
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
		},
	],
	// Tree view: start collapsed so only manufacturer (parent) rows are visible; expand to see items
	initial_depth: 0,
};
