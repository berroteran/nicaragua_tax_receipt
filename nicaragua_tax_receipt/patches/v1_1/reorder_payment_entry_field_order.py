import json

import frappe


DOCTYPE = "Payment Entry"
CONCEPT_SECTION = "custom_concepto"
CONCEPT_FIELD = "concepto"
TRANSACTION_SECTION = "transaction_references"


def execute():
	field_order = get_current_field_order()
	if not field_order:
		return

	field_order = ensure_after(field_order, CONCEPT_FIELD, CONCEPT_SECTION)
	field_order = ensure_after(field_order, TRANSACTION_SECTION, CONCEPT_FIELD)
	upsert_field_order_property_setter(field_order)


def get_current_field_order():
	meta = frappe.get_meta(DOCTYPE, cached=False)
	return [field.fieldname for field in meta.fields if field.fieldname]


def ensure_after(field_order, fieldname, insert_after):
	if fieldname not in field_order or insert_after not in field_order:
		return field_order

	field_order = [value for value in field_order if value != fieldname]
	index = field_order.index(insert_after)
	field_order.insert(index + 1, fieldname)
	return field_order


def upsert_field_order_property_setter(field_order):
	existing = frappe.db.sql(
		"""
		SELECT name
		FROM `tabProperty Setter`
		WHERE doc_type = %s
		  AND property = 'field_order'
		  AND (field_name IS NULL OR field_name = '')
		LIMIT 1
		""",
		(DOCTYPE,),
		as_dict=True,
	)
	existing_name = existing[0].name if existing else None
	value = json.dumps(field_order)

	if existing_name:
		frappe.db.set_value("Property Setter", existing_name, "value", value, update_modified=False)
		frappe.clear_cache(doctype=DOCTYPE)
		return

	frappe.make_property_setter(
		{
			"doctype_or_field": "DocType",
			"doctype": DOCTYPE,
			"property": "field_order",
			"value": value,
			"property_type": "Data",
		},
		validate_fields_for_doctype=False,
	)
