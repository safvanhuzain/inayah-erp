// Copyright (c) 2026, safvanhuzain and contributors
// For license information, please see license.txt

frappe.ui.form.on('Agency', {
    refresh: function(frm) {

        if (!frm.is_new()) {

            frm.add_custom_button(__('Create Supplier'), function() {

                frappe.call({
                    method: 'frappe.client.insert',
                    args: {
                        doc: {
                            doctype: 'Supplier',
                            supplier_name: frm.doc.agency,
                            supplier_type: 'Company',
                            territory: frm.doc.territory,
                            custom_linked_agency: frm.doc.name
                        }
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('Supplier Created Successfully'));

                            // Redirect to created Supplier
                            frappe.set_route('Form', 'Supplier', r.message.name);
                        }
                    }
                });

            });
        }
    },
    is_active: function(frm) {
        // If trying to deactivate
        validate_agency(frm);
    },
    validate: function(frm) {
        validate_agency(frm);
    }
});

function validate_agency(frm) {
    if (!frm.doc.is_active) {

        // Check if child table has rows
        if (frm.doc.items && frm.doc.items.length > 0) {
            frappe.throw(__('Cannot deactivate Agency while Agency Items exist. Please remove all items first.'));
        }
    }
}