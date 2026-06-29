from nicaragua_tax_receipt.bootstrap import reconcile_site_metadata


def after_migrate():
	"""Keep target metadata aligned on every migrate.

	This makes the app self-healing on sites whose metadata drifted because of
	older customizations, partial installs, or previous manual changes.
	"""
	reconcile_site_metadata()
