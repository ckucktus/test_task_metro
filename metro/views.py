from rest_framework import generics, request
from rest_framework.exceptions import ParseError, NotFound
from metro.serializers import MetroDetailSerializer
from metro.models import Metro
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

#Кастомный фильтр класс для реализации поиска
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class GetStation(generics.RetrieveAPIView):
    serializer_class = MetroDetailSerializer
    def get_object(self, pk):
        
        try:
            return Metro.objects.get(pk=pk)
        except Metro.DoesNotExist:
            raise NotFound({'error':'id does not exist'})

    def get(self, request, pk, format=None):
        stocks = self.get_object(pk)
        serializer = MetroDetailSerializer(stocks)
        return Response(serializer.data)


class GetListStations(generics.ListAPIView):
    serializer_class = MetroDetailSerializer
    def get_queryset(self):
        page = int(self.kwargs['page'])
        limit = int(self.kwargs['limit'])
        if limit > 20:
             raise ParseError({'error':'Limit excedeed'})
        if page == 0:
            raise ParseError({'error':'Page numbering starts from 1'})
        elif page==1:
            self.queryset = Metro.objects.all().order_by('station')[1:limit]
        else:
            self.queryset = Metro.objects.all().order_by('station')[(page-1)*20:(page-1)*20+limit]

        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MetroDetailSerializer(queryset, many=True)

        return Response({'data':  serializer.data})

class AddStation(generics.CreateAPIView):
    serializer_class = MetroDetailSerializer
    

class DeleteStation(generics.DestroyAPIView):
    serializer_class = MetroDetailSerializer
    def get_object(self, pk):
        try:
            return Metro.objects.get(pk=pk) 
        except Metro.DoesNotExist:
            raise NotFound({'error':'Station not found'})

    def get(self, request, pk, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

class SearchStation(generics.ListAPIView):
    serializer_class = MetroDetailSerializer
    queryset = Metro.objects.all()
    search_fields = ['id' , 'station', 'line', 'admarea', 'district', 'status', 'ID']
    filter_backends = (DynamicSearchFilter,)

