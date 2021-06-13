from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="the-church-project Api",
        default_version='v1',
        description=
        "The django backend Api Documenation uses REST framework and will not be open for public use.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="leojfrancis.now@gmail.com"),
        license=openapi.License(name="GNU License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
