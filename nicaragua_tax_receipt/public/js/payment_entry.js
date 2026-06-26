frappe.ui.form.on("Payment Entry", {
	refresh(frm) {
		frm.trigger("toggle_cheque_reference_requirements");
		frm.trigger("configure_tax_grid");
	},

	mode_of_payment(frm) {
		frm.trigger("toggle_cheque_reference_requirements");
	},

	taxes_on_form_rendered(frm) {
		frm.trigger("configure_tax_grid");
	},

	toggle_cheque_reference_requirements(frm) {
		const isCheque = frm.doc.mode_of_payment === "Cheque";
		frm.set_df_property("transaction_references", "depends_on", "eval:true");
		frm.set_df_property("reference_no", "depends_on", "eval:true");
		frm.set_df_property("reference_date", "depends_on", "eval:true");
		frm.set_df_property("clearance_date", "depends_on", "eval:doc.docstatus==1");
		frm.set_df_property("reference_no", "reqd", isCheque ? 1 : 0);
		frm.set_df_property("reference_date", "reqd", isCheque ? 1 : 0);
		frm.refresh_field("transaction_references");
		frm.refresh_field("reference_no");
		frm.refresh_field("reference_date");
		frm.refresh_field("clearance_date");
	},

	configure_tax_grid(frm) {
		if (frm.fields_dict.taxes?.grid) {
			frm.fields_dict.taxes.grid.toggle_display("custom_require_official_receipt_no", true);
			frm.fields_dict.taxes.grid.toggle_display("custom_official_receipt_no", true);
			frm.fields_dict.taxes.grid.update_docfield_property(
				"custom_require_official_receipt_no",
				"read_only",
				0
			);
			frm.fields_dict.taxes.grid.update_docfield_property(
				"custom_official_receipt_no",
				"read_only",
				0
			);
		}
	},
});
