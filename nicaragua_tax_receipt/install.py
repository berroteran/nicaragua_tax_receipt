from nicaragua_tax_receipt.bootstrap import reconcile_site_metadata


def after_install():
	"""Provision all required metadata when the app is installed on a site."""
	reconcile_site_metadata()
