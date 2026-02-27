import frappe
from frappe import _

def check_if_manufacturer_blocked(doc, method=None):
    if doc.custom_is_blocked:
        frappe.throw(
            _("Cannot add Manufacturer Item because Manufacturer is blocked.")
        )


def validate_unique_manufacturer_item(doc, method=None):
    if not doc.custom_items:
        return

    seen = set()

    for row in doc.custom_items:
        key = (row.manufacturer, row.item_code)

        if key in seen:
            frappe.throw(
                _("Duplicate Item {0} found in row {1}").format(
                    row.item_code,
                    row.idx
                )
            )

        seen.add(key)


def auto_fill_part_number(doc, method=None):
    if not doc.custom_items:
        return

    for row in doc.custom_items:
        if not row.part_number and row.item_code:
            row.part_number = row.item_code
