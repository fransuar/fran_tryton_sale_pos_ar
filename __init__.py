# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from .sale import *
from .configuration import *
from .invoice import *
from reports import *


def register():
    Pool.register(
        Invoice,
        AfipWSTransaction,
        Sale,
        SalePaymentForm,
        Configuration,        
        module='z_fix__invoice_ar__sale_pos', type_='model')
    Pool.register(
        SalePosTicketReport,
        SaleReportSummary,
        SaleReportSummaryByParty,
        module='z_fix__invoice_ar__sale_pos', type_='report')
    Pool.register(
        WizardSalePayment,
        module='z_fix__invoice_ar__sale_pos', type_='wizard')