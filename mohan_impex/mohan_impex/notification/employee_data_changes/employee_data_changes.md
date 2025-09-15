<p>Dear HR Manager,</p>
<p>The employee record for <strong>{{doc.name}}</strong> has been modified by {{ frappe.session.user }}</p>
<p>
  <a href="{{ frappe.utils.get_url_to_form('Employee', doc.name) }}" style="background: #007bff; color: #fff; padding: 10px 15px; text-decoration: none; border-radius: 4px;">Please review the changes</a>
</p>
<p>Thank you</p>


<style>
  .footer { color: #777; font-size: 12px; margin-top: 20px; }
</style>

<p class="footer">
  This is an automated notification. Please do not reply to this email.
</p>