#! -*- coding: utf8 -*-

from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond import backend

import logging
import collections


__all__ = ['AfipWSTransaction','Invoice']
__metaclass__ = PoolMeta


IVA_AFIP_CODE = collections.defaultdict(lambda: 0)


class AfipWSTransaction:
    'AFIP WS Transaction'
    __name__ = 'account_invoice_ar.afip_transaction'    
    
    invoice = fields.Integer('Invoice')
    
    #sale = fields.Integer('Sale')
    
    @classmethod
    def __register__(cls, z_fix__invoice_ar__sale_pos):
        #super(AfipWSTransaction, cls).__register__(z_fix__invoice_ar__sale_pos)
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().cursor
        table = TableHandler(cursor, cls, z_fix__invoice_ar__sale_pos)
        cursor.execute("ALTER TABLE account_invoice_ar_afip_transaction\
	                  DROP CONSTRAINT IF EXISTS account_invoice_ar_afip_transaction_invoice_fkey;")
	
	#if not table.column_exist('sale'):
	    #table.add_raw_column(
                    #'sale',
                    #cls.sale.sql_type(),
                    #cls.sale.sql_format, None, None
                    #)

class Invoice:
    'Invoice'
    __name__ = 'account.invoice'
    transactions =fields.Function(
                        fields.One2Many ('account_invoice_ar.afip_transaction',
                        None, u"Transacciones"),'get_transactions')

    def get_transactions(self,name):
      Afip_Transactions =Pool().get('account_invoice_ar.afip_transaction')
      this_transactions = Afip_Transactions.search(['invoice','=',self.id])
      if this_transactions:
         return [at.id for at in this_transactions]
      return None
  
    #def do_pyafipws_request_cae(self):
        #logger = logging.getLogger('pyafipws')
        #"Request to AFIP the invoices' Authorization Electronic Code (CAE)"
        ## if already authorized (electronic invoice with CAE), ignore
        #if self.pyafipws_cae:
            #logger.info(u'Se trata de obtener CAE de la factura que ya tiene. '\
                        #u'Factura: %s, CAE: %s', self.number, self.pyafipws_cae)
            #return
        ## get the electronic invoice type, point of sale and service:
        #pool = Pool()

        #Company = pool.get('company.company')
        #company_id = Transaction().context.get('company')
        #if not company_id:
            #logger.info(u'No hay companía')
            #return

        #company = Company(company_id)

        #tipo_cbte = self.invoice_type.invoice_type
        #punto_vta = self.pos.number
        #service = self.pos.pyafipws_electronic_invoice_service
        ## check if it is an electronic invoice sale point:
        ###TODO
        ##if not tipo_cbte:
        ##    self.raise_user_error('invalid_sequence', pos.invoice_type.invoice_type)

        ## authenticate against AFIP:
        #auth_data = company.pyafipws_authenticate(service=service)

        ## import the AFIP webservice helper for electronic invoice
        #if service == 'wsfe':
            #from pyafipws.wsfev1 import WSFEv1  # local market
            #ws = WSFEv1()
            #if company.pyafipws_mode_cert == 'homologacion':
                #WSDL = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
            #elif company.pyafipws_mode_cert == 'produccion':
                #WSDL = "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL"
        ##elif service == 'wsmtxca':
        ##    from pyafipws.wsmtx import WSMTXCA, SoapFault   # local + detail
        ##    ws = WSMTXCA()
        #elif service == 'wsfex':
            #from pyafipws.wsfexv1 import WSFEXv1 # foreign trade
            #ws = WSFEXv1()
            #if company.pyafipws_mode_cert == 'homologacion':
                #WSDL = "https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?WSDL"
            #elif company.pyafipws_mode_cert == 'produccion':
                #WSDL = "https://servicios1.afip.gov.ar/wsfexv1/service.asmx?WSDL"
        #else:
            #logger.critical(u'WS no soportado: %s', service)
            #return

        ## connect to the webservice and call to the test method
        #ws.LanzarExcepciones = True
        #ws.Conectar(wsdl=WSDL)
        ## set AFIP webservice credentials:
        #ws.Cuit = company.party.vat_number
        #ws.Token = auth_data['token']
        #ws.Sign = auth_data['sign']

        ## get the last 8 digit of the invoice number
        #if self.move:
            #cbte_nro = int(self.move.number[-8:])
        #else:
            #Sequence = pool.get('ir.sequence')
            #cbte_nro = int(Sequence(
                #self.invoice_type.invoice_sequence.id).get_number_next(''))

        ## get the last invoice number registered in AFIP
        #if service == "wsfe" or service == "wsmtxca":
            #cbte_nro_afip = ws.CompUltimoAutorizado(tipo_cbte, punto_vta)
        #elif service == 'wsfex':
            #cbte_nro_afip = ws.GetLastCMP(tipo_cbte, punto_vta)
        #cbte_nro_next = int(cbte_nro_afip or 0) + 1
        ## verify that the invoice is the next one to be registered in AFIP
        #if cbte_nro != cbte_nro_next:
            #self.raise_user_error('invalid_invoice_number', (cbte_nro, cbte_nro_next))

        ## invoice number range (from - to) and date:
        #cbte_nro = cbt_desde = cbt_hasta = cbte_nro_next

        #if self.invoice_date:
            #fecha_cbte = self.invoice_date.strftime("%Y-%m-%d")
        #else:
            #Date = pool.get('ir.date')
            #fecha_cbte = Date.today().strftime("%Y-%m-%d")

        #if service != 'wsmtxca':
            #fecha_cbte = fecha_cbte.replace("-", "")

        ## due and billing dates only for concept "services"
        #concepto = tipo_expo = int(self.pyafipws_concept or 0)
        #if int(concepto) != 1:

            #payments = self.payment_term.compute(self.total_amount, self.currency)
            #last_payment = max(payments, key=lambda x:x[0])[0]
            #fecha_venc_pago = last_payment.strftime("%Y-%m-%d")
            #if service != 'wsmtxca':
                    #fecha_venc_pago = fecha_venc_pago.replace("-", "")
            #if self.pyafipws_billing_start_date:
                #fecha_serv_desde = self.pyafipws_billing_start_date.strftime("%Y-%m-%d")
                #if service != 'wsmtxca':
                    #fecha_serv_desde = fecha_serv_desde.replace("-", "")
            #else:
                #fecha_serv_desde = None
            #if  self.pyafipws_billing_end_date:
                #fecha_serv_hasta = self.pyafipws_billing_end_date.strftime("%Y-%m-%d")
                #if service != 'wsmtxca':
                    #fecha_serv_hasta = fecha_serv_hasta.replace("-", "")
            #else:
                #fecha_serv_hasta = None
        #else:
            #fecha_venc_pago = fecha_serv_desde = fecha_serv_hasta = None

        ## customer tax number:
        #if self.party.vat_number:
            #nro_doc = self.party.vat_number
            #if len(nro_doc) < 11:
                #tipo_doc = 96           # DNI
            #else:
                #tipo_doc = 80           # CUIT
        #else:
            #nro_doc = "0"           # only "consumidor final"
            #tipo_doc = 99           # consumidor final

        ## invoice amount totals:
        #imp_total = str("%.2f" % abs(self.total_amount))
        #imp_tot_conc = "0.00"
        #imp_neto = str("%.2f" % abs(self.untaxed_amount))
        #imp_iva = str("%.2f" % abs(self.tax_amount))
        #imp_subtotal = imp_neto  # TODO: not allways the case!
        #imp_trib = "0.00"
        #imp_op_ex = "0.00"
        #if self.currency.code == 'ARS':
            #moneda_id = "PES"
            #moneda_ctz = 1
        #else:
            #moneda_id = {'USD':'DOL'}[self.currency.code]
            #ctz = 1 / self.currency.rate
            #moneda_ctz =  str("%.2f" % ctz)

        ## foreign trade data: export permit, country code, etc.:
        #if self.pyafipws_incoterms:
            #incoterms = self.pyafipws_incoterms
            #incoterms_ds = dict(self._fields['pyafipws_incoterms'].selection)[self.pyafipws_incoterms]
        #else:
            #incoterms = incoterms_ds = None

        #if incoterms == None and incoterms_ds == None and service == 'wsfex':
            #self.raise_user_error('missing_pyafipws_incoterms')

        #if int(tipo_cbte) == 19 and tipo_expo == 1:
            #permiso_existente =  "N" or "S"     # not used now
        #else:
            #permiso_existente = ""
        #obs_generales = self.comment
        #if self.payment_term:
            #forma_pago = self.payment_term.name
            #obs_comerciales = self.payment_term.name
        #else:
            #forma_pago = obs_comerciales = None
        #idioma_cbte = 1     # invoice language: spanish / español

        ## customer data (foreign trade):
        #nombre_cliente = self.party.name
        #if self.party.vat_number:
            #if self.party.vat_country == "AR":
                ## use the Argentina AFIP's global CUIT for the country:
                #cuit_pais_cliente = self.party.vat_number
                #id_impositivo = None
            #else:
                ## use the VAT number directly
                #id_impositivo = self.party.vat_number
                ## TODO: the prefix could be used to map the customer country
                #cuit_pais_cliente = None
        #else:
            #cuit_pais_cliente = id_impositivo = None
        #if self.invoice_address:
            #address = self.invoice_address
            #domicilio_cliente = " - ".join([
                                        #address.name or '',
                                        #address.street or '',
                                        #address.streetbis or '',
                                        #address.zip or '',
                                        #address.city or '',
                                #])
        #else:
            #domicilio_cliente = ""
        #if self.invoice_address.country:
            ## map ISO country code to AFIP destination country code:
            #pais_dst_cmp = {
                #'ar': 200, 'bo': 202, 'br': 203, 'ca': 204, 'co': 205,
                #'cu': 207, 'cl': 208, 'ec': 210, 'us': 212, 'mx': 218,
                #'py': 221, 'pe': 222, 'uy': 225, 've': 226, 'cn': 310,
                #'tw': 313, 'in': 315, 'il': 319, 'jp': 320, 'at': 405,
                #'be': 406, 'dk': 409, 'es': 410, 'fr': 412, 'gr': 413,
                #'it': 417, 'nl': 423, 'pt': 620, 'uk': 426, 'sz': 430,
                #'de': 438, 'ru': 444, 'eu': 497, 'cr': '206'
                #}[self.invoice_address.country.code.lower()]


        ## create the invoice internally in the helper
        #if service == 'wsfe':
            #ws.CrearFactura(concepto, tipo_doc, nro_doc, tipo_cbte, punto_vta,
                #cbt_desde, cbt_hasta, imp_total, imp_tot_conc, imp_neto,
                #imp_iva, imp_trib, imp_op_ex, fecha_cbte, fecha_venc_pago,
                #fecha_serv_desde, fecha_serv_hasta,
                #moneda_id, moneda_ctz)
        #elif service == 'wsmtxca':
            #ws.CrearFactura(concepto, tipo_doc, nro_doc, tipo_cbte, punto_vta,
                #cbt_desde, cbt_hasta, imp_total, imp_tot_conc, imp_neto,
                #imp_subtotal, imp_trib, imp_op_ex, fecha_cbte,
                #fecha_venc_pago, fecha_serv_desde, fecha_serv_hasta,
                #moneda_id, moneda_ctz, obs_generales)
        #elif service == 'wsfex':
            #ws.CrearFactura(tipo_cbte, punto_vta, cbte_nro, fecha_cbte,
                #imp_total, tipo_expo, permiso_existente, pais_dst_cmp,
                #nombre_cliente, cuit_pais_cliente, domicilio_cliente,
                #id_impositivo, moneda_id, moneda_ctz, obs_comerciales,
                #obs_generales, forma_pago, incoterms,
                #idioma_cbte, incoterms_ds)

        ## analyze VAT (IVA) and other taxes (tributo):
        #if service in ('wsfe', 'wsmtxca'):
            #for tax_line in self.taxes:
                #tax = tax_line.tax
                #if tax.group.name == "IVA":
                    #iva_id = IVA_AFIP_CODE[tax.rate]
                    #base_imp = ("%.2f" % abs(tax_line.base))
                    #importe = ("%.2f" % abs(tax_line.amount))
                    ## add the vat detail in the helper
                    #ws.AgregarIva(iva_id, base_imp, importe)
                #else:
                    #if 'impuesto' in tax_line.tax.name.lower():
                        #tributo_id = 1  # nacional
                    #elif 'iibbb' in tax_line.tax.name.lower():
                        #tributo_id = 3  # provincial
                    #elif 'tasa' in tax_line.tax.name.lower():
                        #tributo_id = 4  # municipal
                    #else:
                        #tributo_id = 99
                    #desc = tax_line.name
                    #base_imp = ("%.2f" % abs(tax_line.base))
                    #importe = ("%.2f" % abs(tax_line.amount))
                    #alic = "%.2f" % tax_line.base
                    ## add the other tax detail in the helper
                    #ws.AgregarTributo(tributo_id, desc, base_imp, alic, importe)

                ### Agrego un item:
                ##codigo = "PRO1"
                ##ds = "Producto Tipo 1 Exportacion MERCOSUR ISO 9001"
                ##qty = 2
                ##precio = "150.00"
                ##umed = 1 # Ver tabla de parámetros (unidades de medida)
                ##bonif = "50.00"
                ##imp_total = "250.00" # importe total final del artículo
        ## analize line items - invoice detail
        ## umeds
        ## Parametros. Unidades de Medida, etc.
        ## https://code.google.com/p/pyafipws/wiki/WSFEX#WSFEX/RECEX_Parameter_Tables
        #if service in ('wsfex', 'wsmtxca'):
            #for line in self.lines:
                #if line.product:
                    #codigo = line.product.code
                #else:
                    #codigo = 0
                #ds = line.description
                #qty = line.quantity
                #umed = 7 # FIXME: (7 - unit)
                #precio = str(line.unit_price)
                #importe_total = str(line.amount)
                #bonif = None  # line.discount
                ##for tax in line.taxes:
                ##    if tax.group.name == "IVA":
                ##        iva_id = IVA_AFIP_CODE[tax.rate]
                ##        imp_iva = importe * tax.rate
                ##if service == 'wsmtxca':
                ##    ws.AgregarItem(u_mtx, cod_mtx, codigo, ds, qty, umed,
                ##            precio, bonif, iva_id, imp_iva, importe+imp_iva)
                #if service == 'wsfex':
                    #ws.AgregarItem(codigo, ds, qty, umed, precio, importe_total,
                                   #bonif)

        ## Request the authorization! (call the AFIP webservice method)
        #try:
            #if service == 'wsfe':
                #ws.CAESolicitar()
                #vto = ws.Vencimiento
            #elif service == 'wsmtxca':
                #ws.AutorizarComprobante()
                #vto = ws.Vencimiento
            #elif service == 'wsfex':
                #ws.Authorize(self.id)
                #vto = ws.FchVencCAE
        ##except SoapFault as fault:
        ##    msg = 'Falla SOAP %s: %s' % (fault.faultcode, fault.faultstring)
        #except Exception, e:
            #if ws.Excepcion:
                ## get the exception already parsed by the helper
                ##import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
                #msg = ws.Excepcion + ' ' + str(e)
            #else:
                ## avoid encoding problem when reporting exceptions to the user:
                #import traceback
                #import sys
                #msg = traceback.format_exception_only(sys.exc_type,
                                                      #sys.exc_value)[0]
        #else:
            #msg = u"\n".join([ws.Obs or "", ws.ErrMsg or ""])
        ## calculate the barcode:
        #if ws.CAE:
            #cae_due = ''.join([c for c in str(ws.Vencimiento or '')
                                       #if c.isdigit()])
            #bars = ''.join([str(ws.Cuit), "%02d" % int(tipo_cbte),
                              #"%04d" % int(punto_vta),
                              #str(ws.CAE), cae_due])
            #bars = bars + self.pyafipws_verification_digit_modulo10(bars)
        #else:
            #bars = ""
               
        #AFIP_Transaction = pool.get('account_invoice_ar.afip_transaction')
        #with Transaction().new_cursor():
            #AFIP_Transaction.create([{'invoice': self.id,
                                #'pyafipws_result': ws.Resultado,
                                #'pyafipws_message': msg,
                                #'pyafipws_xml_request': ws.XmlRequest,
                                #'pyafipws_xml_response': ws.XmlResponse,
                                #}])
            #Transaction().cursor.commit()
        
      
        #if ws.CAE:

            ## store the results
            #vals = {'pyafipws_cae': ws.CAE,
                   #'pyafipws_cae_due_date': vto or None,
                   #'pyafipws_barcode': bars,
                #}
            #if not '-' in vals['pyafipws_cae_due_date']:
                #fe = vals['pyafipws_cae_due_date']
                #vals['pyafipws_cae_due_date'] = '-'.join([fe[:4],fe[4:6],fe[6:8]])

            #self.write([self], vals)