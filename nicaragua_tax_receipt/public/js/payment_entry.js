frappe.ui.form.on("Payment Entry", {
	refresh(frm) {
		frm.trigger("configure_tax_grid");
	},

	taxes_on_form_rendered(frm) {
		frm.trigger("configure_tax_grid");
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
