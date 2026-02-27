
import frappe
from frappe import _

@frappe.whitelist()
def get_manufacturer_mappings(item_code):
    if not item_code:
        frappe.throw(_("Item Code is required"))

    mappings = frappe.get_all(
        "Manufacturer Item",
        filters={"item_code": item_code},
        fields=[
            "manufacturer",
            "item_code",
            "part_number",
            "gtin"
        ]
    )

    return mappings