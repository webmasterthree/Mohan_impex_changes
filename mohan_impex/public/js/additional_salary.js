frappe.ui.form.on('Additional Salary', {
    employee: function(frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: "mohan_impex.over_short_time.get_employee_checkins",  // Ensure correct API path
                args: {
                    employee: frm.doc.employee  // Pass only the employee ID
                },
                callback: function(response) {
                    if (response.message && response.message.status === "success" && Array.isArray(response.message.data)) {
                        let employee_data = response.message.data.find(emp => emp.employee === frm.doc.employee);
                        
                        if (employee_data) {
                            frm.set_value('custom_overtime_hours', employee_data.overtime_hours || 0);
                            frm.set_value('custom_shortfall_hours', employee_data.shortfall_hours || 0);
                        } else {
                            frappe.msgprint(__('No check-in data found for the selected employee.'));
                            frm.set_value('custom_overtime_hours', 0);
                            frm.set_value('custom_shortfall_hours', 0);
                        }
                    } else {
                        frappe.msgprint(__('Error fetching check-in data. Please try again.'));
                        frm.set_value('custom_overtime_hours', 0);
                        frm.set_value('custom_shortfall_hours', 0);
                    }
                },
                error: function(err) {
                    frappe.msgprint(__('API request failed. Please check the server logs.'));
                    console.error("Error fetching employee check-in data:", err);
                    frm.set_value('custom_overtime_hours', 0);
                    frm.set_value('custom_shortfall_hours', 0);
                }
            });
        } else {
            frappe.msgprint(__('Please select an employee.'));
        }
    }
});


frappe.ui.form.on('Additional Salary', {
    setup: function (frm) {
        toggle_salary_component_fields(frm);
    },
    salary_component: function (frm) {
        toggle_salary_component_fields(frm);
    }
});

function toggle_salary_component_fields(frm) {
    const component = frm.doc.salary_component?.toLowerCase() || "";

    frm.toggle_display('custom_overtime_hours', component === "over time");
    frm.toggle_display('custom_shortfall_hours', component === "short hour");
}
