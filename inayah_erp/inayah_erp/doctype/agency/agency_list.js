frappe.listview_settings['Agency'] = {
    add_fields: ['agency', 'territory', 'is_active'],
    get_indicator: function(doc) {
        console.log(doc);

        if (doc.is_active == 0) {
            return [__('Inactive'), 'red'];
        } else {
            return [__('Active'), 'green'];
        }
    }
};