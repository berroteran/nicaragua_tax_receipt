import frappe


DOCTYPE = "Payment Entry"
FIELDNAME = "transaction_references"
INSERT_AFTER = "concepto"


def execute():
	upsert_insert_after_property_setter()


def upsert_insert_after_property_setter():
	filters = {
		"doc_type": DOCTYPE,
		"field_name": FIELDNAME,
		"property": "insert_after",
	}
	existing = frappe.db.get_value("Property Setter", filters, "name")

	if existing:
		frappe.db.set_value("Property Setter", existing, "value", INSERT_AFTER, update_modified=False)
		frappe.clear_cache(doctype=DOCTYPE)
		return

	frappe.make_property_setter(
		{
			"doctype_or_field": "DocField",
			"doc_type": DOCTYPE,
			"field_name": FIELDNAME,
			"property": "insert_after",
			"value": INSERT_AFTER,
			"property_type": "Data",
		},
		validate_fields_for_doctype=False,
	)
