from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget

from .models import Expenses, ExpenseType
from tenant.models import BusinessUnit


class ExpenseTypeResource(resources.ModelResource):
    class Meta:
        model = ExpenseType
        fields = ('id', 'code', 'name', 'limit', 'created_at', 'updated_at')
        export_order = ('code', 'name', 'limit', 'created_at', 'updated_at')
        import_id_fields = ['code']


class ExpensesResource(resources.ModelResource):
    business_unit = fields.Field(
        column_name='Unidad Negocio',
        attribute='business_unit',
        widget=ForeignKeyWidget(BusinessUnit, 'name')
    )

    expense_type = fields.Field(
        column_name='Tipo Gasto',
        attribute='expense_type',
        widget=ForeignKeyWidget(ExpenseType, 'name')
    )

    date = fields.Field(
        column_name='Fecha',
        attribute='date',
        widget=DateWidget(format='%d/%m/%Y')
    )

    amount = fields.Field(
        column_name='Monto',
        attribute='amount'
    )

    is_fixed = fields.Field(
        column_name='Gasto Fijo',
        attribute='is_fixed'
    )

    observations = fields.Field(
        column_name='Observaciones',
        attribute='observations'
    )

    created_at = fields.Field(
        column_name='Fecha Creación',
        attribute='created_at'
    )

    class Meta:
        model = Expenses
        fields = (
            'id', 'date', 'business_unit', 'expense_type',
            'amount', 'is_fixed', 'observations',
            'created_at',
        )
        export_order = (
            'id', 'date', 'business_unit', 'expense_type',
            'amount', 'is_fixed', 'observations',
            'created_at',
        )
        import_id_fields = ['id']
