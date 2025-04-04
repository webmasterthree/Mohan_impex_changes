frappe.ui.form.on('Increment Letter', {
	// Add row events
	earnings_add(frm) {
		update_totals(frm);
	},
	deductions_add(frm) {
		update_totals(frm);
	},
	contribution_from_employer_add(frm) {
		update_totals(frm);
	},

	// Remove row events - use delayed update
	earnings_remove(frm) {
		delay_update(frm);
	},
	deductions_remove(frm) {
		delay_update(frm);
	},
	contribution_from_employer_remove(frm) {
		delay_update(frm);
	},

	// Ensure recalculation before save
	validate(frm) {
		update_totals(frm);
	}
});

// Triggers for field value changes in child tables
frappe.ui.form.on('Earnings Component', {
	monthly(frm, cdt, cdn) {
		update_totals(frm);
	},
	yearly(frm, cdt, cdn) {
		update_totals(frm);
	}
});

frappe.ui.form.on('Deduction Component', {
	monthly(frm, cdt, cdn) {
		update_totals(frm);
	}
});

frappe.ui.form.on('Contribution from Employer', {
	monthly(frm, cdt, cdn) {
		update_totals(frm);
	},
	yearly(frm, cdt, cdn) {
		update_totals(frm);
	}
});

// Delayed update for row deletions to allow Frappe to complete internal updates
let updateTimer;
function delay_update(frm) {
	if (updateTimer) clearTimeout(updateTimer);
	updateTimer = setTimeout(() => update_totals(frm), 100);
}

// Main calculation logic
function update_totals(frm) {
	let total_earnings = 0;
	let total_deductions = 0;
	let total_employer_contribution = 0;

	let yearly_earnings = 0;
	let yearly_employer_contribution = 0;

	// Calculate Earnings
	(frm.doc.earnings || []).forEach(row => {
		total_earnings += flt(row.monthly);
		yearly_earnings += flt(row.yearly);
	});

	// Calculate Deductions
	(frm.doc.deductions || []).forEach(row => {
		total_deductions += flt(row.monthly);
	});

	// Calculate Employer Contributions
	(frm.doc.contribution_from_employer || []).forEach(row => {
		total_employer_contribution += flt(row.monthly);
		yearly_employer_contribution += flt(row.yearly);
	});

	const net_in_hand = total_earnings - total_deductions;
	const total_ctc = yearly_earnings + yearly_employer_contribution;

	// Set values only if changed
	if (frm.doc.total_gross !== total_earnings) {
		frm.set_value('total_gross', total_earnings);
	}
	if (frm.doc.total_deduction !== total_deductions) {
		frm.set_value('total_deduction', total_deductions);
	}
	if (frm.doc.total_employer_contribution !== total_employer_contribution) {
		frm.set_value('total_employer_contribution', total_employer_contribution);
	}
	if (frm.doc.net_in_hand !== net_in_hand) {
		frm.set_value('net_in_hand', net_in_hand);
	}
	if (frm.doc.total_ctc !== total_ctc) {
		frm.set_value('total_ctc', total_ctc);
	}
}
