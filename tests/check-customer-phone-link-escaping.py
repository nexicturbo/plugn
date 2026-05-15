#!/usr/bin/env python3
from pathlib import Path


views = [
    Path("backend/views/customer/view.php"),
    Path("backend/views/customer/index.php"),
    Path("backend/views/order/index.php"),
    Path("backend/views/order/view.php"),
    Path("backend/views/order/abandoned-checkout.php"),
]

unsafe_patterns = [
    "'<a href=\"tel:'. $model->customer_phone_number",
    "'<a href=\"tel:' . $model->customer_phone_number",
]

required_patterns = [
    "preg_replace('/[^0-9+]/', '', $phoneNumber)",
    "Html::a(Html::encode(str_replace(' ', '', $phoneNumber)), 'tel:' . $telNumber)",
]

for view in views:
    source = view.read_text()
    for unsafe in unsafe_patterns:
        if unsafe in source:
            raise SystemExit(f"{view}: customer phone link still concatenates raw phone data")
    for required in required_patterns:
        if required not in source:
            raise SystemExit(f"{view}: missing sanitized and encoded customer phone link guard")

print("Customer phone link escaping guard passed.")
