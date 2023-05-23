
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from .models import Product, Order, OrderItem, BillingAddress, UserProfile, CATEGORIES, DiscountCode, Brand, Comment
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, ContactForm, UserProfileForm, CouponForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import os
from django.conf import settings
from datetime import timedelta
import datetime
from django.db.models import Q
from django.http import Http404


def page_not_found(request):
    return render(request, "404.html", {})


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
        product = Comment.objects.filter(
            product=Product.objects.get(slug=self.kwargs['slug']))
        total_comments = Comment.objects.filter(
            product=Product.objects.get(slug=self.kwargs['slug'])).count()
        context['total_comments'] = total_comments
        context['comments'] = product
        context["images"] = list_of_images
        context['form'] = CommentForm()
        return context

    def post(self, request, slug):
        try:
            product = get_object_or_404(Product, slug=slug)
            user = request.user.userprofile
            if request.method == "POST":
                form = CommentForm(request.POST or None)
                if form.is_valid():
                    text = form.cleaned_data.get('text')
                    time = datetime.datetime.now()
                    form = Comment(
                        product=product,
                        text=text,
                        author=user,
                        time=time
                    )
                    form.save()
                    messages.success(request, "Review submited")
                    return redirect('product-detail', slug=slug)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                # return render(request, 'product-detail.html', {"form": form})
        except:
            messages.info(request, "You must be logged in to give a review")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def update(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        slug = comment.product.slug

        if request.method == "GET":
            if not request.user.is_authenticated:
                return redirect("page-not-found")
            else:
                if comment.author.id == request.user.userprofile.id or request.user.is_staff:
                    product = get_object_or_404(Product, slug=slug)
                    form = CommentForm(instance=comment)
                    comments = Comment.objects.filter(
                        product=Product.objects.get(slug=slug))
                    total_comments = Comment.objects.filter(
                        product=Product.objects.get(slug=slug)).count()
                    a = os.listdir(os.path.join(settings.BASE_DIR,
                                                'static/base/static/catalog/productimages/product'))
                    list_of_images = [
                        a for a in a if product.product_code in a]
                    context = {
                        "object": product,
                        "form": form,
                        "comments": comments,
                        "images": list_of_images,
                        "total_comments": total_comments
                    }
                    return render(request, 'update-comment.html', context)
                else:
                    return redirect("page-not-found")

        if request.method == "POST":
            if not request.user.is_authenticated:
                return redirect("page-not-found")
            else:
                if comment.author.id == request.user.userprofile.id or request.user.is_staff:
                    form = CommentForm(request.POST or None)
                    if form.is_valid():
                        comment.text = form.cleaned_data['text']
                        comment.author = comment.author
                        comment.time = comment.time
                        comment.save()
                        messages.info(request, "Review updated")
                        return redirect("product-detail", slug=slug)
                else:
                    messages.warning(request, "You can edit your own comments")
                    return redirect("product-detail", slug=slug)


def delete_comment(request, pk):
    if not request.user.is_authenticated:
        return redirect("page-not-found")
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "GET":
        if comment.author.id == request.user.userprofile.id or request.user.is_staff:
            comment.delete()
            messages.warning(request, "Review deleted")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.info(request, "You can delete only your own reviews")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProductListView(ListView):
    model = Product
    template_name = "products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        brands = Brand.objects.all()
        context = {
            'products': all_products,
            'brands': brands,
        }
        return context

#### PRODUCT CATEGORIES / NEW ARRIVALS #####


def get_perfumes(request):
    perfume_qs = Product.objects.filter(category="P")
    context = {
        "perfumes": perfume_qs
    }
    return render(request, 'perfumes.html', context)


def get_skincare(request):
    skincare_qs = Product.objects.filter(category="S")
    context = {
        "skincare": skincare_qs
    }
    return render(request, 'skincare.html', context)


def get_makeup(request):
    makeup_qs = Product.objects.filter(category="M")
    context = {
        "makeup": makeup_qs
    }
    return render(request, 'makeup.html', context)


def get_new_perfumes(request):
    perfumes_qs = Product.objects.filter(category="P")
    context = {
        "perfumes": perfumes_qs
    }
    return render(request, 'new-perfumes.html', context)


def get_new_makeup(request):
    makeup_qs = Product.objects.filter(category="M")
    context = {
        "new_makeup": makeup_qs
    }
    return render(request, 'new-makeup.html', context)


def get_new_skincare(request):
    skincare_qs = Product.objects.filter(
        category="S")
    context = {
        "skincare": skincare_qs
    }
    return render(request, 'new-skincare.html', context)

#### \\\\ PRODUCT CATEGORIES / PRODUCT NEW ARRIVALS \\\\ #####

#### SKINCARE SUB CATEGORIES ########


def get_skincare_moisturizers(request):
    moist_qs = Product.objects.filter(
        skincare_category__category="Moisturizer")
    context = {
        "moisturizers": moist_qs
    }
    return render(request, 'moisturizers.html', context)


def get_skincare_masks(request):
    mask_qs = Product.objects.filter(
        skincare_category__category="Mask")
    context = {
        "masks": mask_qs
    }
    return render(request, 'masks.html', context)


def get_skincare_lip_balm(request):
    lipbalm_qs = Product.objects.filter(
        skincare_category__category="Lip Balms & Treatmen")
    context = {
        "lipbalm": lipbalm_qs
    }
    return render(request, 'lip-balm-care.html', context)


def get_skincare_cleanser(request):
    cleanser_qs = Product.objects.filter(
        skincare_category__category="Cleanser")
    context = {
        "cleansers": cleanser_qs
    }
    return render(request, 'cleansers.html', context)
#### \\\\\\SKINCARE SUB CATEGORIES \\\\\\\\\\########

#### MAKEUP SUB CATEGORIES ########


def get_makeup_face(request):
    face_qs = Product.objects.filter(
        makeup_category="F")
    context = {
        "face_makeup": face_qs
    }
    return render(request, 'face-makeup.html', context)


def get_makeup_eye(request):
    makeup_eye_qs = Product.objects.filter(
        makeup_category="E")
    context = {
        "eye_makeup": makeup_eye_qs
    }
    return render(request, 'eye-makeup.html', context)


def get_makeup_lip(request):
    makeup_lip_qs = Product.objects.filter(
        makeup_category="L")
    context = {
        "lip_makeup": makeup_lip_qs
    }
    return render(request, 'lip-makeup.html', context)
#### \\\\\\MAKEUP SUB CATEGORIES\\\\\\ ########


def list_by_male_perfumes(request):
    male_qs = Product.objects.filter(gender='M').exclude(~Q(category="P"))
    return render(request, 'male_perfumes.html', {'m_products': male_qs})


def list_by_female_perfumes(request):
    female_qs = Product.objects.filter(
        gender='F').exclude(~Q(category="P"))
    return render(request, 'female_perfumes.html', {'f_products': female_qs})


def arrange_by_rating_perfumes(request):
    perfumes_qs = Product.objects.filter(
        ratings__isnull=False).exclude(~Q(category="P")).order_by('-ratings__average')
    context = {
        'ratings': perfumes_qs
    }
    return render(request, 'top-perfumes.html', context)


def arrange_by_rating_skincare(request):
    skincare_qs = Product.objects.filter(
        ratings__isnull=False).exclude(~Q(category="S")).order_by('-ratings__average')
    context = {
        'ratings': skincare_qs
    }
    return render(request, 'top-skincare.html', context)


def arrange_by_rating_makeup(request):
    makeup_qs = Product.objects.filter(
        ratings__isnull=False).exclude(~Q(category="M")).order_by('-ratings__average')
    context = {
        'rating_makeup': makeup_qs
    }
    return render(request, 'top-makeup.html', context)


def get_all_new_products(request):
    all_new_products_qs = Product.objects.all()
    context = {
        "new_products": all_new_products_qs
    }
    return render(request, 'new-arrivals.html', context)

### FILTER CATEGORY BY BRAND ###


def get_makeup_by_brand(request, *args, **kwargs):
    brand = Brand.objects.get(slug=kwargs['slug'])
    makeup_product_brand_qs = Product.objects.filter(
        Q(category="M") & Q(brand__brand=brand))
    context = {
        "makeup_brand": makeup_product_brand_qs,
        "brand_name": brand
    }
    return render(request, "makeup-by-brand.html", context)


def get_skincare_by_brand(request, *args, **kwargs):
    brand = Brand.objects.get(slug=kwargs['slug'])
    skincare_product_brand_qs = Product.objects.filter(
        Q(category="S") & Q(brand__brand=brand))
    context = {
        "skincare_brand": skincare_product_brand_qs,
        "brand_name": brand
    }
    return render(request, "skincare-by-brand.html", context)


def get_perfumes_by_brand(request, *args, **kwargs):
    brand = Brand.objects.get(slug=kwargs['slug'])
    perfumes_product_brand_qs = Product.objects.filter(
        Q(category="P") & Q(brand__brand=brand))
    context = {
        "perfumes_brand": perfumes_product_brand_qs,
        "brand_name": brand,
    }
    return render(request, "perfumes-by-brand.html", context)
### \\\\ CATEGORY BRANDS \\\\ ###

### BRANDS BY CATEGORY  ###


def all_brands_s(request):
    brand_qs = Brand.objects.exclude(~Q(product__category="S"))
    return render(request, "brands-by-s.html", {"brands": brand_qs})


def all_brands_p(request):
    brand_qs = Brand.objects.exclude(~Q(product__category="P"))
    return render(request, "brands-by-p.html", {"brands": brand_qs})


def all_brands_m(request):
    brand_qs = Brand.objects.exclude(~Q(product__category="M"))
    return render(request, "brands-by-m.html", {"brands": brand_qs})
### \\\\ BRANDS BY CATEGORY  \\\\ ###

### SALE QUERY ###


def items_on_sale(request):
    items_on_sale_query = Product.objects.filter(sale=True)
    return render(request, 'sale.html', {'items_on_sale': items_on_sale_query})


def perfumes_on_sale(request):
    perfumes_on_sale_query = Product.objects.filter(
        category='P').exclude(sale_price__isnull=True)
    return render(request, 'sale.html', {'items_on_sale': perfumes_on_sale_query})


def makeup_on_sale(request):
    makeup_on_sale_query = Product.objects.filter(
        category='M').exclude(sale_price__isnull=True)
    return render(request, 'sale.html', {'items_on_sale': makeup_on_sale_query})


def skincare_on_sale(request):
    skincare_on_sale_query = Product.objects.filter(
        category='S').exclude(sale_price__isnull=True)
    return render(request, 'sale.html', {'items_on_sale': skincare_on_sale_query})


class BrandView(ListView):
    model = Brand
    template_name = 'brand-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_qs = Brand.objects.all()
        context['brands'] = brand_qs
        return context


class BrandDetail(DetailView):
    model = Brand
    template_name = "brand-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        product_qs = Product.objects.filter(
            brand__brand=brand)
        context['branditems'] = product_qs
        return context


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
def remove_from_favorites(request, slug):
    item = get_object_or_404(Product, slug=slug)
    qs = UserProfile.objects.filter(user=request.user)
    try:
        if UserProfile.objects.get(user=request.user):
            user = UserProfile.objects.get(user=request.user)
            if user.favorites.contains(item):
                user.favorites.remove(item)
                messages.warning(request, f"{item} removed from favorites")
    except:
        return HttpResponse("Woops, something went wrong")
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
                zip = form.cleaned_data.get('zip')
                city = form.cleaned_data.get('city')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    phone_number=phone_number,
                    zip=zip,
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
                        self.request, "Coupon applied")
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.warning(self.request, "This coupon does not exist")
                return redirect('checkout')
