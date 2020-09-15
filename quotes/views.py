from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm

import os

from .models import Stock

# home view
def home(request):
  import json
  import requests
  iexcloud_apikey = os.getenv('IEXCLOUD_APIKEY')

  if request.method == "POST":
    ticker = request.POST['ticker_symbol']
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker + "/quote?token=" + iexcloud_apikey)
    try:
      api_result = json.loads(api_request.content)
    except Exception as e:
      api_result = "Error..."
    return render(request, 'home.html', {'api_result': api_result})
  else:
    return render(request, 'home.html', {'ticker': "enter a ticker symbol above.."})
  
# about view
def about(request):
  return render(request, 'about.html', {})

# add stock view
def add_stock(request):
  import json
  import requests
  iexcloud_apikey = os.getenv('IEXCLOUD_APIKEY')
  if request.method == "POST":
    ticker = request.POST['ticker']
    add_stock_form = StockForm(request.POST or None)

    if add_stock_form.is_valid():
      add_stock_form.save()
      messages.success(request, ("Stock has been added"))
      return redirect('add_stock')

  else:  
    ticker = Stock.objects.all()
    output = []
    for ticker_item in ticker:
      api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) + "/quote?token=" + iexcloud_apikey)
      try:
        api_result = json.loads(api_request.content)
        output.append(api_result)
      except Exception as e:
        api_result = "Error..."

    return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

# delete stock view
def delete_stock(request, stock_id):
  item = Stock.objects.get(pk=stock_id)
  item.delete()
  messages.success(request, ("Stock has been deleted!"))
  return redirect(delete_stocks)


# delete stocks view
def delete_stocks(request):
  ticker = Stock.objects.all()
  return render(request, 'delete_stocks.html', {'ticker': ticker})
