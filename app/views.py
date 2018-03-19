"""
Definition of views.
"""

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Item, Bid
from app.forms import itemform
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
        return render(request, 'app/create_user.html', {'form': form})




def Items(request):
    nitem = Item.objects.all()
    return render_to_response('app/items.html', {'nitem':nitem})



def Itemdetails(request, id):
	item = Item.objects.get(id=id)
	current_price = item.get_current_bid()
	time_left = item.get_time_left()

	bids_for_item = []
	if request.user.is_superuser:
		bids_for_item = Bid.objects.filter(item=item).order_by('-price', 'created_at')

	if request.method == 'POST':
		if not time_left:
			return redirect('/items/<id>')

		bid_price = request.POST['bid_price']
		try:
			bid_price = float(bid_price)
		except ValueError:
			return render_to_response('app/itemdetails.html', {'item': item, 'current_price': current_price, 'bid_error': True}, context_instance=RequestContext(request))
		if (bid_price <= current_price or not (bid_price*4).is_integer()):
			return render_to_response('app/itemdetails.html', {'item': item, 'current_price': current_price, 'bid_error': True}, context_instance=RequestContext(request))
		if (not request.user.is_authenticated()):
			return redirect('/items/<id>')

		try:
			my_bid = Bid.objects.get(user=request.user, item=item)
			my_bid.price = bid_price
			my_bid.created_at = datetime.now()
			my_bid.save()
		except Bid.DoesNotExist:
			my_bid = Bid.objects.create(user=request.user, item=item, price=bid_price)
		
		current_price = item.get_current_bid()

		return render_to_response('app/itemdetails.html', {
			 
			'item': item,
			'bids_for_item': bids_for_item,
			'current_price': current_price,
			'bid_success': True,
			'beaten': my_bid.price if item.get_winner() != request.user else False
		}, context_instance=RequestContext(request))
	else:
		beaten = False
		try:
			my_bid = Bid.objects.get(user=request.user, item=item)
			beaten = my_bid.price
		except: # Bid.DoesNotExist:
			pass

		winner = None

		if not time_left:
			winner = item.get_winner()

		return render_to_response('app/itemdetails.html', {
			 
			'item': item,
			'bids_for_item': bids_for_item,
			'current_price': current_price,
			'beaten': beaten if item.get_winner() != request.user else False,
			'winner': winner
		}, context_instance=RequestContext(request))

@login_required(redirect_field_name='login', login_url='login/')
def me(request):
		all_items = Item.objects.all()
		winning_items = []
		beaten_items = []
		for item in all_items:
			try:
				Bid.objects.get(user=request.user, item=item)
			except Bid.DoesNotExist:
				continue
			if item.get_winner() == request.user:
				winning_items.append(item)
			else:
				beaten_items.append(item)
		return render(request, 'app/me.html', {
			'winning_items': winning_items,
			'beaten_items': beaten_items
		})



@login_required(redirect_field_name='login', login_url='login/')
def createitem(request):
    if request.method == "POST":
        form= itemform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/items') 

    else:    
        form = itemform()
    return render(request, 'app/create.html', {'form':form})

def home(request):
    """Renders the home page."""

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Any inconvenience contact below:',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
