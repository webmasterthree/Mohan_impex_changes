import frappe

def table_exists(table_name):
    return bool(frappe.db.sql("""
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = DATABASE() 
        AND table_name = %s
    """, table_name))
# get all doctypes (only tables that exist in DB)
def runscript():
    doctypes = frappe.get_all("DocType", filters={"istable": 1, "module": ["!=","Mohan Impex"]}, pluck="name")
    for dt in sorted(doctypes):
        table_name = f"tab{dt}"
        if table_exists(table_name):
            try:
                count = frappe.db.count(dt)
                if count > 1:
                    print(f"{dt} : {count}")
            except Exception as e:
                print(f"⚠️ Skipped {dt} ({table_name}) → {str(e)}")


import os
import shutil
import frappe

def export_employee_files():
    site_path = frappe.get_site_path()
    base_private = os.path.join(site_path, "private", "files")
    base_public = os.path.join(site_path, "public", "files")

    # Folder where you want to keep organized employee files
    export_base = os.path.join(site_path, "employee_files")
    os.makedirs(export_base, exist_ok=True)

    # Get all files attached to Employee doctype
    files = frappe.get_all("File",
        filters={"attached_to_doctype": "Dashboard Info"},
        fields=["file_url", "file_name", "is_private", "attached_to_name"]
    )

    for f in files:
        emp_id = f.attached_to_name or "Unknown"
        target_folder = os.path.join(export_base, emp_id)
        os.makedirs(target_folder, exist_ok=True)

        # Pick correct source folder
        if f.is_private:
            source_path = os.path.join(base_private, os.path.basename(f.file_url))
        else:
            source_path = os.path.join(base_public, os.path.basename(f.file_url))

        # Destination path
        target_path = os.path.join(target_folder, f.file_name)

        # Copy if exists
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)  # keeps metadata
            print(f"✅ Copied {source_path} → {target_path}")
        else:
            print(f"⚠️ Missing file: {source_path}")

    print(f"\n🎉 Export completed! Files stored in: {export_base}")
