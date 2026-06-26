import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	hide_legacy_header_fields()

	create_custom_fields(
		{
			"Purchase Taxes and Charges": [
				{
					"fieldname": "custom_require_official_receipt_no",
					"fieldtype": "Check",
					"insert_after": "rate",
					"label": "Require Official Receipt No",
					"default": "0",
					"in_list_view": 1,
				}
			],
			"Advance Taxes and Charges": [
				{
					"fieldname": "custom_require_official_receipt_no",
					"fieldtype": "Check",
					"insert_after": "rate",
					"label": "Require Official Receipt No",
					"allow_on_submit": 1,
					"default": "0",
					"in_list_view": 1,
					"read_only": 1,
				}
			],
		},
		update=True,
	)

	create_custom_fields(
		{
			"Advance Taxes and Charges": [
				{
					"fieldname": "custom_official_receipt_no",
					"fieldtype": "Data",
					"insert_after": "custom_require_official_receipt_no",
					"label": "Official Receipt No",
					"allow_on_submit": 1,
					"in_list_view": 1,
					"mandatory_depends_on": "eval:doc.custom_require_official_receipt_no",
				}
			],
		},
		update=True,
	)


def hide_legacy_header_fields():
	for custom_field_name in [
		"Purchase Taxes and Charges Template-custom_require_official_receipt_no",
		"Payment Entry-custom_official_receipt_no",
	]:
		if not frappe.db.exists("Custom Field", custom_field_name):
			continue

		frappe.db.set_value("Custom Field", custom_field_name, "hidden", 1, update_modified=False)
