#! -*- coding: utf8 -*-

from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pyson import Eval, Bool
from trytond.pool import Pool, PoolMeta

__all__ = ['Configuration']

__metaclass__ = PoolMeta


class Configuration:
    'Sale Configuration'
    __name__ = 'sale.configuration'
    
    pos_default = fields.Property(fields.Many2One('account.pos',
						  'Punto de venta AFIP \n por defecto',
						  required=True))
    
    pos_sequence_default = fields.Property(fields.Many2One('account.pos.sequence',
						      'Factura AFIP \n por defecto',
			                              domain=[('pos','=',Eval('pos_default'))],
			                              depends=['pos_default'],
			                              required = True,
	                                 ))
    
    pyafipws_concept_default = fields.Property(fields.Selection([
         ('1', u'1-Productos'),
         ('2', u'2-Servicios'),
         ('3', u'3-Productos y Servicios (mercado interno)'),
         ('4', u'4-Otros (exportación)'),
         ('', ''),
         ], 'Concepto Facturado AFIP \n por defecto',
       ))               