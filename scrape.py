import requests
import datetime
import time
import send_email

def fetch_data(params):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }    
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin', params=params, headers=headers, timeout=5)
    # print(resp.url)
    return response


def scrape(start_date, end_date, pincode, PAYMENT_MODE, AGE_LIMIT):

    params = {
        'pincode': pincode,
        'date': start_date
    }
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
                email_sent = False
                for data in item['sessions']:
                    if email_sent:
                        break
                    if data['min_age_limit'] == AGE_LIMIT and data['available_capacity'] > 0 and email_sent == False:
                        email_data += f"Date: {date_range}"
                        send_email.send_email_to_user(email_data, date_range)
                        email_sent = True
                        print('Email sent successfully.')


def preprocess(pincodes, PAYMENT_MODE, AGE_LIMIT):
    
    #fetch data for 4 weeks
    for pincode in pincodes:
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
            scrape(start_dt, end_dt, pincode, PAYMENT_MODE, AGE_LIMIT)
            time.sleep(2)

    return True


if __name__ == '__main__':
    pincodes = [700061, 700063, 700034] # use comma to separate pincodes
    PAYMENT_MODE = 'Free' # available values: Free, Paid
    AGE_LIMIT = 18 # available values: 18, 45
    print('Execution starts')
    preprocess(pincodes, PAYMENT_MODE, AGE_LIMIT)
    print('Execution finished.')
    