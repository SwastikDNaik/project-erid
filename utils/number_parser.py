import re


def normalize_indian_currency(text):

    text = text.lower()

    # =====================================
    # Convert lakh/lakhs
    # =====================================

    lakh_pattern = r'(\d+(?:\.\d+)?)\s*lakh'

    matches = re.findall(lakh_pattern, text)

    for match in matches:

        value = float(match) * 100000

        text = re.sub(
            rf'{match}\s*lakh',
            f'₹{int(value)}',
            text,
            count=1
        )

    # =====================================
    # Convert crore/crores
    # =====================================

    crore_pattern = r'(\d+(?:\.\d+)?)\s*crore'

    matches = re.findall(crore_pattern, text)

    for match in matches:

        value = float(match) * 10000000

        text = re.sub(
            rf'{match}\s*crore',
            f'₹{int(value)}',
            text,
            count=1
        )

    return text