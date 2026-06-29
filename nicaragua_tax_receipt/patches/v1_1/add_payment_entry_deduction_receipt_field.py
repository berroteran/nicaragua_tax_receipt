import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


DOCTYPE = "Payment Entry Deduction"
FIELDNAME = "custom_receipt_no"


def execute():
	field_config = {
		"label": "No Comprobante",
		"fieldtype": "Data",
		"insert_after": "description",
		"in_list_view": 1,
		"in_standard_filter": 1,
		"in_global_search": 1,
		"search_index": 1,
		"report_hide": 0,
		"columns": 2,
	}

	if not frappe.db.exists("Custom Field", f"{DOCTYPE}-{FIELDNAME}"):
		create_custom_fields(
			{
				DOCTYPE: [
					{
						"fieldname": FIELDNAME,
						**field_config,
					}
				]
			},
			update=True,
		)
		return

	frappe.db.set_value(
		"Custom Field",
		f"{DOCTYPE}-{FIELDNAME}",
		field_config,
		update_modified=False,
	)
