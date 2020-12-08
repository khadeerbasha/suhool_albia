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
	analytic_account_id = fields.Many2one(related="sale_id.analytic_account_id", string="Analytic Account", store=True, readonly=False)
	
	def _create_backorder(self):
		""" This method is called when the user chose to create a backorder. It will create a new
		picking, the backorder, and move the stock.moves that are not `done` or `cancel` into it.
		"""
		backorders = self.env['stock.picking']
		for picking in self:
			moves_to_backorder = picking.move_lines.filtered(lambda x: x.state not in ('done', 'cancel'))
			if moves_to_backorder:
				backorder_picking = picking.copy({
					'name': '/',
					'move_lines': [],
					'move_line_ids': [],
					'backorder_id': picking.id,
					'slip_ref': False
				})
				picking.message_post(
					body=_('The backorder <a href=# data-oe-model=stock.picking data-oe-id=%d>%s</a> has been created.') % (
						backorder_picking.id, backorder_picking.name))
				moves_to_backorder.write({'picking_id': backorder_picking.id})
				moves_to_backorder.mapped('package_level_id').write({'picking_id':backorder_picking.id})
				moves_to_backorder.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
				backorders |= backorder_picking
		return backorders
	
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
  
class sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	bales = fields.Float('Bales')

sale_order_line()

class account_move_line(models.Model):
	_inherit = 'account.move.line'

	bales = fields.Float('Bales')

account_move_line()

class stock_move(models.Model):
	_inherit = 'stock.move'

	#def _compute_is_analytic(self):
		#for order in self:
			#order.analytic_account_id = order.picking_id.analytic_account_id

	bales = fields.Float('Bales')
	#analytic_account_id = fields.Many2one('account.analytic.account', compute='_compute_is_analytic', string="Analytic Account", store=True, readonly=False)
	analytic_account_id = fields.Many2one(related="picking_id.analytic_account_id", string="Analytic Account", store=True, readonly=False)
stock_move()

class purchase_order_line(models.Model):
	_inherit = 'purchase.order.line'

	bales = fields.Float('Bales')

purchase_order_line()
