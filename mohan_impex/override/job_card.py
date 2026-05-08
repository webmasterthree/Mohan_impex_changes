from erpnext.manufacturing.doctype.job_card.job_card import JobCard as ERPNextJobCard


class CustomJobCard(ERPNextJobCard):

	def get_overlap_for(self, args, open_job_cards=None):
		return {}