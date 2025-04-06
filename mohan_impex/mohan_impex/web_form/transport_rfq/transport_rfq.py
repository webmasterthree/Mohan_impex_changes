# import frappe

# def get_context(context):
# 	# do your magic here
# 	pass

import frappe

def get_context(context):
    # Fetch Transport RFQ document
    context.title = "Transport RFQ"
    context.show_sidebar = 1
    context.add_breadcrumbs = 1
    pass