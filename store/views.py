from django.shortcuts import render
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.response import Response
from .models import Product,Collection,Review,Cart,CartItem
from .filters import ProductFilter
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer

class ProductViewSet(ModelViewSet):
      

      queryset=Product.objects.all()
      serializer_class=ProductSerializer
      filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
      filterset_class=ProductFilter
      pagination_class=PageNumberPagination
      search_fields=['title','description']
      ordering_fields=['unit_price','last_update']
      

      def get_serializer_context(self):
           return {'request':self.request}
      
      def destroy(self, request, *args, **kwargs):
           
           if orderitem.objects.filter(product_id=kwargs['pk']).count() > 0:
                return Response({'error':'Product cannot be deleted'})
           return super().destroy(request, *args, **kwargs)
           

class CollectionViewSet(ModelViewSet):
     
      queryset= Collection.objects.annotate(
           
           products_count=Count('products')).all()
      serializer_class=CollectionSerializer

      def delete(self,request,pk):
           collection=Collection.objects.get(pk=pk)
           if collection.products.count() > 0:
                return Response({'error':'collection cannot be deleted'})
           
           collection.delete()
           return Response('deleted')
      

class ReviewViewSet(ModelViewSet):
     
      queryset=Review.objects.all()
      serializer_class=ReviewSerializer
      def get_queryset(self):
           
           return Review.objects.filter(product_id=self.kwargs['product_pk'])


      def get_serializer_context(self):
           return {'product_id': self.kwargs['product_pk']}
            

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
      
      queryset=Cart.objects.prefetch_related('items__product').all()
      serializer_class=CartSerializer

class CartItemViewSet(ModelViewSet):

    serializer_class=CartItemSerializer
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']) \
        .select_related('product')      


