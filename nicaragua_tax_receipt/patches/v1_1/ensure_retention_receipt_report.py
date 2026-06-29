import frappe


REPORT_NAME = "Comprobantes de retencion en la fuente"
REPORT_MODULE = "Nicaragua Tax Receipt"
WORKSPACE_NAME = "Accounting"
WORKSPACE_SHORTCUT_LABEL = "Comprobantes de retencion en la fuente"
ROLES = ("Accounts User", "Accounts Manager", "Auditor", "System Manager")


def execute():
	ensure_report()
	ensure_workspace_shortcut()
	frappe.clear_cache()


def ensure_report():
	report = frappe.get_doc("Report", REPORT_NAME) if frappe.db.exists("Report", REPORT_NAME) else None

	if not report:
		report = frappe.get_doc(
			{
				"doctype": "Report",
				"report_name": REPORT_NAME,
				"name": REPORT_NAME,
				"ref_doctype": "Payment Entry",
				"report_type": "Script Report",
				"module": REPORT_MODULE,
				"is_standard": "Yes",
				"prepared_report": 0,
				"roles": [{"role": role} for role in ROLES],
			}
		)
		report.insert(ignore_permissions=True)
		return

	report.ref_doctype = "Payment Entry"
	report.report_type = "Script Report"
	report.module = REPORT_MODULE
	report.is_standard = "Yes"
	report.disabled = 0
	report.prepared_report = 0
	report.set("roles", [{"role": role} for role in ROLES])
	report.save(ignore_permissions=True)


def ensure_workspace_shortcut():
	if not frappe.db.exists("Workspace", WORKSPACE_NAME):
		return

	workspace = frappe.get_doc("Workspace", WORKSPACE_NAME)
	for shortcut in workspace.shortcuts:
		if shortcut.type == "Report" and shortcut.link_to == REPORT_NAME:
			shortcut.link_to = REPORT_NAME
			if shortcut.label != WORKSPACE_SHORTCUT_LABEL:
				shortcut.label = WORKSPACE_SHORTCUT_LABEL
			workspace.save(ignore_permissions=True)
			return

	workspace.append(
		"shortcuts",
		{
			"type": "Report",
			"link_to": REPORT_NAME,
			"label": WORKSPACE_SHORTCUT_LABEL,
		},
	)
	workspace.save(ignore_permissions=True)
