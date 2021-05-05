# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Module name",
    "version": "11.0.1.0.0",
    "author": "<AUTHOR(S)>, Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "maintainers": ["your-github-login"],
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail"
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "reports/helpdesk_ticket_report_templates.xml",
        "reports/res_partner_templates.xml",
        "views/helpdesk_menu.xml",
        "views/helpdesk_view.xml",
        "wizards/create_ticket_view.xml",
        "views/helpdesk_tag_view.xml",
        "data/delete_tag_cron.xml",

    ],
}
