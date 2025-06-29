from django.shortcuts import render
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.response import Response
from .models import Product,Collection,Review,Cart,CartItem,Customer,Order
from .permissions import IsAdminOrReadOnly,ViewCustomerHistoryPermission
from .permissions import FullDjangoModelPermissions
from .filters import ProductFilter
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer

class ProductViewSet(ModelViewSet):
      

      queryset=Product.objects.all()
      serializer_class=ProductSerializer
      filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
      filterset_class=ProductFilter
      pagination_class=PageNumberPagination
      permission_classes=[IsAdminOrReadOnly]
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
      permission_classes=[IsAdminOrReadOnly]

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
     
     http_method_names=['get','post','patch','delete']

     def get_serializer_class(self):
            
          if self.request.method=='POST':
              return AddCartItemSerializer 
          elif self.request.method=='PATCH':
              return UpdateCartItemSerializer 
          return CartItemSerializer
     
     def get_serializer_context(self):
          return {'cart_id':self.kwargs['cart_pk']}

     def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('cart', 'product')

class CustomerViewSet(ModelViewSet):
      
      queryset=Customer.objects.all()
      serializer_class=CustomerSerializer
      permission_classes=[IsAdminUser]

      
      @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
      def history(self,request,pk):

          return Response('ok') 

      
      @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
      def me(self,request):
        
        customer=Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':   
          serializer=CustomerSerializer(customer)
          return Response(serializer.data) 
        elif request.method=='PUT':
             
             serializer=CustomerSerializer()
             serializer.is_valid(raise_exception=True)
             serializer.save()
             return Response(serializer.data)
      

class OrderViewSet(ModelViewSet):
     

     http_method_names=['get','post','patch','delete','head','options']
     def get_permission(self):

       if self.request.method in ['PATCH','DELETE']:   
          return [IsAdminUser()]
       return [IsAuthenticated()]
     

     def create(self, request, *args, **kwargs):
         
         serializer=CreateOrderSerializer(data=request.data,
                                          context={'user_id': self.request.user.id})
         serializer.is_valid(raise_exception=True)
         order=serializer.save()
         serializer=OrderSerializer(order)
         return Response(serializer.data)

     def get_serializer_class(self):
         if self.request.method == 'POST':

            return CreateOrderSerializer
         elif self.request.method=='PATCH':
              return UpdateOrderSerializer
         return OrderSerializer
         

     def get_queryset(self):

          user=self.request.user

          if user.is_staff:
               return Order.objects.all()
          
          customer_id=Customer.objects.only('id').get(user_id=self.request.user.id)
          return Order.objects.filter(customer_id=customer_id)
          


               
