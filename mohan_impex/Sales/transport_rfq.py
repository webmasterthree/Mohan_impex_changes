import frappe
from frappe.model.document import Document

class TransportRFQ(Document):
    def before_save(self):
        if not self.transporter_details or not self.transporters:
            return

        for detail_row in self.transporter_details:
            for transporter_row in self.transporters:
                if transporter_row.transporter == detail_row.transporter:
                    transporter_row.quoted_amount = detail_row.quoted_amount
                    transporter_row.expected_delivery = detail_row.expected_delivery
                    transporter_row.remarks = detail_row.remarks
                    transporter_row.driver = detail_row.driver
                    transporter_row.driver_name = detail_row.driver_name
                    transporter_row.phone_number = detail_row.phone_number
                    transporter_row.vehicle_number = detail_row.vehicle_number
                    detail_row.status = 'RFQ Sent'
