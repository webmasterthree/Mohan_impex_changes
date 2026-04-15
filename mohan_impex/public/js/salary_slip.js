frappe.ui.form.on("Salary Slip", {
    validate: function(frm) {
        calculate_bonus_values(frm);
    },
    on_submit: function(frm){
        calculate_bonus_values(frm);
    },
    after_save: function(frm){
        calculate_bonus_values(frm);
    }
});

function calculate_bonus_values(frm) {

    let earning_components = [
        "Basic Pay",
        "House Rent Allowance",
        "Conveyance Allowance",
        "Telephone Allowance",
        "Special Allowance",
        "Working Holiday"
    ];

    let deduction_components = [
        "Employees State Insurance Corporation For Bonus",
        "Professional Tax For Bonus",
        "Provident Fund For Bonus"
    ];

    let total_earnings = 0;
    let total_deductions = 0;

    // Earnings total
    (frm.doc.earnings || []).forEach(row => {
        if (earning_components.includes(row.salary_component)) {
            console.log("Amount",row.amount)
            total_earnings += row.amount || 0;
        }
    });

    // Deductions total
    (frm.doc.deductions || []).forEach(row => {
        if (deduction_components.includes(row.salary_component)) {
            total_deductions += row.amount || 0;
        }
    });

    // Set values
    frm.set_value("custom_bonus_earnings", total_earnings);
    frm.set_value("custom_bonus_deduction", total_deductions);
    frm.set_value("custom_bonus_net_pay", total_earnings - total_deductions);
}