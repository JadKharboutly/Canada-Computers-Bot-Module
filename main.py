import requests
import time
from bs4 import BeautifulSoup as bs
import emoji
import webhooks

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    # 'Cookie':'hc_accessibility=4DruEMuVo77TZDV2k5GzSb29NxC2yk5rWpbNMADN2u1J4Vl/LKOPhVdPqoi9DLCwZHRRKBhaXZuqxOzl/m32oYakpPRT1kJxY1irYQ5l/7c8UVH7HLNSbNVprI+pbVWwuY8yQrz5OKt5hyyvk0V4v/ZOnMvivQt4CgGDID78kq64KRjWojUbRrQXBIssxZ6yNNGfD/M/hy1MZ2qzNLA8z/1luRkRyi7SSZRSncf39dyirWl9e+KdPyVbT8J1YEu6FkEpYF6uFWhbQQt5I82L7eKbzCtCFMLfl2SkZ4BhNeSR3Ue7AUA3sNDCaQnVxorJbUQ0Gxa0nbEwUupZf983PCzBuo0Kjua7m496dqQSrkKBkyb0YsXsNaOI/1mKe/VBq260vRRCOzEDZx/QNHBxzVUlmLs3JAZ268mI33+nJHELitzHnZy8jQ5FjR+aStudWMG0Z0n5JXCIHZN5I5sHQv8rWkjZnvA/d+LZ0mcLqXPocIVUDTQ+9E0xqNxxvZlS/zbA1KzimGk=Oe87tGUmNiC58qqO;'
}


print(time.strftime('[%I:%M:%S]')+' Task Started')


with requests.session() as s:
#Login
    login_url = 'https://www.canadacomputers.com/login.php'
    login_info = {
        'lo-type': 'regular_customer',
        'lo-username': 'kharbouj@mcmaster.ca',
        'lo-password': 'MOONjado203',
        'login':''

    }
    login = s.post(login_url, headers=headers, data=login_info)
    if login.url == 'https://www.canadacomputers.com/account.php':
        print(time.strftime('[%I:%M:%S]') + ' Successfully logged in!')
    else:
        print(time.strftime('[%I:%M:%S]') + ' Login Failed!')
    # for cookie in login.cookies:
    #     headers['Cookie'] += '{}={};'.format(cookie.name,cookie.value)
#Add to Cart
    atc_url = 'https://www.canadacomputers.com/shopping_cart.php?action=bundle_add_to_cart&item0=138042&qty0=1' #Product Url
    atc = s.post(atc_url, headers=headers)
    # for cookie in atc.cookies:
    #     headers['Cookie'] += '{}={};'.format(cookie.name, cookie.value)

#Check Cart
    '''cart_url = 'https://www.canadacomputers.com/shopping_cart.php'
    cart = s.get(cart_url, headers=headers)
    print(time.strftime('[%I:%M:%S]') + ' Added to Cart')'''

#Checkout Method
    ch_url = 'https://www.canadacomputers.com/checkout_method.php'
    ch = s.get(ch_url, headers=headers)
    # for cookie in ch.cookies:
    #     headers['Cookie'] += '{}={};'.format(cookie.name, cookie.value)
    print(ch.url)
#Shipping
    shipping_url = 'https://www.canadacomputers.com/checkout_shipping.php'
    storeList = {}
    selectedStore = []
    # my_stores = ['Oakville','Mississauga','Burlington','Etobicoke','Hamilton','Brampton']
    store_stock = s.get(shipping_url, headers=headers)
    print(store_stock.url)
    stock_soup = bs(store_stock.content,'lxml')
    stores = stock_soup.find_all('input', attrs={'class':'form-check-input', 'type':'radio','name':'ch-depot'})
    for i in range(len(stores)):
        storeList[(stores[i]['data-store-name'])] = (stores[i]['id'])
        selectedStore.append(stores[i]['id'])
    print(selectedStore[0])
    shipping_info = {

    'ch-method': 'pickup',
    'ch-depot': selectedStore[0], #Store ID
    'checkout_shipping':''

    }
    shipping = s.post(shipping_url, headers=headers, data=shipping_info )
    print(time.strftime('[%I:%M:%S]') +' Submitting Shipping')
    print(shipping.url)
    # for cookie in shipping.cookies:
    #     headers['Cookie'] += '{}={};'.format(cookie.name, cookie.value)


#Checkout Payment

    payment_info = {
    'ch-methodofpayment': 'pay_instore',
    'ch-frm-flexiticard-number': '',
    'ch-frm-paymentcontact-areacode': '333',
    'ch-frm-paymentcontact-phone-three': '333',
    'ch-frm-paymentcontact-phone-four': '3333',
    'ch-frm-paymentcontact-ext': '',
    'ch-frm-paymentcontact-email': 'email@@gmail.com',
    'ch-frm-paymentcontact-verify-firstname': 'name',
    'ch-frm-paymentcontact-verify-lastname': 'lastName',
    'ch-frm-paymentcontact-verify-address-autocomplete': 'address',
    'ch-frm-paymentcontact-verify-address': 'address',
    'ch-frm-paymentcontact-verify-street-number': '3333',
    'ch-frm-paymentcontact-verify-street-name': '222',
    'ch-frm-paymentcontact-verify-suburb': 'Oakville',
    'ch-frm-paymentcontact-verify-postal': 'postalCode',
    'ch-frm-paymentcontact-verify-city': 'Oakville',
    'ch-frm-paymentcontact-verify-province': 'ON',
    'ch-frm-paymentcontact-verify-country': 'Canada',
    # 'ch-frm-paymentcontact-card-number': '3333', ## Added for gpu restock (NEW)
    # 'ch-frm-paymentcontact-card-holder': '3333', ## Added for gpu restock (NEW)
    'checkout_payment': ''
    }
    payment_url = 'https://www.canadacomputers.com/checkout_payment.php'
    payment = s.post(payment_url, headers=headers, data=payment_info)
    print(time.strftime('[%I:%M:%S]') + ' Submitting Payment')
    print(payment.url)


#Submit Order

    status = 0
    submitorder_info = {
        'ch_shippingtnc': 'agree',
        'checkout_confirmation': '',

    }
    confirmation_url = 'https://www.canadacomputers.com/checkout_confirmation.php'
    confirmation = s.post(confirmation_url, headers=headers, data=submitorder_info)
    print(confirmation.url)
    if 'success' in str(confirmation.url):
        print(time.strftime('[%I:%M:%S]') + 'Order Placed')
        status = 1

    else:
        print(time.strftime('[%I:%M:%S]') + 'Checkout Failed')
        status = 0




