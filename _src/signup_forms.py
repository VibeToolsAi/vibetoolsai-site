# MailerLite sign-up forms embedded on free product pages (rule 22.11: every free product collects emails).
# Two MailerLite forms per lead magnet: one without marketing consent (delivery only), one with consent.
# The page's JS posts to the consent form only when the visitor ticks the separate, unticked box.
# Endpoint: https://assets.mailerlite.com/jsonp/<account>/forms/<form_id>/subscribe (double opt-in on).
ML_ACCOUNT = "2745036"
SIGNUP = {
    "hlzeqi": {  # Where It All Is (Kept Kindly, EN) -> groups "KK – Checklist (all)" / + "KK – Emails OK (consent v1.2)"
        "plain": "204846007616275594",
        "consent": "204846008281072930",
        "lang": "en",
        "button": "Email me the free sheet",
        "consent_text": ("Yes, also send me Kept Kindly emails: a short welcome series, one practical email a week, "
                         "news about new planners and occasional offers. I can unsubscribe at any time."),
    },
}
