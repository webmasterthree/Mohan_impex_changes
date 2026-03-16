import frappe

@frappe.whitelist()
def last_created_batch(item):
    # Setting up the filter for 'item' if it's passed
    filters = {}
    if item:
        filters = {"item": item}
    
    # Fetching the batches based on the passed 'item' argument
    res = frappe.db.get_all(
        "Batch",
        filters=filters,
        fields=["name", "item", "item_name", "creation"],
        order_by="creation desc",  # Order by creation date to get the latest batch first
        limit=1  # Get only the most recent batch
    )
    
    return res