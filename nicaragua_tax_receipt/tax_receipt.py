import frappe
from frappe import _


PAYMENT_ENTRY_DOCTYPE = "Payment Entry"
TAX_REQUIRED_FIELD = "custom_require_official_receipt_no"
CHILD_RECEIPT_FIELD = "custom_official_receipt_no"


def validate_payment_entry(doc, _method=None):
	if doc.doctype != PAYMENT_ENTRY_DOCTYPE or doc.party_type != "Supplier":
		return

	for tax in doc.get("taxes") or []:
		receipt_no = (tax.get(CHILD_RECEIPT_FIELD) or "").strip()
		if tax.get(CHILD_RECEIPT_FIELD) != receipt_no:
			tax.set(CHILD_RECEIPT_FIELD, receipt_no)

		if tax.get(TAX_REQUIRED_FIELD) and not receipt_no:
			frappe.throw(
				_(
					"Row #{0}: Official Receipt No is mandatory for this tax row."
				).format(tax.idx)
			)
