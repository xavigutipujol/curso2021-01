# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "sale - Module name",
    "version": "11.0.1.0.0",
    "author": "<AUTHOR(S)>, Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "maintainers": ["your-github-login"],
    "license": "AGPL-3",
    "depends": [
        "sale",
        "helpdesk_xavigutierrez"
    ],
    "data": [
        "views/helpdesk_ticket_view.xml",
        "views/product_product_view.xml",
        "views/sale_order_view.xml",
        "reports/sale_report_templates.xml",
    ],
}
