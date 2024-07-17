# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import base64
import requests


class FleetTrip(models.Model):
    _name = 'fleet.trip'
    _rec_name = 'equipment_id'
    _order = 'schedule_date asc'
    _description = 'Hành trình vận tải'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # def _get_location_selection(self):
    #     selection = []
    #     list_location = self.env['fleet.location'].search([])
    #     for location in list_location:
    #         selection += [(location.code, location.name)]
    #     return selection

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    equipment_id = fields.Many2one('maintenance.equipment', string='Xe')
    location_name = fields.Char()
    location_dest_name = fields.Char()
    # location_id = fields.Selection(selection=_get_location_selection)
    # location_dest_id = fields.Selection(selection=_get_location_selection)
    location_id = fields.Many2one('fleet.location', string="Tên điểm đi")
    location_dest_id = fields.Many2one('fleet.location', string="Tên điểm đến")
    eating_fee = fields.Monetary('Tiền ăn')
    law_money = fields.Monetary('Tiền luật')
    road_tiket_fee = fields.Monetary('Vé cầu đường')
    incurred_fee = fields.Monetary('Phát sinh')
    incurred_note = fields.Char('Ghi chú phát sinh')
    incurred_fee_2 = fields.Monetary('Phát sinh 2')
    incurred_note_2 = fields.Char('Ghi chú phát sinh 2')
    note = fields.Text('Ghi chú hành trình')
    fee_total = fields.Monetary('Tổng cộng', compute='_compute_fee_total')
    odometer_start = fields.Integer('Số CTM xuất phát')
    odometer_dest = fields.Integer('Số CTM điểm đích')
    odometer_end = fields.Integer('Số KM hành trình', compute='_compute_odometer_end', store=True)
    employee_id = fields.Many2one('hr.employee', string='Nhân viên')
    state = fields.Selection([
        ('1_draft', 'Đang Chờ'),
        ('2_confirm', 'Đã Xuất Phát'),
        ('3_done', 'Hoàn Thành')
    ], string='Trạng thái', default='1_draft')
    schedule_date = fields.Date(string='Ngày thực hiện')
    start_date = fields.Datetime(string='Bắt đầu', readonly=True)
    end_date = fields.Datetime(string='Kết thúc', readonly=True)

    delivery_id = fields.Many2one('stock.delivery', string='Phiếu xuất kho')
    code = fields.Char(related='delivery_id.code', store=True)
    project_id = fields.Many2one(related='delivery_id.project_id')

    district_id = fields.Many2one('res.country.district', string='Huyện', domain="[('state_id', '=', state_id)]")
    ward_id = fields.Many2one('res.country.ward', string='Xã', domain="[('district_id', '=', district_id)]")
    state_id = fields.Many2one("res.country.state", string='Tỉnh', ondelete='restrict',
                               domain="[('country_id', '=', country_id)]")

    location_start_district_state = fields.Char(string='Địa chỉ điểm đi',
                                                compute='_compute_location_start_district_state')
    location_dest_district_state = fields.Char(string='Địa chỉ điểm đến',
                                               compute='_compute_location_dest_district_state')

    location_compute_name = fields.Char(string='Nơi xuất phát',
                                        compute='_compute_location_compute_name')
    location_dest_compute_name = fields.Char(string='Nơi đến',
                                             compute='_compute_location_dest_compute_name')

    district_dest_id = fields.Many2one('res.country.district', string='Huyện',
                                       domain="[('state_id', '=', state_dest_id)]")
    ward_dest_id = fields.Many2one('res.country.ward', string='Xã', domain="[('district_id', '=', district_dest_id)]")
    state_dest_id = fields.Many2one("res.country.state", string='Tỉnh', ondelete='restrict',
                                    domain="[('country_id', '=', country_id)]")

    country_id = fields.Many2one('res.country', default=241, string='Quốc gia', ondelete='restrict')
    company_name = fields.Char(string='Công ty')
    fleet_product_id = fields.Many2one('fleet.product', string='Mặt hàng', ondelete='restrict')
    address_start = fields.Char(string="Địa chỉ xuất phát")
    address_end = fields.Char(string="Địa chỉ đích")
    start_hour = fields.Datetime(string="Giờ xuất phát")
    end_hour = fields.Datetime(string="Giờ đến đích")
    is_approved = fields.Boolean(string="Đã xác nhận")
    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model', '=', 'fleet.trip')],
                                     string='Attachments')

    @api.onchange("location_id")
    def onchange_location_id(self):
        if self.location_id:
            self.location_name = self.location_id.name
            self.district_id = self.location_id.district_id.id
            self.ward_id = self.location_id.ward_id.id
            self.state_id = self.location_id.state_id.id
            self.address_start = self.location_id.note

    @api.onchange("location_dest_id")
    def onchange_location_dest_id(self):
        if self.location_dest_id:
            self.location_dest_name = self.location_dest_id.name
            self.district_dest_id = self.location_dest_id.district_id.id
            self.ward_dest_id = self.location_dest_id.ward_id.id
            self.state_dest_id = self.location_dest_id.state_id.id
            self.address_end = self.location_dest_id.note

    @api.depends("district_id", "ward_id", "state_id")
    def _compute_location_compute_name(self):
        for record in self:
            location_name = []
            if record.ward_id:
                location_name.append(record.ward_id.name or '')
            if record.district_id:
                location_name.append(record.district_id.name or '')
            if record.state_id:
                location_name.append(record.state_id.name or '')
            record.location_compute_name = ', '.join(location_name)

    @api.depends("district_dest_id", "ward_dest_id", "state_dest_id")
    def _compute_location_dest_compute_name(self):
        for record in self:
            location_name = []
            if record.ward_dest_id:
                location_name.append(record.ward_dest_id.name or '')
            if record.district_dest_id:
                location_name.append(record.district_dest_id.name or '')
            if record.state_dest_id:
                location_name.append(record.state_dest_id.name or '')
            record.location_dest_compute_name = ', '.join(location_name)

    @api.onchange("equipment_id")
    def _onchange_equipment_id(self):
        if self.equipment_id and self.equipment_id.owner_user_id and self.equipment_id.owner_user_id.employee_id:
            self.employee_id = self.equipment_id.owner_user_id.employee_id.id

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        if self.employee_id and self.employee_id.user_id:
            equipment_id = self.env['maintenance.equipment'].search([
                ('owner_user_id', '=', self.employee_id.user_id.id)], limit=1)
            if equipment_id:
                self.equipment_id = equipment_id.id

    @api.depends("eating_fee", "law_money", "road_tiket_fee", "incurred_fee", "incurred_fee_2")
    def _compute_fee_total(self):
        for rec in self:
            rec.fee_total = rec.eating_fee + rec.law_money + rec.road_tiket_fee + rec.incurred_fee + rec.incurred_fee_2

    def do_start_trip(self):
        self.start_date = fields.Datetime.now()
        self.state = '2_confirm'

    def do_end_trip(self):
        self.end_date = fields.Datetime.now()
        self.state = '3_done'

    def do_odometer_start(self, odometer_start, attachments=[]):
        self.odometer_start = odometer_start
        if not attachments:
            return True
        for attachment in attachments:
            self.env['ir.attachment'].create({
                'name': self.equipment_id.name,
                'type': 'url',
                'url': attachment,
                'res_model': 'fleet.trip',
                'res_id': self.id,
            })

    def do_odometer_end(self, odometer_end, attachments=[]):
        self.odometer_dest = odometer_end
        if not attachments:
            return True
        for attachment in attachments:
            self.env['ir.attachment'].create({
                'name': self.equipment_id.name,
                'type': 'url',
                'url': attachment,
                'res_model': 'fleet.trip',
                'res_id': self.id,
            })
    
    def do_odometer_dest(self, odometer_dest, attachments=[]):
        self.odometer_dest = odometer_dest
        if not attachments:
            return True
        for attachment in attachments:
            self.env['ir.attachment'].create({
                'name': self.equipment_id.name,
                'type': 'url',
                'url': attachment,
                'res_model': 'fleet.trip',
                'res_id': self.id,
            })

    @api.depends('odometer_start', 'odometer_dest')
    def _compute_odometer_end(self):
        for record in self:
            odometer_total = record.odometer_dest - record.odometer_start
            record.odometer_end = odometer_total if odometer_total >= 0 else 0

    @api.depends("district_id", "state_id")
    def _compute_location_start_district_state(self):
        for record in self:
            location_name = []
            if record.district_id:
                location_name.append(record.district_id.name or '')
            if record.state_id:
                location_name.append(record.state_id.name or '')
            record.location_start_district_state = ', '.join(location_name)

    @api.depends("district_dest_id", "state_dest_id")
    def _compute_location_dest_district_state(self):
        for record in self:
            location_name = []
            if record.district_dest_id:
                location_name.append(record.district_dest_id.name or '')
            if record.state_dest_id:
                location_name.append(record.state_dest_id.name or '')
            record.location_dest_district_state = ', '.join(location_name)

    # @api.onchange('location_id', 'location_dest_id')
    # def onchange_location(self):
    #     company_name = ''
    #     if self.location_id:
    #         company_name = "NM" + self.location_id
    #     elif self.location_dest_id:
    #         company_name = "NM" + self.location_dest_id
    #     self.company_name = company_name

    def do_approve(self):
        view_id = self.env.ref('fleet_trip.fleet_trip_approve_form_view').id
        act_window = {
            'type': 'ir.actions.act_window',
            'name': (_("Confirmation")),
            'res_model': 'fleet.trip.approve.reject',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {'default_fleet_trip_id': self.id}}
        return act_window

    def do_reject(self):
        view_id = self.env.ref('fleet_trip.fleet_trip_reject_form_view').id
        act_window = {
            'type': 'ir.actions.act_window',
            'name': (_("Confirmation")),
            'res_model': 'fleet.trip.approve.reject',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {'default_fleet_trip_id': self.id}}
        return act_window


