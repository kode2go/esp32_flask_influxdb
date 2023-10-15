import requests
import random
import time

# Define the URL where you want to send the POST request
# url = 'http://10.0.0.106:5000/flask/rec'
# url = 'http://34.29.140.126/flask/rec'
# url = 'http://34.70.111.2/flask/rec'
# url = 'http://127.0.0.1:5000/flask/rec'
url = 'http://172.30.223.25:5000/flask/rec'
# url = 'http://10.0.0.100:5000/flask/rec'



# Iterate 10,000 times
for _ in range(10000):
    # Generate a new random number
    random_number = random.randint(1, 100)
    
    # Define the data to send in the POST request
    data_to_send = {'data': str(random_number)}
    
    try:
        # Send the POST request        
        response = requests.post(url, data=data_to_send)

        # Check the response
        if response.status_code == 200:
            print(f'POST request with data {random_number} was successful!')
            print('Response content:')
            print(response.text)
        else:
            print(f'POST request with data {random_number} failed with status code:', response.status_code)

    except Exception as e:
        print('An error occurred:', str(e))
    
    # Wait for 1 second before the next iteration
    time.sleep(1)
