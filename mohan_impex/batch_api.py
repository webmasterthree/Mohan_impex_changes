import frappe
import re

@frappe.whitelist()
def get_next_batch_id(item):
    """
    Suggest the next unique batch ID in NSE-XXXX format.
    Ensures uniqueness even if some NSE-XXXX values were manually added.
    """

    # Get existing NSE-style batch_ids
    existing_batches = frappe.get_all(
        "Batch",
        filters={"batch_id": ["like", "NSE-%"]},
        fields=["batch_id"]
    )

    # Build a set for fast lookup
    existing_ids = {b["batch_id"] for b in existing_batches}

    max_number = 0
    for batch_id in existing_ids:
        match = re.match(r"NSE-(\d+)", batch_id)
        if match:
            num = int(match.group(1))
            max_number = max(max_number, num)

    # Try until we find an unused ID (just in case of skipped numbers)
    while True:
        max_number += 1
        next_batch_id = f"NSE-{str(max_number).zfill(4)}"
        if next_batch_id not in existing_ids:
            break

    return {"next_batch_id": next_batch_id}
