import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


FIELD_NAME = "concepto"
FIELD_LABEL = "Concepto"
PAYMENT_ENTRY = "Payment Entry"


def execute():
	if frappe.db.exists("Custom Field", f"{PAYMENT_ENTRY}-{FIELD_NAME}"):
		update_existing_custom_field()
		return

	create_custom_fields(
		{
			PAYMENT_ENTRY: [
				{
					"fieldname": FIELD_NAME,
					"fieldtype": "Small Text",
					"label": FIELD_LABEL,
					"insert_after": "taxes_and_charges_section",
					"description": "Colocar el concepto del pago",
					"reqd": 1,
					"in_standard_filter": 1,
					"search_index": 1,
					"allow_on_submit": 1,
				}
			]
		},
		update=True,
	)


def update_existing_custom_field():
	values = {
		"label": FIELD_LABEL,
		"fieldtype": "Small Text",
		"description": "Colocar el concepto del pago",
		"reqd": 1,
		"in_standard_filter": 1,
		"search_index": 1,
		"allow_on_submit": 1,
		"hidden": 0,
	}
	frappe.db.set_value("Custom Field", f"{PAYMENT_ENTRY}-{FIELD_NAME}", values, update_modified=False)
