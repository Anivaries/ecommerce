
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from .models import Product, Order, OrderItem, BillingAddress, UserProfile
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, ContactForm
from django.http import HttpResponseRedirect, HttpResponse


class ProductDetailView(DetailView):
    model = Product
    template_name = "product-detail.html"

    def get_queryset(self):
        return super().get_queryset()


class ProductListView(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()

    def list_by_male_products(self):
        # Filter male products only
        pass

    def list_by_female_products(self):
        # Filter female products only
        pass


class OrderSummaryView(LoginRequiredMixin, View):

    template_name = "order_summary.html"

    def get(self, request, *args):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            # TO DO ; ERROR - no order, add message
            return redirect("/")
        return render(self.request, 'order_summary.html', {"object": order})


@login_required
# TO DO: CHECK IF ITEM IS IN FAVORITES AND THEN CHANGE ICON COLOR ACORDINGLY
def add_to_favorites(request, slug):
    item = get_object_or_404(Product, slug=slug)
    qs = UserProfile.objects.filter(user=request.user)
    # print(qs[0].favorites.count())
    try:
        if UserProfile.objects.get(user=request.user):
            user = UserProfile.objects.get(user=request.user)
            if user.favorites.contains(item):
                print(f'{item} YES')
                user.favorites.remove(item)
                # TO DO: ADD MESSAGE - ITEM REMOVE FROM FAVORITES
                print(f'{item} NO')
                print(qs[0].favorites.count())
            else:
                user.favorites.add(item)
                print(qs[0].favorites.count())
                # TO DO: ADD MESSAGE - ITEM ADDED TO FAVORITES
                print(f'{item} YES')
            print(item)
            print(UserProfile.objects.get(user=request.user))
    except:
        return HttpResponse("You must be logged in")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, ordered = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            print("ITEM QUANTITY UPDATED")
            # TO DO Message to update cart item
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # print(len(order))
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order_item.delete()
            if len(order.items.all()) == 0:
                # TO DO MESSAGE CART IS EMPTY
                print("CART IS EMPTY")
            print("ITEM DELETED")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # TO DO Message to remove cart item
        else:
            print("This item was not in your cart")
            return redirect('product-detail', slug=slug)
    return redirect('order-summary')


@login_required
def remove_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order_item.quantity -= 1
            if order_item.quantity == 0:
                order_item.delete()
                if len(order.items.all()) == 0:
                    # TO DO MESSAGE CART IS EMPTY
                    print("CART IS EMPTY")
                # order.items.remove(order_item)
                # TO DO: Print message item removed from cart
                print("MESSAGE DA JE REMOVED IZ CARTA")
                return redirect('order-summary')
            else:
                order_item.save()
                # TO DO: Print message item quantity updated
                print("Item quantity updated")
                return redirect('order-summary')
            # TO DO Message to update cart item
        else:
            return redirect('product-detail', slug=slug)
    else:
        print("THE CART IS EMPTY")
        return redirect('order-summary')


class CheckoutView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context=context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                phone_number = form.cleaned_data.get('phone_number')
                zip_code = form.cleaned_data.get('zip')
                city = form.cleaned_data.get('city')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    phone_number=phone_number,
                    zip_code=zip_code,
                    city=city
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
            # print(form.cleaned_data)
            return redirect('checkout')
        except ObjectDoesNotExist:
            # TO DO ; ERROR - no order, add message
            return redirect('checkout')


def contact_form(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # TO DO: Send email to admin
        # TO DO: REDIRECT TO SUCCESS MESSAGE
        return redirect('product-list')
    return render(request, 'contact.html', {"form": form})
