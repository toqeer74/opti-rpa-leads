import asyncio
import dns.resolver
import aiosmtplib
from email_validator import validate_email, EmailNotValidError


def validate_email_smtp(email):
    try:
        v = validate_email(email, check_deliverability=False)
        domain = v.domain
    except EmailNotValidError:
        return "invalid"

    try:
        mx = dns.resolver.resolve(domain, "MX")[0].exchange.to_text()

        async def check():
            try:
                s = aiosmtplib.SMTP(hostname=mx, port=25, timeout=8)
                await s.connect()
                await s.ehlo()
                await s.mail("validator@" + domain)
                code, _ = await s.rcpt(email)
                await s.quit()
                if code in (250, 251, 252):
                    return "deliverable"
                if 500 <= code < 600:
                    return "invalid"
            except Exception:
                pass
            return "catch_all"

        return asyncio.run(check())
    except Exception:
        return "unknown"

