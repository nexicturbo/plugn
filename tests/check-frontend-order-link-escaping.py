#!/usr/bin/env python3
from pathlib import Path


views = [
    Path("frontend/views/site/incoming-orders-table.php"),
    Path("frontend/views/site/real-time-orders.php"),
]

unsafe_patterns = [
    "Html::a($data->customer->customer_name",
    "'<a href=\"tel:'. $model->customer_phone_number",
    "'<a href=\"tel:' . $model->customer_phone_number",
]

required_patterns = [
    "Html::a(Html::encode($data->customer->customer_name)",
    "preg_replace('/[^0-9+]/', '', $phoneNumber)",
    "Html::a(Html::encode(str_replace(' ', '', $phoneNumber)), 'tel:' . $telNumber)",
]

for view in views:
    source = view.read_text()
    for unsafe in unsafe_patterns:
        if unsafe in source:
            raise SystemExit(f"{view}: frontend order table still renders raw customer link data")
    for required in required_patterns:
        if required not in source:
            raise SystemExit(f"{view}: missing encoded customer link or sanitized phone guard")

print("Frontend order link escaping guard passed.")
