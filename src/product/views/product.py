from django.views import generic

from product.models import Variant

from django.shortcuts import render
from ..models import Product
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.core.paginator import Paginator

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context




class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = self.get_queryset()
        paginator = Paginator(all_products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        total_products = all_products.count()

        # Calculate page range for pagination boxes
        current_page = page_obj.number
        max_page = paginator.num_pages
        left = max(current_page - 2, 1)
        right = min(current_page + 2, max_page)

        page_range = range(left, right+1)

        context.update({
            'page_obj': page_obj,
            'total_products': total_products,
            'page_range': page_range,
        })
        return context