import logging
from twilio.rest import Client
from config import settings

def dispatch_emergency_sos(latitude: float, longitude: float, hazard_type: str, severity: str) -> dict:
    maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    message_body = f"🚨 CAMPUS EMERGENCY: {hazard_type} | Severity: {severity} | Location: {maps_url}"
    
    if not settings.TWILIO_ACCOUNT_SID or settings.TWILIO_ACCOUNT_SID == "your_twilio_sid_here":
        logging.warning("Twilio credentials not configured. Logging mock SOS payload.")
        print(f"[MOCK SOS DISPATCH] -> To: {settings.CAMPUS_SAFETY_PHONE} | Body: {message_body}")
        return {"status": "mock_sent", "message": message_body}
    
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=settings.CAMPUS_SAFETY_PHONE
        )
        return {"status": "sent", "sid": message.sid}
    except Exception as e:
        logging.error(f"Failed to send SOS: {e}")
        return {"status": "failed", "error": str(e)}