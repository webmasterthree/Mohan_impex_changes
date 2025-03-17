frappe.ui.form.on('Request for Quotation', {
    setup: function (frm) {
        // Define the roles that should have the field hidden
        let hiddenRoles = [
            "Administrator", 
            "Purchase Executive", 
            "Purchase Manager", 
            "Purchase Master Manager", 
            "Purchase User", 
            "SCM Manager"
        ];

        // Check if the user has any of the roles in the hiddenRoles list
        let shouldHide = frappe.user_roles.some(role => hiddenRoles.includes(role));

        // Hide or show the field based on the role
        frm.set_df_property('message_for_supplier', 'hidden', shouldHide ? 0 : 1);
        frm.set_df_property('email_template','hidden',shouldHide ? 0 : 1);
        frm.set_df_property('send_attached_files','hidden',shouldHide ? 0 : 1);
        frm.set_df_property('send_document_print','hidden',shouldHide ? 0 : 1);

    }
});




