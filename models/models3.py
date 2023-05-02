# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class stuff_printer(models.Model):
    _name = 'print_table'
    _description = 'our test module to print stuff we try'

    show_stuff = fields.Text(name="Stuff", required=True)
