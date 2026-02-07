// salary_structure.js (or salary_structure__js)

function set_master_formula_autocomplete(frm) {
    if (!window.mohan_impex || !mohan_impex.mohan_impex_utils) {
        console.error("mohan_impex utilities not loaded yet");
        // Optionally retry after a short delay
        setTimeout(() => set_master_formula_autocomplete(frm), 100);
        return;
    }
    
    mohan_impex.mohan_impex_utils.set_autocompletions_for_condition_and_formula(
        frm,
        null,
        "custom_formula"
    );
}

frappe.ui.form.on('Salary Structure', {
    refresh: function(frm) {
        set_master_formula_autocomplete(frm);
    },
    
    custom_formula: function(frm) {
        set_master_formula_autocomplete(frm);
    }
});