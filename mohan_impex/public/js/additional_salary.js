frappe.ui.form.on('Additional Salary', {
    setup: function (frm) {
        toggle_salary_component_fields(frm);
    },

    employee: function(frm) {
        fetch_overtime_hours(frm);
    },

    salary_component: function (frm) {
        toggle_salary_component_fields(frm);
        fetch_overtime_hours(frm);
    },

    custom_start_date: function(frm) {
        fetch_overtime_hours(frm);
    },

    custom_end_date: function(frm) {
        fetch_overtime_hours(frm);
    }
});

function toggle_salary_component_fields(frm) {
    const component = (frm.doc.salary_component || "").toLowerCase();
    const show = component === "over time";

    frm.toggle_display('custom_start_date', show);
    frm.toggle_display('custom_end_date', show);
    frm.toggle_display('custom_overtime_hours', show);

    if (!show) {
        frm.set_value('custom_start_date', null);
        frm.set_value('custom_end_date', null);
        frm.set_value('custom_overtime_hours', 0);
        frm.set_value('amount', 0);
    }
}

function fetch_overtime_hours(frm) {
    const component = (frm.doc.salary_component || "").toLowerCase();
    if (component !== "over time") return;

    const { employee, custom_start_date, custom_end_date } = frm.doc;

    if (!employee || !custom_start_date || !custom_end_date) return;

    const from_date = custom_start_date;
    const to_date = custom_end_date;

    frappe.call({
        method: "mohan_impex.over_short_time.get_overtime_checkins",
        args: { from_date, to_date },
        callback: function(response) {
            const data = response.message || [];

            console.log("Overtime API response:", data);

            const emp_data = data.find(emp => emp.employee.toLowerCase() === employee.toLowerCase());

            frappe.after_ajax(() => {
                if (emp_data) {
                    const hours = emp_data.total_overtime_hours || 0;
                    frm.set_value('custom_overtime_hours', hours);
                    frm.set_value('amount', hours * 50);
                } else {
                    frm.set_value('custom_overtime_hours', 0);
                    frm.set_value('amount', 0);
                    frappe.msgprint(__('No overtime data found for this employee in selected period.'));
                }
                frm.refresh_fields(['custom_overtime_hours', 'amount']);
            });
        },
        error: function(err) {
            console.error("Error calling get_overtime_checkins API:", err);
            frappe.msgprint(__('Failed to fetch overtime hours.'));

            frm.set_value('custom_overtime_hours', 0);
            frm.set_value('amount', 0);
            frm.refresh_fields(['custom_overtime_hours', 'amount']);
        }
    });
}


// frappe.ui.form.on('Additional Salary', {
//     employee: function(frm) {
//         if (frm.doc.employee) {
//             frappe.call({
//                 method: "mohan_impex.over_short_time.get_employee_checkins",  // Ensure correct API path
//                 args: {
//                     employee: frm.doc.employee  // Pass only the employee ID
//                 },
//                 callback: function(response) {
//                     if (response.message && response.message.status === "success" && Array.isArray(response.message.data)) {
//                         let employee_data = response.message.data.find(emp => emp.employee === frm.doc.employee);
                        
//                         if (employee_data) {
//                             frm.set_value('custom_overtime_hours', employee_data.overtime_hours || 0);
//                             frm.set_value('custom_shortfall_hours', employee_data.shortfall_hours || 0);
//                         } else {
//                             frappe.msgprint(__('No check-in data found for the selected employee.'));
//                             frm.set_value('custom_overtime_hours', 0);
//                             frm.set_value('custom_shortfall_hours', 0);
//                         }
//                     } else {
//                         frappe.msgprint(__('Error fetching check-in data. Please try again.'));
//                         frm.set_value('custom_overtime_hours', 0);
//                         frm.set_value('custom_shortfall_hours', 0);
//                     }
//                 },
//                 error: function(err) {
//                     frappe.msgprint(__('API request failed. Please check the server logs.'));
//                     console.error("Error fetching employee check-in data:", err);
//                     frm.set_value('custom_overtime_hours', 0);
//                     frm.set_value('custom_shortfall_hours', 0);
//                 }
//             });
//         } else {
//             frappe.msgprint(__('Please select an employee.'));
//         }
//     }
// });


// frappe.ui.form.on('Additional Salary', {
//     setup: function (frm) {
//         toggle_salary_component_fields(frm);
//     },
//     salary_component: function (frm) {
//         toggle_salary_component_fields(frm);
//     }
// });

// function toggle_salary_component_fields(frm) {
//     const component = frm.doc.salary_component?.toLowerCase() || "";

//     frm.toggle_display('custom_overtime_hours', component === "over time");
//     frm.toggle_display('custom_shortfall_hours', component === "short hour");
// }