class StockDelvery(models.Model):
    _name = 'stock.delivery'
    _rec_name = 'code'
    _description = 'Phiếu xuất kho'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string='Số phiếu', required=True)
    project_id = fields.Many2one('fleet.project', string='Dự án', required=True)
    category_id = fields.Many2one('fleet.category', string='Hạng mục')
    stock_date = fields.Date(string="Ngày", default=fields.Date.today)
    location_dest_id = fields.Many2one('fleet.location', 'Điểm đích', required=True)
    partner_receive_id = fields.Many2one('res.partner', string='Người nhận', required=True)
    partner_receive_phone = fields.Char(related='partner_receive_id.phone', string='Điện thoại')
    shipping_id = fields.Many2one('res.partner', string='Đơn vị vận chuyển', required=True)
    driver_id = fields.Many2one('res.partner', string='Lái xe', required=True)
    driver_phone = fields.Char(related='driver_id.phone', string='Điện thoại')
    equipment_id = fields.Many2one('maintenance.equipment', string='Xe', required=True)
    delivery_line = fields.One2many('stock.delivery.line', 'delivery_id', string='Chi tiết xuất kho')


class StockDelveryLine(models.Model):
    _name = 'stock.delivery.line'
    _description = 'Chi tiết xuất kho'

    delivery_id = fields.Many2one('stock.delivery', string='Phiếu xuất kho')
    product_id = fields.Many2one('product.template', string='Sản phẩm', required=True)
    section = fields.Char(related='product_id.section', string='Tiết diện')
    product_length = fields.Integer(related='product_id.product_length', string='Dài')
    uom_id = fields.Many2one(related='product_id.uom_id', string='Đơn vị')
    out_qty = fields.Float(string='SL Xuất')
    bao_qty = fields.Float(string='Bao')
    note = fields.Text(string='Ghi chú')
