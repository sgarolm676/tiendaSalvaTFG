from django.urls import path
from . import views


urlpatterns = [
    path('listado/', views.ListadoView.as_view(), name='listado'),
    path('listado/add/', views.CreateProductoView.as_view(), name='add_product'),
    path('listado/<pk>/edit', views.UpdateProductoView.as_view(), name='edit_product'),
    path('listado/<pk>/delete', views.DeleteProductoView.as_view(), name='delete_product'),
    path('compra', views.ComprarView.as_view(), name='compra'),
    path('checkout/<int:id>', views.CheckoutView.as_view(), name='checkout'),
    path('valoracion_add/<pk>', views.CreateValoracion.as_view(), name='add_valoracion'),
    path('valoracion_update/<pk>', views.UpdateValoracion.as_view(), name='update_valoracion'),
    path('valoracion_delete/<pk>', views.DeleteValoracion.as_view(), name='delete_valoracion'),
    path('informe', views.InformeView.as_view(), name='informe_index'),
    path('informe/marca', views.FiltradoPorMarcasView.as_view(), name='filtrar_marcas'),
    path('informe/top_diez_productos', views.TopDiezProductosComprasView.as_view(), name='top_diez_productos'),
    path('informe/top_diez_clientes', views.TopDiezClientesComprasView.as_view(), name='top_diez_clientes'),
    path('informe/compras_cliente', views.FiltradoComprasView.as_view(), name='compras_cliente'),
    path('informe/compras_cliente/<pk>/detail', views.CompraDetail.as_view(), name='compras_cliente_detail'),
    path('carrito/<pk>', views.CarritoView.as_view(), name='carrito'),
    path('carrito', views.CarritoView.as_view(), name='carrito'),
    path('carrito_delete/<pk>', views.RemoveCarritoView.as_view(), name='carrito delete'),
    path('carrito_update/<pk>', views.UpdateCarritoView.as_view(), name='carrito update'),
    path('carrito_checkout', views.CheckoutCarrito.as_view(), name='carrito checkout'),
]
