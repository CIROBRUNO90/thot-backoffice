from django.db.models import Q
from tenant.models import BusinessUnitUser


class BusinessUnitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Obtener las unidades de negocio del usuario
            user_business_units = BusinessUnitUser.objects.filter(
                user=request.user
            ).values_list('business_unit_id', flat=True)

            # Agregar el queryset base a la request para uso posterior
            request.user_business_units = user_business_units

            # Crear un filtro base para usar en los modelos
            request.business_unit_filter = Q(
                business_unit_id__in=user_business_units
            )

        response = self.get_response(request)
        return response
