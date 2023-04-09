
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from .models import Product, Order, OrderItem, BillingAddress, UserProfile, CATEGORIES, DiscountCode
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, ContactForm, UserProfileForm, CouponForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import os
from django.conf import settings


class ProductDetailView(DetailView):
    model = Product
    template_name = "product-detail.html"

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = os.listdir(os.path.join(settings.BASE_DIR,
                                    'static/base/static/catalog/productimages/product'))
        item = Product.objects.get(slug=self.kwargs['slug'])
        list_of_images = [a for a in a if item.product_code in a]
        context["images"] = list_of_images
        return context


class ProductListView(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()

    def list_by_male_products(self):
        pass

    def list_by_female_products(self):
        # Filter female products only
        pass


class IndexPageView(ListView):
    model = Product
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = []
        for item in CATEGORIES:
            categories.append(item[1])
        context["category"] = categories
        return context


class OrderSummaryView(LoginRequiredMixin, View):

    template_name = "order_summary.html"

    def get(self, request, *args):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if len(order.items.all()) == 0:
                return render(self.request, 'empty-cart.html')
        except ObjectDoesNotExist:
            messages.warning(request, "You have no active orders")
        return render(self.request, 'order_summary.html', {"object": order})


@login_required
def empty_cart(request):
    return render(request, 'empty-cart')


@login_required
# TO DO: CHECK IF ITEM IS IN FAVORITES AND THEN CHANGE HTTP ICON COLOR ACORDINGLY
def add_to_favorites(request, slug):
    item = get_object_or_404(Product, slug=slug)
    qs = UserProfile.objects.filter(user=request.user)
    print(qs.all())
    try:
        if UserProfile.objects.get(user=request.user):
            user = UserProfile.objects.get(user=request.user)
            if user.favorites.contains(item):
                user.favorites.remove(item)
                messages.warning(request, f"{item} removed from favorites")
            else:
                user.favorites.add(item)
                messages.success(request, f"{item} added to favorites")
    except:
        return HttpResponse("You must be logged in")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def show_favorites(request):
    qs = UserProfile.objects.get(user=request.user)
    favorites = qs.favorites.all()
    return render(request, "favorites.html", {"favorites": favorites})


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
            messages.info(request, f"{item} quantity updated")
        else:
            order.items.add(order_item)
            messages.success(request, f"{item} added to cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, f"{item} added to cart")
    return redirect('order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order_item.delete()
            if len(order.items.all()) == 0:
                # TODO: REDIRECT TO EMPRYT CART PAGE
                messages.info(request, "Cart is empty")
            messages.info(request, f"{item} removed from cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, f"{item} was not in your cart")
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
                    # TODO:  REDIRECT TO EMPTY CART
                    messages.info(request, "Your cart is empty")
                    print("CART IS EMPTY")
                messages.info(request, f"{item} removed from cart")
                return redirect('order-summary')
            else:
                order_item.save()
                messages.info(request, f"{item} quantity updated")
                return redirect('order-summary')
        else:
            return redirect('product-detail', slug=slug)
    else:
        messages.warning(request, "Cart is empty")
        return redirect('order-summary')


class CheckoutView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            if order.get_total_price() <= 0:
                messages.info(self.request, "You must have active order")
                return redirect('product-list')
        except ObjectDoesNotExist:
            messages.info(self.request, "You must have active order")
            return redirect('product-list')
        try:
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                'couponform': CouponForm(),
            }
            return render(self.request, 'checkout.html', context=context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You have no active orders")
            return redirect('checkout')

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
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You have no active orders")
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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    context_object_name = 'profile'
    template_name = 'profile-details.html'

    def get_object(self, *args, **kwargs):
        return UserProfile.objects.get(user=self.request.user.id)


@login_required
def update_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.email = form.cleaned_data['email']
            profile.address = form.cleaned_data['address']
            profile.city = form.cleaned_data['city']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()
            print(profile.phone_number)
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile-update.html', {"form": form})


def get_coupon(request, code):
    coupon = DiscountCode.objects.get(code=code)
    return coupon


class CouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data['code']
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                coupon = get_coupon(self.request, code)
                if order.coupon:
                    messages.info(self.request, "A coupon is already active")
                else:
                    order.coupon = coupon
                    order.save()
                    messages.success(
                        self.request, "Successfully applied coupon")
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.warning(self.request, "This coupon does not exist")
                return redirect('checkout')
