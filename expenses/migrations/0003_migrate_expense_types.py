from django.db import migrations, models
import django.db.models.deletion

from expenses.constants import ExpenseTypeChoices


def create_expense_types(apps, schema_editor):
    ExpenseType = apps.get_model('expenses', 'ExpenseType')
    
    # Crear los tipos de gastos desde las constantes
    for code, name in ExpenseTypeChoices.choices:
        ExpenseType.objects.create(code=code, name=name)


def reverse_create_expense_types(apps, schema_editor):
    ExpenseType = apps.get_model('expenses', 'ExpenseType')
    ExpenseType.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_expenses_expense_type'),
    ]

    operations = [
        # 1. Crear el nuevo modelo ExpenseType
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(help_text='Código único para el tipo de gasto', max_length=3, unique=True, verbose_name='Código')),
                ('name', models.CharField(help_text='Nombre del tipo de gasto', max_length=50, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Tipo de Gasto',
                'verbose_name_plural': 'Tipos de Gastos',
                'ordering': ['name'],
            },
        ),
        
        # 2. Crear una columna temporal para mantener el código del tipo de gasto
        migrations.AddField(
            model_name='expenses',
            name='expense_type_code',
            field=models.CharField(max_length=3, null=True),
        ),
        
        # 3. Poblar los tipos de gastos
        migrations.RunPython(create_expense_types, reverse_create_expense_types),
        
        # 4. Crear la nueva columna ForeignKey
        migrations.AddField(
            model_name='expenses',
            name='expense_type_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='expenses.expensetype', verbose_name='Tipo de gasto'),
        ),
        
        # 5. Migrar los datos
        migrations.RunPython(
            code=lambda apps, schema_editor: apps.get_model('expenses', 'Expenses').objects.all().update(
                expense_type_code=models.F('expense_type')
            ),
            reverse_code=lambda apps, schema_editor: None
        ),
        
        # 6. Actualizar la relación
        migrations.RunPython(
            code=lambda apps, schema_editor: apps.get_model('expenses', 'Expenses').objects.all().update(
                expense_type_new_id=models.Subquery(
                    apps.get_model('expenses', 'ExpenseType').objects.filter(
                        code=models.OuterRef('expense_type_code')
                    ).values('id')[:1]
                )
            ),
            reverse_code=lambda apps, schema_editor: None
        ),
        
        # 7. Eliminar la columna antigua
        migrations.RemoveField(
            model_name='expenses',
            name='expense_type',
        ),
        
        # 8. Renombrar la nueva columna
        migrations.RenameField(
            model_name='expenses',
            old_name='expense_type_new',
            new_name='expense_type',
        ),
        
        # 9. Eliminar la columna temporal
        migrations.RemoveField(
            model_name='expenses',
            name='expense_type_code',
        ),
    ]