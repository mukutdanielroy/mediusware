from django.views import generic

from product.models import Variant, ProductVariant

from django.shortcuts import render
from ..models import Product
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q

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

        # Apply filters based on search criteria
        title = self.request.GET.get('title')
        variant_id = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_min')
        price_to = self.request.GET.get('price_max')
        date = self.request.GET.get('date_min')

        # Construct query based on form inputs
        products = Product.objects.all()
        if title:
            products = products.filter(title__icontains=title)
        if variant_id:
            products = products.filter(Q(productvariant__variant__id=variant_id))
        if price_from and price_to:
            products = products.filter(productvariant__productvariantprice__price__range=(price_from, price_to))
        if date:
            products = products.filter(created_at__date=date)

        variants = Variant.objects.prefetch_related(
            Prefetch('productvariant_set', queryset=ProductVariant.objects.all().order_by('variant'))
        ).all()

        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        total_products = products.count()

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
            'variants': variants,
        })
        return context