import hmac
import hashlib
import json

secret = "sk_test_mock_secret_key_12345"
# Change this UUID to an active RESERVED ticket ID from the database
ticket_uuid = "YOUR_TICKET_UUID_HERE" 

payload = {
    "event": "charge.success",
    "data": {
        "amount": 5000,
        "currency": "NGN",
        "metadata": {
            "ticket_id": ticket_uuid
        }
    }
}

body = json.dumps(payload)
signature = hmac.new(bytes(secret, 'utf-8'), msg=bytes(body, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

print("--- COPY THIS FOR POSTMAN ---")
print(f"X-Paystack-Signature: {signature}")
print("\n--- RAW JSON BODY ---")
print(body)