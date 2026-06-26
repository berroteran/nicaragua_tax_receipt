import frappe


LABELS = {
	"Purchase Taxes and Charges-custom_require_official_receipt_no": "Requiere comprobante oficial",
	"Advance Taxes and Charges-custom_require_official_receipt_no": "Requiere comprobante oficial",
	"Advance Taxes and Charges-custom_official_receipt_no": "Numero de comprobante oficial",
	"Supplier-impresion_cheque": "Impresion en cheque",
}


def execute():
	for custom_field_name, label in LABELS.items():
		if not frappe.db.exists("Custom Field", custom_field_name):
			continue

		frappe.db.set_value("Custom Field", custom_field_name, "label", label, update_modified=False)
