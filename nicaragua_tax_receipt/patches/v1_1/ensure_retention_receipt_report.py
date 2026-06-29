import json

import frappe


REPORT_NAME = "Comprobantes de retencion en la fuente"
REPORT_MODULE = "Nicaragua Tax Receipt"
WORKSPACE_NAME = "Accounting"
WORKSPACE_SHORTCUT_LABEL = "Comprobantes de retencion en la fuente"
WORKSPACE_CARD_LABEL = "Informes Nicaragua"
ROLES = ("Accounts User", "Accounts Manager", "Auditor", "System Manager")


def execute():
	ensure_report()
	ensure_workspace_shortcut()
	ensure_workspace_card()
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


def ensure_workspace_card():
	if not frappe.db.exists("Workspace", WORKSPACE_NAME):
		return

	workspace = frappe.get_doc("Workspace", WORKSPACE_NAME)
	ensure_workspace_link_group(workspace)
	ensure_workspace_content_block(workspace)
	workspace.save(ignore_permissions=True)


def ensure_workspace_link_group(workspace):
	card_break = None
	report_link = None

	for link in workspace.links:
		if link.type == "Card Break" and link.label == WORKSPACE_CARD_LABEL:
			card_break = link
		elif link.type == "Link" and link.link_to == REPORT_NAME and link.is_query_report:
			report_link = link

	if not card_break:
		workspace.append(
			"links",
			{
				"type": "Card Break",
				"label": WORKSPACE_CARD_LABEL,
			},
		)
		card_break = workspace.links[-1]

	if not report_link:
		workspace.append(
			"links",
			{
				"type": "Link",
				"label": REPORT_NAME,
				"link_type": "Report",
				"link_to": REPORT_NAME,
				"is_query_report": 1,
			},
		)
		report_link = workspace.links[-1]

	report_link.label = REPORT_NAME
	report_link.link_type = "Report"
	report_link.link_to = REPORT_NAME
	report_link.is_query_report = 1
	report_link.hidden = 0

	rebuild_workspace_link_order(workspace, card_break, report_link)


def rebuild_workspace_link_order(workspace, card_break, report_link):
	other_links = [row for row in workspace.links if row.name not in {card_break.name, report_link.name}]
	workspace.set("links", other_links + [card_break, report_link])


def ensure_workspace_content_block(workspace):
	try:
		content = json.loads(workspace.content or "[]")
	except Exception:
		content = []

	content = [
		block
		for block in content
		if not (
			block.get("type") == "card"
			and block.get("data", {}).get("card_name") == WORKSPACE_CARD_LABEL
		)
	]

	content.append(
		{
			"id": "ntr-informes-nicaragua-card",
			"type": "card",
			"data": {
				"card_name": WORKSPACE_CARD_LABEL,
				"col": 4,
			},
		}
	)
	workspace.content = json.dumps(content)
