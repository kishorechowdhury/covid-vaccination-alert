# COVID vaccination alert
Simple COVID vaccination alert. Check if any slots available in your locality and get email notification right away.

# Usage

1. install python
2. run pip install -r requirements.txt to install necessary packages.
3. configure 'send_email.py'
4. at the top in 'scrape.py' and set the following params:

   a. PINCODES 
   
   b. PAYMENT_MODE
   
   c. AGE_LIMIT
	 
5. run 'scrape.py' file
6. Optionally, to periodically check if any slots available in the given pincodes.

   a. create a task scheduler on windows. For reference follow this <a href="https://datatofish.com/python-script-windows-scheduler/">link</a>
 
For any queries, feel free to drop me an email at kishore.chowdhuri@gmail.com
