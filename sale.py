#! -*- coding: utf8 -*-

from trytond.model import ModelSQL, Workflow, fields, ModelView
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.pyson import Bool, Eval, Or, Not, Equal, And
from trytond import backend
from trytond.wizard import Wizard, StateView, StateTransition, Button

__all__ = ['Sale','SalePaymentForm','WizardSalePayment']

__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'
    pos = fields.Many2One('account.pos','Punto de venta Afip',
			    states={
			    'readonly': Eval('state') != 'draft',
			    })
    
    pos_sequences = fields.Many2One('account.pos.sequence','Factura Afip',
			                 domain=[('pos','=',Eval('pos'))],
			                 depends=['pos'],
	                                 states={
					   'readonly': Eval('state') != 'draft',
					   })

    pyafipws_concept = fields.Selection([
       ('1', u'1-Productos'),
       ('2', u'2-Servicios'),
       ('3', u'3-Productos y Servicios (mercado interno)'),
       ('4', u'4-Otros (exportación)'),
       ('', ''),
       ], 'Concepto',
       select=True,
       states={
           'readonly': Eval('state') != 'draft',
           'required': Eval('pos.pos_type') == 'electronic',
            }, depends=['state']
       )

    #transactions =fields.Function(
                        #fields.One2Many ('account_invoice_ar.afip_transaction',
                        #None, u"Transacciones"),'get_transactions')

    #def get_transactions(self,name):
      #Afip_Transactions =Pool().get('account_invoice_ar.afip_transaction')
      #this_transactions = Afip_Transactions.search(['sale','=',self.id])
      #if this_transactions:
         #return [at.id for at in this_transactions]
      #return None
    
    @classmethod
    def workflow_to_end(cls, sales):
      super(Sale, cls).workflow_to_end(sales)
    
    @staticmethod
    def default_pos():
      Config = Pool().get('sale.configuration')
      config = Config(1)
      if config.pos_default:
	return config.pos_default.id
      return None
    
    @staticmethod
    def default_pos_sequences():
      Config = Pool().get('sale.configuration')
      config = Config(1)
      if config.pos_sequence_default:
	return config.pos_sequence_default.id
      return None
        
    @staticmethod
    def default_pyafipws_concept():
      Config = Pool().get('sale.configuration')
      config = Config(1)
      if config.pyafipws_concept_default:
	return config.pyafipws_concept_default
      return None
    
    
    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().cursor
        sql_table = cls.__table__()
        table = TableHandler(cursor, cls, module_name)
        if not table.column_exist('pos'):
	    table.add_raw_column(
                    'pos',
                    cls.pos.sql_type(),
                    cls.pos.sql_format, None, None
                    )
        if not table.column_exist('pos_sequences'):
	    table.add_raw_column(
                    'pos_sequences',
                    cls.pos_sequences.sql_type(),
                    cls.pos_sequences.sql_format, None, None
                    )
        if not table.column_exist('pyafipws_concept'):
	    table.add_raw_column(
                    'pyafipws_concept',
                    cls.pyafipws_concept.sql_type(),
                    cls.pyafipws_concept.sql_format, None, None
                    )
	    
    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
    
    def _get_invoice_sale(self, invoice_type):
      Invoice = super(Sale, self)._get_invoice_sale(invoice_type)
      Invoice.pos = self.pos
      Invoice.invoice_type = self.pos_sequences
      Invoice.pyafipws_concept = self.pyafipws_concept
      return Invoice
  
class SalePaymentForm:  
    'Sale Payment Form'
    __name__ = 'sale.payment.form'
    pos = fields.Many2One('account.pos','Punto de venta Afip',
			   required=True,readonly='True')
    
    pos_sequences = fields.Many2One('account.pos.sequence','Factura Afip',
			                 domain=[('pos','=',Eval('pos'))],
			                 depends=['pos'],
	                                 required=True,readonly='True')
    
    pyafipws_concept = fields.Selection([
       ('1', u'1-Productos'),
       ('2', u'2-Servicios'),
       ('3', u'3-Productos y Servicios (mercado interno)'),
       ('4', u'4-Otros (exportación)'),
       ('', ''),
       ], 'Concepto',
       select=True,
       states={
           'readonly': Eval('state') != 'draft',
           'required': Eval('pos.pos_type') == 'electronic',
            }, depends=['state']
       )


class WizardSalePayment:
    'Wizard Sale Payment'
    __name__ = 'sale.payment'
       
    def default_start(self, fields):
        pool = Pool()
        Sale = pool.get('sale.sale')
        sale = Sale(Transaction().context['active_id'])
        result = super(WizardSalePayment, self).default_start(fields)
        result['pos'] = sale.pos.id
        result['pos_sequences'] = sale.pos_sequences.id
        result['pyafipws_concept'] = sale.pyafipws_concept
        return result
      
    def transition_pay_(self):
        result = super(WizardSalePayment, self).transition_pay_()        
        Sale = Pool().get('sale.sale')
        sale = Sale(Transaction().context['active_id'])
        
        Invoice = Pool().get('account.invoice')
        
        AFIP_Transaction = Pool().get('account_invoice_ar.afip_transaction')
  
        if sale.invoices:
           for invoice in sale.invoices:
	     if invoice.state == 'draft':
               invoice.description = sale.reference
               invoice.reference = sale.reference
               invoice_id = invoice.id
               Invoice.post([invoice])
                             
               
               #afip_transaction = AFIP_Transactions.search(['invoice','=',invoice_id])
               #with Transaction().new_cursor():
		 #for transaction in afip_transaction:
		   #transaction.sale = sale.id
		 #Transaction().cursor.commit()	
              
       
        for payment in sale.payments:
                    invoice = sale.invoices[0]
                    payment.invoice = invoice.id
                    if payment.party != invoice.party:
                        payment.party = invoice.party
                    payment.save()
        
        Sale.workflow_to_end([sale])
	return result
    
    def transition_print_(self):
        return 'end'
      
    def do_print_(self, action):
        return super(WizardSalePayment, self).do_print_(action)
