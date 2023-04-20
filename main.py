from fastapi import FastAPI

from utils import generate_possible_emails, validate_emails_non_blocking

app = FastAPI()


def root():
    return {"message": "Hello World"}


@app.get("/generate_and_validate_emails")
async def generate_and_validate_emails(first_name: str, last_name: str, domain: str):
    # Generates and validates mails by first, last names and domain
    possible_emails = generate_possible_emails(first_name, last_name, domain)
    validation_result = await validate_emails_non_blocking(possible_emails)

    return {'status': 'success', 'results': validation_result}


@app.post('/validate_emails')
async def validate_emails(emails: list[str]):
    # Gets list of mails in POST request body, validates it's and returns response
    validation_result = await validate_emails_non_blocking(emails)

    return {'status': 'success', 'results': validation_result}
