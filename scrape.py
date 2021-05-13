import requests
import datetime
import time
import threading
import send_email

PINCODES = [700061, 700063, 700034] # use comma to separate pincodes
PAYMENT_MODE = 'Free' # available values: Free, Paid
AGE_LIMIT = 18 # available values: 18, 45


def fetch_data(params):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }    
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin', params=params, headers=headers, timeout=5)
    return response


def scrape(start_date, end_date, pincode):
    
    params = {
        'pincode': pincode,
        'date': start_date
    }
    time.sleep(1)
    source = fetch_data(params)
    
    if source.status_code != 200:
        print('Error occurred')
    else:
        response = source.json()
        if not response:
            print('No result found')
            return True

        date_range = start_date + ' ~ ' + end_date
        for item in response['centers']:
            if item['fee_type'] == PAYMENT_MODE:
                email_data  = f"{item['name'].upper()}\n"
                email_data += f"Address: {item['address']} \n{item['district_name']}: {item['pincode']}\n"
                email_data += f"Date: {date_range}"
                
                for data in item['sessions']:
                    if data['min_age_limit'] == AGE_LIMIT and data['available_capacity'] > 0:
                        send_email.send_email_to_user(email_data, date_range)
                        print('Email sent successfully.')
                        break
    return True

if __name__ == '__main__':
    start = time.perf_counter()
    
    threads = []
    
    for pincode in PINCODES:
        start_day = 0
        for _ in range(4):
            if start_day == 0:
                dt = datetime.datetime.now()
                end_dt = datetime.datetime.now() + datetime.timedelta(days=(start_day+6))
                start_day += 7
            else:            
                dt = datetime.datetime.now() + datetime.timedelta(days=start_day)
                end_dt = datetime.datetime.now() + datetime.timedelta(days=(start_day+6))
                start_day += 7
            
            start_dt = "%02d-%02d-%d" % (dt.day, dt.month, dt.year)
            end_dt = "%02d-%02d-%d" % (end_dt.day,end_dt.month,end_dt.year)
            
            t = threading.Thread(target=scrape, args=[start_dt, end_dt, pincode])
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
        

    finish = time.perf_counter()
    print(f'finished in {round(finish - start, 5)} second(s)')