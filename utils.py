import asyncio
import concurrent
import os

import validate_email

SHOULD_LOG_SMTP = os.getenv('LOG_SMTP') == '1'  # Debug flag. If True than all SMTP request would be logged.


def generate_possible_emails(first_name: str, last_name: str, domain: str) -> list:
    """Used for generating mails inside microservice. Now, all mails being generated on client. not here"""
    return [f'{first_name.lower()}.{last_name.lower()}@{domain}',
            f'{last_name.lower()}.{first_name.lower()}@{domain}',
            f'{first_name.lower()[0]}.{last_name.lower()}@{domain}',
            f'{last_name.lower()}.{first_name.lower()[0]}@{domain}',
            f'{last_name.lower()[0]}{first_name.lower()[0]}@{domain}',
            f'{first_name.lower()[0]}{last_name.lower()}@{domain}',
            f'{first_name.lower()}@{domain}',
            f'{last_name.lower()}@{domain}',
            f'{first_name.lower()[0]}_{last_name.lower()}@{domain}',
            f'{first_name.lower()[:2]}{last_name.lower()[:3]}@{domain}',
            f'{first_name.lower()}{last_name.lower()}@{domain}',
            f'{first_name.lower()}_{last_name.lower()}@{domain}',
            f'{last_name.lower()}_{first_name.lower()}@{domain}',
            f'{last_name.lower()}_{first_name.lower()}@{domain}',
            f'{last_name.lower()}{first_name.lower()[0]}@{domain}',
            f'{last_name.lower()[0]}{first_name.lower()}@{domain}',
            f'{first_name.lower()}{last_name.lower()[0]}@{domain}',
            f'{first_name.lower()[:3]}{last_name.lower()[:3]}@{domain}',
            f'{last_name.lower()[:3]}{first_name.lower()[:3]}@{domain}',
            f'iam.{first_name.lower()}{last_name.lower()}@{domain}',
            f'iam.{last_name.lower()}{first_name.lower()}@{domain}']


def _blocking_validation(possible_email: str) -> tuple[str, bool]:
    """Blocking mail validation function that uses py3-validate-email library"""
    is_valid = validate_email.validate_email(possible_email, smtp_debug=SHOULD_LOG_SMTP,
                                             smtp_from_address='support@salestech.pro',
                                             # smtp_helo_host='mail-v.salestech.pro')
                                             )
    return possible_email, is_valid


async def validate_emails_non_blocking(possible_emails):
    """Calls blocking function _blocking_validation in executor, so it runs in non-blocking way."""
    loop = asyncio.get_running_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=25)

    done, pending = await asyncio.wait(
        fs=[loop.run_in_executor(executor, _blocking_validation, email) for email in possible_emails],
        return_when=asyncio.ALL_COMPLETED
    )

    validation_results = [task.result() for task in done]
    validation_result = {result[0]: result[1] for result in validation_results}
    return validation_result
