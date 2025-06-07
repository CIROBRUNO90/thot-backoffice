# constants.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class ExpenseTypeChoices(models.TextChoices):
    """Tipos de gastos permitidos en el sistema"""
    # Gastos operativos
    SALARIES = 'SAL', _('Salarios')
    UTILITIES = 'UTL', _('Servicios')
    MOBILITY = 'MOB', _('Movilidad')

    # Gastos comerciales
    MARKETING = 'MKT', _('Marketing')
    SHIPPING = 'SHI', _('Envíos')

    # Gastos administrativos
    TAXES = 'TAX', _('Impuestos')
    PLATFORM = 'PLT', _('PlataformaS')

    # Gastos de inventario
    SUPPLIES = 'SUP', _('Insumos')
    LOGISTICS = 'LOG', _('Logística')

    PUBLICITY = 'PUB', _('Publicidad')
    RENT = 'REN', _('Alquiler')

    # Otros
    OTHER = 'OTH', _('Otros')


class ExpensesSubTypeChoices(models.TextChoices):
    """Subtipos de gastos permitidos en el sistema"""
    # Gastos operativos
    WATER = 'WAT', _('Agua')
    ELECTRICITY = 'ELE', _('Electricidad')
    GAS = 'GAS', _('Gas')
    INTERNET = 'INT', _('Internet')
    PHONE = 'PHO', _('Teléfono')

    # Gastos comerciales
    PACKAGING = 'PAC', _('Embalaje')
    SENDINGS = 'SEN', _('Envíos')

    # Gastos administrativos
    INCOME_TAX = 'ITX', _('Impuesto a las Ganancias')
    VAT = 'VAT', _('IVA')
    PLATFORM = 'PLT', _('Plataforma')

    # Gastos de inventario
    RAW_MATERIALS = 'RAW', _('Materias Primas')
    TRANSPORT = 'TRA', _('Transporte')

    ADVERTISING = 'ADV', _('Publicidad')
    WAREHOUSE = 'WAR', _('Almacén')
    ACCOUNTING = 'ACC', _('Contabilidad')

    UBER = 'UBE', _('Uber')

    # Otros
    OTHER = 'OTH', _('Otros')
