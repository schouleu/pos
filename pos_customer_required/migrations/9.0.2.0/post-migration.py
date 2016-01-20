# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


BOOLEAN_TO_SELECTION = {
    'false': 'no',
    'true': 'order',
}


def migrate_require_customer(cr):
    for old, new in BOOLEAN_TO_SELECTION.iteritems():
        cr.execute("""
            UPDATE pos_config
            SET require_customer='%s'
            WHERE %s = '%s'
        """ % (new, openupgrade.get_legacy_name('require_customer'), old))


def migrate(cr, installed_version):
    migrate_require_customer(cr)
