from nicaragua_tax_receipt.patches.v1_0.add_tax_receipt_custom_fields import execute as add_tax_receipt_custom_fields
from nicaragua_tax_receipt.patches.v1_1.add_payment_entry_concept_field import execute as add_payment_entry_concept_field
from nicaragua_tax_receipt.patches.v1_1.add_supplier_check_print_field import execute as add_supplier_check_print_field
from nicaragua_tax_receipt.patches.v1_1.align_cheque_section_visibility import execute as align_cheque_section_visibility
from nicaragua_tax_receipt.patches.v1_1.ensure_payment_entry_concept_layout import execute as ensure_payment_entry_concept_layout
from nicaragua_tax_receipt.patches.v1_1.move_payment_entry_transaction_section_below_concept import (
	execute as move_payment_entry_transaction_section_below_concept,
)
from nicaragua_tax_receipt.patches.v1_1.normalize_spanish_labels import execute as normalize_spanish_labels
from nicaragua_tax_receipt.patches.v1_1.reorder_payment_entry_field_order import execute as reorder_payment_entry_field_order


def after_migrate():
	"""Keep target metadata aligned on every migrate.

	This makes the app self-healing on sites whose metadata drifted because of
	older customizations, partial installs, or previous manual changes.
	"""
	add_tax_receipt_custom_fields()
	add_payment_entry_concept_field()
	add_supplier_check_print_field()
	ensure_payment_entry_concept_layout()
	move_payment_entry_transaction_section_below_concept()
	reorder_payment_entry_field_order()
	align_cheque_section_visibility()
	normalize_spanish_labels()
