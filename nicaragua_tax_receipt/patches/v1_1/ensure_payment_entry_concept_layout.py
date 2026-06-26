import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


DOCTYPE = "Payment Entry"
SECTION_FIELDNAME = "custom_concepto"
CONCEPT_FIELDNAME = "concepto"


def execute():
	if not frappe.db.exists("Custom Field", f"{DOCTYPE}-{SECTION_FIELDNAME}"):
		create_custom_fields(
			{
				DOCTYPE: [
					{
						"fieldname": SECTION_FIELDNAME,
						"fieldtype": "Section Break",
						"label": "Concepto",
						"insert_after": "contact_email",
					}
				]
			},
			update=True,
		)

	if frappe.db.exists("Custom Field", f"{DOCTYPE}-{CONCEPT_FIELDNAME}"):
		frappe.db.set_value(
			"Custom Field",
			f"{DOCTYPE}-{CONCEPT_FIELDNAME}",
			"insert_after",
			SECTION_FIELDNAME,
			update_modified=False,
		)
