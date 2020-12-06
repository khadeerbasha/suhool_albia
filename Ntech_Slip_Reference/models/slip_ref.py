# -*- coding: utf-8 -*-
from odoo import api, fields, models
import base64
from random import choice
from string import digits
import itertools
from werkzeug import url_encode
import pytz

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
from odoo.addons.resource.models.resource_mixin import timezone_datetime

class stock_picking(models.Model):
	_inherit = 'stock.picking'

	slip_ref = fields.Char('Slip Reference')
	
	@api.constrains('slip_ref')
	def _check_slip_ref(self):
		if self.slip_ref:
			for record in self:
				stock_ids = self.env['stock.picking'].search([('slip_ref', '=', self.slip_ref)])
				if len(stock_ids) > 1:
					raise ValidationError("Slip Reference Should be Unique") 
	
stock_picking()

class account_payment(models.Model):
	_inherit = 'account.payment'

	pay_ref = fields.Char('Reference')

account_payment()

class AccountPaymentRegister(models.TransientModel):
	_inherit = 'account.payment.register'

	pay_ref = fields.Char('Reference')
	
	def _create_payment_vals_from_wizard(self):
		payment_vals = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
		payment_vals['pay_ref'] = self.pay_ref
		return payment_vals


AccountPaymentRegister()
  
#class sale_order_line(models.Model):
#	_inherit = 'sale.order.line'

#	analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")

#sale_order_line()

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    
StockPicking()
