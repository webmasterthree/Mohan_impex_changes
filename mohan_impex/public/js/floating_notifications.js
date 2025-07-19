frappe.ui.form.on("Sales Order", {
    onload: function (frm) {
        frappe.call({
            method: "mohan_impex.testapi.get_my_assignment_notifications",
            callback: function (r) {
                if (r.message && r.message.length) {
                    r.message.forEach(log => {
                        show_floating_notification(log.subject, log.email_content);
                    });
                }
            }
        });
    }
});

function show_floating_notification(title, html) {
    let notification = $(`<div class="floating-notification">
        <h4>${title}</h4>
        <div>${html}</div>
    </div>`);

    notification.css({
        position: "fixed",
        bottom: "20px",
        right: "20px",
        background: "#f0f0f0",
        padding: "15px",
        borderRadius: "8px",
        zIndex: 10000,
        boxShadow: "0 2px 8px rgba(0,0,0,0.15)"
    });

    $("body").append(notification);

    setTimeout(() => {
        notification.fadeOut(300, () => notification.remove());
    }, 5000);
}
