// Copyright (c) 2026, safvanhuzain and contributors
// For license information, please see license.txt

frappe.query_reports["Agency Lead Times"] = {
	"filters": [
		{
			fieldname: "agency",
			label: __("Agency"),
			fieldtype: "Link",
			options: "Agency",
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
		},
	],
	// Tree view: start collapsed so only agency (parent) rows are visible; expand to see items
	initial_depth: 0,
};
