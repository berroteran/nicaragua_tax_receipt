import frappe


DOCTYPE = "Payment Entry"

SECTION_VISIBILITY_RULE = "eval:true"
REFERENCE_VISIBILITY_RULE = "eval:true"
CLEARANCE_VISIBILITY_RULE = "eval:doc.docstatus==1"


def execute():
	upsert_property_setter("transaction_references", "depends_on", SECTION_VISIBILITY_RULE)
	upsert_property_setter("reference_no", "depends_on", REFERENCE_VISIBILITY_RULE)
	upsert_property_setter("reference_date", "depends_on", REFERENCE_VISIBILITY_RULE)
	upsert_property_setter("clearance_date", "depends_on", CLEARANCE_VISIBILITY_RULE)
	frappe.clear_cache(doctype=DOCTYPE)


def upsert_property_setter(fieldname, property_name, value):
	filters = {
		"doc_type": DOCTYPE,
		"field_name": fieldname,
		"property": property_name,
	}
	existing = frappe.db.get_value("Property Setter", filters, "name")

	if existing:
		frappe.db.set_value("Property Setter", existing, "value", value, update_modified=False)
		return

	frappe.get_doc(
		{
			"doctype": "Property Setter",
			"doctype_or_field": "DocField",
			"doc_type": DOCTYPE,
			"field_name": fieldname,
			"property": property_name,
			"property_type": "Data",
			"value": value,
		}
	).insert(ignore_permissions=True)
