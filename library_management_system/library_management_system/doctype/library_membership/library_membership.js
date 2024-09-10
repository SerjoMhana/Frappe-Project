frappe.ui.form.on('Library Membership', {
    refresh: function(frm) {
        frm.set_query('library_member', function() {
            return {
                filters: {
                    is_membership_valid: 0
                }
            };
        });
    }
});
frappe.ui.form.on('Library Membership', {
    membership_type: function(frm) {
        console.log("Membership type changed!");

        const DURATIONS = {
            "bronze": 30,
            "Selver Member": 60,
            "Gold Member": 90
        };

        let membership_type = frm.doc.membership_type || null;
        console.log("Selected Membership Type: ", membership_type);

        if (membership_type && DURATIONS[membership_type]) {
            let days = DURATIONS[membership_type];
            let today = frappe.datetime.get_today();
            let to_date = frappe.datetime.add_days(today, days);

            console.log("From Date: ", today);
            console.log("To Date: ", to_date);

            frm.set_value('from_date', today);
            frm.set_value('to_date', to_date);
        } else {
            console.error("Invalid membership type or membership type is empty:", membership_type);
            frm.set_value('from_date', null);
            frm.set_value('to_date', null);
        }
    }
});




frappe.ui.form.on('Library Membership', {
    onload: function(frm) {
        frm.set_query('membership_type', function() {
            return {
                filters: {
                    'custom_library_member': 1
                }
            };
        });
    }
});
