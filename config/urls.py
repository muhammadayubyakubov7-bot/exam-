from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from book.views import BookViewSet
from reviews.views import BookReviewListCreateAPIView, ReviewListAPIView, ReviewViewSet
from users.views import LoginAPIView, RegisterAPIView
from book.views import home

schema_view = get_schema_view(
    openapi.Info(title='Book Review API', default_version='1.0', description='Kitoblar va sharhlar API'),
    public=True,
    permission_classes=[],
)

router = DefaultRouter()
router.register('books', BookViewSet, basename='api-books')
router.register('reviews', ReviewViewSet, basename='api-reviews')

urlpatterns = [
    path('', home, name='home'),
    path('books/', include('book.urls')),
    path('users/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('admin-dashboard/', include('admin_dashboard.urls')),
    path('api/books/<int:book_id>/reviews/', BookReviewListCreateAPIView.as_view(), name='api_book_reviews'),
    path('api/reviews/all/', ReviewListAPIView.as_view(), name='api_reviews_all'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='api_auth_register'),
    path('api/auth/login/', LoginAPIView.as_view(), name='api_auth_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='api_auth_refresh'),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
