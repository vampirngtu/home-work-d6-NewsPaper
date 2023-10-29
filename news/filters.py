from django_filters import FilterSet 
from django_filters import filters 
from .models import Post, Author
 
 

class PostFilter(FilterSet):
    data = filters.DateFilter (label = "Дата (YYYY-MM-DD)", lookup_expr="gt")
    
    title = filters.CharFilter (label = 'Заголовок', lookup_expr='icontains')
    author = filters.ModelChoiceFilter (label = "Автор",
            queryset = Author.objects.all())
    class Meta:
        model = Post
        fields = ('data', 'title', 'author')