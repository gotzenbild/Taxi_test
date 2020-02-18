from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.urls import reverse
from main.forms import OrderForm, LoginForm
from main.models import Order, Car
from django.core.paginator import Paginator


def order_view(request):
    # Рендерит главную страницу, с формой для заказа, и входа в аккаунт диспетчера
    order_form = OrderForm(request.POST or None)
    login_form = LoginForm(request.GET or None)
    context = {
        'order_form': order_form,
        'login_form': login_form
    }
    if order_form.is_valid():
        client_name = order_form.cleaned_data['client_name']
        client_phone = order_form.cleaned_data['client_phone']
        address = order_form.cleaned_data['address']
        destination = order_form.cleaned_data['destination']
        desired_time = order_form.cleaned_data['desired_time']
        new_order = Order(client_name=client_name,
                          client_phone=client_phone,
                          address=address,
                          destination=destination,
                          desired_time=desired_time)
        try:
            car = Car.objects.filter(ordered=False)[0]
            new_order.car = car
            new_order.save()
            car.ordered = True
            car.save()
            order_inf = {"order_id": new_order.id, "car_brand": car.brand}
        except:
            order_inf = False

        context.update({'order_inf': order_inf})

    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('all_orders'))

    return render(request, 'order.html', context)


def all_order_view(request):
    # выводит все заказы деспетчеру
    if request.user.is_authenticated:
        orders = Order.objects.all()
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'all_orders.html', {'page_obj': page_obj})
    else:
        return HttpResponseRedirect(reverse('order'))


def details_view(request, order_id):
    # выводит детали заказа
    try:
        order = Order.objects.get(id=order_id)
        context = {"order": order}
        return render(request, 'details.html', context)
    except:
        raise Http404("No car matches the given query")


def back_to_ordered_false(car_id):
    # возвразает машину в пул свободных по id
    try:
        car = Car.objects.get(id=car_id)
        car.ordered = False
        car.save()
    except:
        raise Http404("No car matches the given query")


def delete_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        car = Car.objects.get(id=order.car.id)
        car.ordered = False
        car.save()
        order.delete()
        return HttpResponseRedirect(reverse('all_orders'))
    except:
        raise Http404("No car matches the given query")