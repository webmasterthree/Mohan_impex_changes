frappe.ui.form.on("Sales Order", {
    setup: function(frm) {
        frm.set_df_property("naming_series", "options", [
            "",
            "SO-DNK-.####.-.FY",
            "SO-KPS-.####.-.FY",
            "SO-BB-.####.-.FY",
            "SO-GWH-.####.-.FY",
            "SO-PAT-.####.-.FY",
            "SO-HYD-.####.-.FY",
            "SO-CHN-.####.-.FY",
            "SO-DEL-.####.-.FY",
            "SO-MUM-.####.-.FY",
            "SO-MFG-.####.-.FY",
            "SO-EXP-.####.-.FY",
            "SO-RET-.####.-.FY",
            "SO-BT-DNK-.####.-.FY",
            "SO-BT-KPS-.####.-.FY",
            "SO-BT-BB-.####.-.FY",
            "SO-BT-GWH-.####.-.FY",
            "SO-BT-PAT-.####.-.FY",
            "SO-BT-HYD-.####.-.FY",
            "SO-BT-CHN-.####.-.FY",
            "SO-BT-DEL-.####.-.FY",
            "SO-BT-MUM-.####.-.FY",
            "SO-BT-MFG-.####.-.FY",
            "SO-ECOM/.####./.FY"
        ].join("\n"));

        frm.set_df_property("naming_series", "reqd", 1);
    },

    onload: function(frm) {
        if (frm.is_new()) {
            frm.set_value("naming_series", "");
        }
    },

    refresh: function(frm) {
        frm.set_df_property("naming_series", "reqd", 1);
    },

    validate: function(frm) {
        if (!frm.doc.naming_series) {
            frappe.throw("Please select Naming Series.");
        }
    }
});