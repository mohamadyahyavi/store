from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.response import Response
from .models import Product,Collection,Review
from .filters import ProductFilter
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer

class ProductViewSet(ModelViewSet):
      

      queryset=Product.objects.all()
      serializer_class=ProductSerializer
      filter_backends=[DjangoFilterBackend]
      filterset_class=ProductFilter
      

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
            


