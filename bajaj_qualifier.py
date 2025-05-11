import requests

url_generate_webhook = 'https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON'
data = {
    "name": "Aadish Sanghvi",
    "regNo": "0827CS221002",
    "email": "aadishsanghvi220704@acropolis.in"
}

response = requests.post(url_generate_webhook, json=data)
response.raise_for_status()  
response_data = response.json()

webhook_url = response_data.get("webhook")
access_token = response_data.get("accessToken")

if not webhook_url or not access_token:
    print("Error: Webhook URL or Access Token missing.")
    exit(1)

print("Webhook URL:", webhook_url)
print("Access Token:", access_token)

reg_no_last_digit = int(data["regNo"][-1])
question_url = "https://drive.google.com/file/d/1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY/view?usp=sharing" if reg_no_last_digit % 2 == 1 else "https://drive.google.com/file/d/1PO1ZvmDqAZJv77XRYsVben11Wp2HVb/view?usp=sharing"

print("SQL Question URL:", question_url)


sql_query = """SELECT 
  e1.emp_id,
  e1.first_name,
  e1.last_name,
  d.department_name,
  (SELECT COUNT(*) 
   FROM employee e2 
   WHERE e2.department = e1.department 
   AND e2.DOB > e1.DOB) AS YOUNGER_EMPLOYEES_COUNT
FROM employee e1
JOIN department d ON e1.department = d.department_id
ORDER BY e1.emp_id DESC;"""  

url_submit_query = 'https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON'
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submission_data = {
    "finalQuery": sql_query
}

response_submit = requests.post(url_submit_query, headers=headers, json=submission_data)
response_submit.raise_for_status()  
print("Submission Response:", response_submit.text)
