from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import path
from django.http import JsonResponse
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Sum
from django.utils.dateparse import parse_date

# --- REGISTRO DE MODELOS EN EL ADMIN PERSONALIZADO ---
# Incomes
from incomes.models import Income
from incomes.admin import IncomeAdmin
# Expenses
from expenses.models import Expenses, ExpenseType
from expenses.admin import ExpensesAdmin, ExpenseTypeAdmin
# Tenant
from tenant.models import Customer, BusinessUnit, BusinessUnitUser
from tenant.admin import (
    CustomerAdmin, BusinessUnitAdmin, BusinessUnitUserAdmin
)
# Theme
from admin_interface.models import Theme
from admin_interface.admin import ThemeAdmin


class OnlySuperuserThemeAdmin(ThemeAdmin):
    """
    ModelAdmin personalizado que solo permite acceso a superusuarios
    """
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class CustomAdminSite(admin.AdminSite):
    """
    Sitio de administración personalizado con sección de Analítica
    """
    site_header = 'Administración Financiera'
    site_title = 'Admin Financiero'
    index_title = 'Panel de Control'

    def get_app_list(self, request, app_label=None):
        """
        Sobrescribimos este método para agregar nuestra sección 
        personalizada de Analítica
        """
        app_list = super().get_app_list(request, app_label)

        # Agregamos la sección de Analítica al menú
        analytics_app = {
            'name': 'Analítica',
            'app_label': 'analytics',
            'app_url': '/panel/analytics/',
            'has_module_perms': True,
            'models': [
                {
                    'name': 'Dashboard Financiero',
                    'object_name': 'financial_dashboard',
                    'admin_url': '/panel/analytics/dashboard/',
                    'view_only': True,
                    'permissions': {'view': True}
                },
                {
                    'name': 'Reporte de Gastos',
                    'object_name': 'expense_report',
                    'admin_url': '/panel/analytics/expense-report/',
                    'view_only': True,
                    'permissions': {'view': True}
                },
                {
                    'name': 'Análisis de Ingresos',
                    'object_name': 'income_analysis',
                    'admin_url': '/panel/analytics/income-analysis/',
                    'view_only': True,
                    'permissions': {'view': True}
                }
            ],
        }

        # Insertar la app de Analítica al principio de la lista
        app_list.insert(0, analytics_app)

        return app_list

    def get_urls(self):
        """
        Extendemos las URLs del admin para incluir nuestras vistas 
        personalizadas
        """
        urls = super().get_urls()

        custom_urls = [
            # URL principal de Analítica
            path(
                'analytics/',
                self.admin_view(self.analytics_index_view),
                name='analytics_index'
            ),
            # Dashboard Financiero
            path(
                'analytics/dashboard/',
                self.admin_view(self.financial_dashboard_view),
                name='financial_dashboard'
            ),
            # Reporte de Gastos
            path(
                'analytics/expense-report/',
                self.admin_view(self.expense_report_view),
                name='expense_report'
            ),
            # Endpoint de datos para el reporte de gastos
            path(
                'analytics/expense-report/data/',
                self.admin_view(self.expense_report_data_view),
                name='expense_report_data'
            ),
            # Endpoint de datos para el análisis de ingresos
            path(
                'analytics/income-analysis/data/',
                self.admin_view(self.income_analysis_data_view),
                name='income_analysis_data'
            ),
            # Endpoint de datos para el dashboard financiero
            path(
                'analytics/dashboard/data/',
                self.admin_view(self.financial_dashboard_data_view),
                name='financial_dashboard_data'
            ),
            # Análisis de Ingresos
            path(
                'analytics/income-analysis/',
                self.admin_view(self.income_analysis_view),
                name='income_analysis'
            ),
        ]

        # Las URLs personalizadas deben ir antes que las URLs por defecto
        return custom_urls + urls

    @method_decorator(login_required)
    def analytics_index_view(self, request, extra_context=None):
        """
        Vista índice de la sección Analítica
        """
        context = {
            **self.each_context(request),
            'title': 'Analítica',
            'analytics_sections': [
                {
                    'title': 'Dashboard Financiero',
                    'description': (
                        'Vista general de gastos, ingresos y métricas clave'
                    ),
                    'url': 'dashboard',
                    'icon': 'dashboard'
                },
                {
                    'title': 'Reporte de Gastos',
                    'description': (
                        'Análisis detallado de gastos por categoría y período'
                    ),
                    'url': 'expense-report',
                    'icon': 'trending_down'
                },
                {
                    'title': 'Análisis de Ingresos',
                    'description': 'Evolución y proyección de ingresos',
                    'url': 'income-analysis',
                    'icon': 'trending_up'
                }
            ]
        }

        extra_context = extra_context or {}
        context.update(extra_context)

        return TemplateResponse(
            request,
            'panel/analytics/index.html',
            context
        )

    @method_decorator(login_required)
    def financial_dashboard_view(self, request, extra_context=None):
        """
        Vista del Dashboard Financiero principal
        """
        # Aquí irá la lógica para obtener los datos del dashboard
        # Por ahora, usamos datos de ejemplo

        context = {
            **self.each_context(request),
            'title': 'Dashboard Financiero',
            'dashboard_data': {
                'total_gastos_mes': 15000,
                'total_ingresos_mes': 25000,
                'balance_mes': 10000,
                'categorias_gastos': [
                    {'nombre': 'Alimentación', 'total': 3000},
                    {'nombre': 'Transporte', 'total': 2000},
                    {'nombre': 'Servicios', 'total': 4000},
                    {'nombre': 'Otros', 'total': 6000},
                ]
            }
        }

        extra_context = extra_context or {}
        context.update(extra_context)

        return TemplateResponse(
            request,
            'panel/analytics/financial_dashboard.html',
            context
        )

    @method_decorator(login_required)
    def expense_report_view(self, request, extra_context=None):
        """
        Vista del Reporte de Gastos
        """
        context = {
            **self.each_context(request),
            'title': 'Reporte de Gastos',
        }

        extra_context = extra_context or {}
        context.update(extra_context)

        return TemplateResponse(
            request,
            'panel/analytics/expense_report.html',
            context
        )

    @method_decorator(login_required)
    def income_analysis_view(self, request, extra_context=None):
        """
        Vista del Análisis de Ingresos
        """
        context = {
            **self.each_context(request),
            'title': 'Análisis de Ingresos',
        }

        extra_context = extra_context or {}
        context.update(extra_context)

        return TemplateResponse(
            request,
            'panel/analytics/income_analysis.html',
            context
        )

    def expense_report_data_view(self, request):
        """
        Endpoint que devuelve los datos de gastos en JSON para el dashboard de gastos.
        Aplica los filtros de fecha recibidos por GET.
        """
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        qs = Expenses.objects.all()
        if date_from:
            qs = qs.filter(date__gte=parse_date(date_from))
        if date_to:
            qs = qs.filter(date__lte=parse_date(date_to))

        # Gastos por categoría
        gastos_por_categoria = (
            qs.values('expense_type__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        # Evolución diaria
        gastos_diarios = (
            qs.annotate(day=TruncDay('date'))
            .values('day')
            .annotate(total=Sum('amount'))
            .order_by('day')
        )

        # Distribución semanal
        gastos_semanales = (
            qs.annotate(week=TruncWeek('date'))
            .values('week')
            .annotate(total=Sum('amount'))
            .order_by('week')
        )

        # Tendencia mensual
        gastos_mensuales = (
            qs.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        # Estadísticas resumidas
        total_gastos = qs.aggregate(total=Sum('amount'))['total'] or 0
        promedio_diario = (
            sum([x['total'] for x in gastos_diarios]) / gastos_diarios.count()
            if gastos_diarios.count() else 0
        )
        num_categorias = gastos_por_categoria.count()
        mayor_categoria = gastos_por_categoria[0]['total'] if gastos_por_categoria else 0

        data = {
            'gastos_por_categoria': list(gastos_por_categoria),
            'gastos_diarios': list(gastos_diarios),
            'gastos_semanales': list(gastos_semanales),
            'gastos_mensuales': list(gastos_mensuales),
            'stats': {
                'total_gastos': float(total_gastos),
                'promedio_diario': float(promedio_diario),
                'num_categorias': num_categorias,
                'mayor_categoria': float(mayor_categoria),
            }
        }
        return JsonResponse(data)

    def income_analysis_data_view(self, request):
        """
        Endpoint que devuelve los datos de ingresos en JSON para el dashboard
        de ingresos. Aplica los filtros de fecha recibidos por GET.
        """
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        qs = Income.objects.all()
        if date_from:
            qs = qs.filter(date__gte=parse_date(date_from))
        if date_to:
            qs = qs.filter(date__lte=parse_date(date_to))

        # Ingresos por fuente (business_type)
        ingresos_por_fuente = (
            qs.values('business_type')
            .annotate(total=Sum('total'))
            .order_by('-total')
        )

        # Evolución mensual de ingresos
        ingresos_mensuales = (
            qs.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('total'))
            .order_by('month')
        )

        # Comparación anual
        ingresos_anuales = (
            qs.annotate(year=TruncMonth('date'))
            .values('year')
            .annotate(total=Sum('total'))
            .order_by('year')
        )

        # Distribución por estado de pago
        ingresos_por_estado = (
            qs.values('payment_status')
            .annotate(total=Sum('total'))
            .order_by('-total')
        )

        # Estadísticas resumidas
        total_ingresos = qs.aggregate(total=Sum('total'))['total'] or 0
        num_transacciones = qs.count()
        
        # Cálculo de proyecciones mejoradas
        proyecciones = self._calcular_proyecciones_mejoradas(ingresos_mensuales)
        
        # Promedio diario (ajustado según datos disponibles)
        promedio_diario = self._calcular_promedio_diario(ingresos_mensuales, total_ingresos)

        # Ingresos por unidad de negocio
        ingresos_por_unidad = (
            qs.values('business_unit__name')
            .annotate(total=Sum('total'))
            .order_by('-total')
        )
        ingresos_por_unidad = [
            {
                'business_unit': x['business_unit__name'] or 'Sin unidad',
                'total': float(x['total'])
            }
            for x in ingresos_por_unidad
        ]

        data = {
            'ingresos_por_fuente': list(ingresos_por_fuente),
            'ingresos_por_unidad': ingresos_por_unidad,
            'ingresos_mensuales': list(ingresos_mensuales),
            'ingresos_anuales': list(ingresos_anuales),
            'ingresos_por_estado': list(ingresos_por_estado),
            'stats': {
                'total_ingresos': float(total_ingresos),
                'promedio_diario': float(promedio_diario),
                'num_transacciones': num_transacciones,
                'proyeccion': float(proyecciones['proyeccion']),
                'cambio_porcentual': float(proyecciones['cambio_porcentual']),
                'confiabilidad': proyecciones['confiabilidad'],
                'indicadores': proyecciones['indicadores']
            },
            'proyecciones': proyecciones['detalles']
        }
        return JsonResponse(data)

    def financial_dashboard_data_view(self, request):
        """
        Endpoint que devuelve datos combinados de ingresos y gastos
        para el dashboard financiero principal
        """
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        # Obtener datos de gastos
        gastos_qs = Expenses.objects.all()
        if date_from:
            gastos_qs = gastos_qs.filter(date__gte=parse_date(date_from))
        if date_to:
            gastos_qs = gastos_qs.filter(date__lte=parse_date(date_to))

        # Obtener datos de ingresos
        ingresos_qs = Income.objects.all()
        if date_from:
            ingresos_qs = ingresos_qs.filter(date__gte=parse_date(date_from))
        if date_to:
            ingresos_qs = ingresos_qs.filter(date__lte=parse_date(date_to))

        # Gastos por categoría
        gastos_por_categoria = (
            gastos_qs.values('expense_type__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        # Ingresos por unidad de negocio
        ingresos_por_unidad = (
            ingresos_qs.values('business_unit__name')
            .annotate(total=Sum('total'))
            .order_by('-total')
        )
        # Unificar nombres
        nombres_gastos = set(
            x['expense_type__name'] or 'Sin categoría' for x in gastos_por_categoria
        )
        nombres_ingresos = set(
            x['business_unit__name'] or 'Sin unidad' for x in ingresos_por_unidad
        )
        nombres_combinados = list(nombres_gastos.union(nombres_ingresos))
        nombres_combinados.sort()
        # Crear estructura combinada
        datos_cruzados = []
        for nombre in nombres_combinados:
            gasto = next(
                (x['total'] for x in gastos_por_categoria
                 if (x['expense_type__name'] or 'Sin categoría') == nombre),
                0
            )
            ingreso = next(
                (x['total'] for x in ingresos_por_unidad
                 if (x['business_unit__name'] or 'Sin unidad') == nombre),
                0
            )
            datos_cruzados.append({
                'nombre': nombre,
                'gastos': float(gasto),
                'ingresos': float(ingreso)
            })

        # Evolución mensual combinada
        gastos_mensuales = (
            gastos_qs.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        ingresos_mensuales = (
            ingresos_qs.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('total'))
            .order_by('month')
        )

        # Estadísticas resumidas
        total_gastos = gastos_qs.aggregate(total=Sum('amount'))['total'] or 0
        total_ingresos = ingresos_qs.aggregate(total=Sum('total'))['total'] or 0
        balance = total_ingresos - total_gastos

        # Calcular métricas del mes actual (si no hay filtros de fecha)
        from datetime import datetime, date
        hoy = date.today()
        mes_actual = date(hoy.year, hoy.month, 1)
        
        if not date_from and not date_to:
            gastos_mes = (
                gastos_qs.filter(date__gte=mes_actual)
                .aggregate(total=Sum('amount'))['total'] or 0
            )
            ingresos_mes = (
                ingresos_qs.filter(date__gte=mes_actual)
                .aggregate(total=Sum('total'))['total'] or 0
            )
            balance_mes = ingresos_mes - gastos_mes
        else:
            gastos_mes = total_gastos
            ingresos_mes = total_ingresos
            balance_mes = balance

        # Preparar datos para gráficos
        # Combinar datos mensuales para el gráfico de evolución
        meses_combinados = {}
        
        # Agregar gastos
        for gasto in gastos_mensuales:
            mes_key = gasto['month'].strftime('%Y-%m')
            if mes_key not in meses_combinados:
                meses_combinados[mes_key] = {'gastos': 0, 'ingresos': 0, 'mes': gasto['month']}
            meses_combinados[mes_key]['gastos'] = gasto['total']
        
        # Agregar ingresos
        for ingreso in ingresos_mensuales:
            mes_key = ingreso['month'].strftime('%Y-%m')
            if mes_key not in meses_combinados:
                meses_combinados[mes_key] = {'gastos': 0, 'ingresos': 0, 'mes': ingreso['month']}
            meses_combinados[mes_key]['ingresos'] = ingreso['total']

        # Ordenar por mes
        evolucion_mensual = sorted(meses_combinados.values(), key=lambda x: x['mes'])

        # Agrupar gastos por unidad de negocio y tipo de gasto
        gastos_por_unidad_tipo = (
            gastos_qs.values('business_unit__name', 'expense_type__name')
            .annotate(total=Sum('amount'))
        )
        # Agrupar ingresos por unidad de negocio
        ingresos_por_unidad = (
            ingresos_qs.values('business_unit__name')
            .annotate(total=Sum('total'))
        )
        # Listar todas las unidades de negocio
        unidades_gastos = set(x['business_unit__name'] or 'Sin unidad' for x in gastos_por_unidad_tipo)
        unidades_ingresos = set(x['business_unit__name'] or 'Sin unidad' for x in ingresos_por_unidad)
        unidades = sorted(unidades_gastos.union(unidades_ingresos))
        # Listar todos los tipos de gasto
        tipos_gasto = set(x['expense_type__name'] or 'Sin tipo' for x in gastos_por_unidad_tipo)
        tipos_gasto = sorted(tipos_gasto)
        # Construir estructura de datos
        datos_cruzados = []
        for unidad in unidades:
            # Ingresos
            ingreso = next((x['total'] for x in ingresos_por_unidad if (x['business_unit__name'] or 'Sin unidad') == unidad), 0)
            # Gastos por tipo
            gastos_por_tipo = {}
            for tipo in tipos_gasto:
                gasto = next((x['total'] for x in gastos_por_unidad_tipo if (x['business_unit__name'] or 'Sin unidad') == unidad and (x['expense_type__name'] or 'Sin tipo') == tipo), 0)
                gastos_por_tipo[tipo] = float(gasto)
            datos_cruzados.append({
                'unidad': unidad,
                'ingresos': float(ingreso),
                'gastos_por_tipo': gastos_por_tipo
            })
        data = {
            'unidades': datos_cruzados,
            'tipos_gasto': tipos_gasto,
            'evolucion_mensual': evolucion_mensual,
            'stats': {
                'total_gastos': float(total_gastos),
                'total_ingresos': float(total_ingresos),
                'balance': float(balance),
                'gastos_mes': float(gastos_mes),
                'ingresos_mes': float(ingresos_mes),
                'balance_mes': float(balance_mes)
            }
        }
        return JsonResponse(data)

    def _calcular_promedio_diario(self, datos_mensuales, total_ingresos):
        """
        Calcula el promedio diario usando el rango real de días entre el primer y último ingreso
        """
        if not datos_mensuales or total_ingresos == 0:
            return 0
        
        # Obtener fechas reales de ingresos
        from incomes.models import Income
        fechas = list(Income.objects.order_by('date').values_list('date', flat=True))
        if not fechas:
            return 0
        if len(fechas) == 1:
            return total_ingresos
        from datetime import timedelta
        dias = (fechas[-1] - fechas[0]).days + 1
        if dias <= 0:
            dias = 1
        return total_ingresos / dias

    def _calcular_proyecciones_mejoradas(self, datos_mensuales):
        """
        Calcula proyecciones usando análisis de tendencia lineal
        y maneja casos con pocos datos. Si hay pocos datos, solo muestra el próximo mes.
        """
        if not datos_mensuales:
            return {
                'proyeccion': 0,
                'cambio_porcentual': 0,
                'confiabilidad': 'SIN_DATOS',
                'indicadores': {'razon': 'No hay datos disponibles'},
                'detalles': {}
            }

        datos_lista = list(datos_mensuales)
        valores = [float(d['total']) for d in datos_lista]
        
        if len(datos_lista) == 1:
            return {
                'proyeccion': valores[0],
                'cambio_porcentual': 0,
                'confiabilidad': 'BAJA',
                'indicadores': {'razon': 'Solo 1 mes de datos disponibles'},
                'detalles': {
                    'proximo_mes': valores[0],
                    'en_2_meses': None,
                    'en_3_meses': None,
                    'en_6_meses': None
                }
            }

        if len(datos_lista) <= 3:
            promedio = sum(valores) / len(valores)
            return {
                'proyeccion': promedio,
                'cambio_porcentual': self._calcular_cambio_porcentual(valores),
                'confiabilidad': 'MEDIA',
                'indicadores': {'razon': f'Solo {len(datos_lista)} meses de datos'},
                'detalles': {
                    'proximo_mes': promedio,
                    'en_2_meses': None,
                    'en_3_meses': None,
                    'en_6_meses': None
                }
            }

        # Caso 3: 4+ meses - usar análisis de tendencia lineal
        return self._calcular_tendencia_lineal(datos_lista, valores)

    def _calcular_tendencia_lineal(self, datos_lista, valores):
        n = len(valores)
        x = list(range(n))
        sum_x = sum(x)
        sum_y = sum(valores)
        sum_xy = sum(x[i] * valores[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        denominador = n * sum_x2 - sum_x ** 2
        if denominador == 0:
            promedio = sum_y / n
            return {
                'proyeccion': promedio,
                'cambio_porcentual': 0,
                'confiabilidad': 'MEDIA',
                'indicadores': {'razon': 'No se puede calcular tendencia'},
                'detalles': {
                    'proximo_mes': promedio,
                    'en_2_meses': None,
                    'en_3_meses': None,
                    'en_6_meses': None
                }
            }
        pendiente = (n * sum_xy - sum_x * sum_y) / denominador
        intercepto = (sum_y - pendiente * sum_x) / n
        proximo_mes = max(intercepto + pendiente * n, 0)
        detalles = {
            'proximo_mes': proximo_mes,
            'en_2_meses': max(intercepto + pendiente * (n + 1), 0),
            'en_3_meses': max(intercepto + pendiente * (n + 2), 0),
            'en_6_meses': max(intercepto + pendiente * (n + 5), 0),
            'tendencia': pendiente,
            'intercepto': intercepto
        }
        indicadores = self._calcular_indicadores_confiabilidad(valores, pendiente)
        cambio_porcentual = self._calcular_cambio_porcentual(valores)
        return {
            'proyeccion': proximo_mes,
            'cambio_porcentual': cambio_porcentual,
            'confiabilidad': indicadores['confiabilidad'],
            'indicadores': indicadores,
            'detalles': detalles
        }

    def _calcular_indicadores_confiabilidad(self, valores, pendiente):
        """
        Calcula métricas para evaluar la confiabilidad de la proyección
        """
        promedio = sum(valores) / len(valores)
        
        # Coeficiente de variación (menor = más estable)
        desviacion = (sum((x - promedio) ** 2 for x in valores) / len(valores)) ** 0.5
        coef_variacion = desviacion / promedio if promedio > 0 else 0
        
        # Evaluar confiabilidad basada en estabilidad y tendencia
        if coef_variacion < 0.3 and abs(pendiente) < promedio * 0.2:
            confiabilidad = 'ALTA'
        elif coef_variacion < 0.5:
            confiabilidad = 'MEDIA'
        else:
            confiabilidad = 'BAJA'
        
        return {
            'confiabilidad': confiabilidad,
            'coef_variacion': round(coef_variacion, 3),
            'tendencia': round(pendiente, 2),
            'datos_disponibles': len(valores),
            'estabilidad': 'ALTA' if coef_variacion < 0.3 else 'MEDIA' if coef_variacion < 0.5 else 'BAJA'
        }

    def _calcular_cambio_porcentual(self, valores):
        """
        Calcula el cambio porcentual entre el último y penúltimo valor
        """
        if len(valores) < 2:
            return 0
        
        ultimo = valores[-1]
        penultimo = valores[-2]
        
        if penultimo == 0:
            return 100 if ultimo > 0 else 0
        
        cambio = ((ultimo - penultimo) / penultimo) * 100
        return round(cambio, 1)


# Crear una instancia del sitio personalizado
custom_admin_site = CustomAdminSite(name='custom_admin')

custom_admin_site.register(Income, IncomeAdmin)
custom_admin_site.register(Expenses, ExpensesAdmin)
custom_admin_site.register(ExpenseType, ExpenseTypeAdmin)
custom_admin_site.register(Customer, CustomerAdmin)
custom_admin_site.register(BusinessUnit, BusinessUnitAdmin)
custom_admin_site.register(BusinessUnitUser, BusinessUnitUserAdmin)
custom_admin_site.register(Theme, OnlySuperuserThemeAdmin)
