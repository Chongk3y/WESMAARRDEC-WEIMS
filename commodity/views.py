from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CommodityForm, IecMaterialForm
from cmscore.decorators import secretariat_required

def commodities(request):
    title = "Commodity"
    commodity_list = Commodity.objects.all()
    paginator = Paginator(commodity_list, 4)  # Show 10 commodities per page.
    page_number = request.GET.get('page')
    commodities = paginator.get_page(page_number)

    context = {
        'commodities': commodities,
        'title' : title
    }

    return render(request, 'Commodities.html', context)

def commodity_detail(request, com_id):
    commodity = get_object_or_404(Commodity, com_id=com_id)
    context = {
        'commodity': commodity
    }
    return render(request, 'commodity_detail.html', context)

def view_commodity(request):
    agency_filter = request.GET.get('agency')
    query = request.GET.get('q')
    commodities = Commodity.objects.all()  # Add () here

    if agency_filter:
        agency = CMI.objects.get(name=agency_filter)
        commodities = commodities.filter(cmi_name=agency)
    if query:
        commodities = commodities.filter(
            Q(name__icontains=query) |
            Q(detail__icontains=query)
        )

    paginator = Paginator(commodities, 10)  # Show 10 programs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Commodity Management",
        'page_obj': page_obj,
        'agencies': CMI.objects.all(),
    }

    return render(request, 'view_commodity.html', context)

def add_commodity(request):
    if request.method == 'POST':
        form = CommodityForm(request.POST, request.FILES)
        if form.is_valid():
            commodity = form.save(commit=False)
            commodity.created_by = request.user
            commodity.save()
            return redirect('view_commodity')  # redirect to the consortium view page
    else:
        form = CommodityForm()
    return render(request, 'add_commodity.html', {'form': form})

def edit_commodity(request, com_id):
    commodity = Commodity.objects.get(pk=com_id)
    if request.method == 'POST':
        form = CommodityForm(request.POST, request.FILES, instance=commodity)
        if form.is_valid():
            form.save()
            return redirect('view_commodity')  # redirect to commodity list view
    else:
        form = CommodityForm(instance=commodity)
    return render(request, 'edit_commodity.html', {'form': form, 'commodity': commodity})

@secretariat_required
def delete_commodity(request, com_id):
    commodity = get_object_or_404(Commodity, pk=com_id)
    if request.method == 'POST':
        commodity.delete()
        return redirect('view_commodity')  # Redirect to user list after deletion
    return render(request, 'delete_commodity.html', {'commodity': commodity})

def view_IEC(request):
    query = request.GET.get('q')
    IEC = IecMaterial.objects.all()  # Add () here

    if query:
        IEC = IEC.filter(
            Q(title__icontains=query) |
            Q(iec_type__icontains=query)
        )

    paginator = Paginator(IEC, 10)  # Show 10 programs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "IecMaterial Management",
        'page_obj': page_obj,
    }

    return render(request, 'view_IEC.html', context)

def add_IEC(request):
    if request.method == 'POST':
        form = IecMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            IEC = form.save(commit=False)
            IEC.created_by = request.user
            IEC.save()
            return redirect('view_IEC')
    else:
        form = IecMaterialForm()
    return render(request, 'add_IEC.html', {'form': form})

def edit_IEC(request, iec_id):
    IEC = IecMaterial.objects.get(pk=iec_id)
    if request.method == 'POST':
        form = IecMaterialForm(request.POST, request.FILES, instance=IEC)
        if form.is_valid():
            form.save()
            return redirect('view_IEC')  # redirect to commodity list view
    else:
        form = IecMaterialForm(instance=IEC)
    return render(request, 'edit_IEC.html', {'form': form, 'IEC': IEC})

@secretariat_required
def delete_IEC(request, iec_id):
    IEC = IecMaterial.objects.get(pk=iec_id)
    if request.method == 'POST':
        IEC.delete()
        return redirect('view_IEC')  # Redirect to user list after deletion
    return render(request, 'delete_IEC.html', {'IEC': IEC})

