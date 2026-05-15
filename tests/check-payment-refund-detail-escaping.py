#!/usr/bin/env python3
"""Guard admin payment/refund detail views against raw user-name rendering."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text()


def assert_label_uses_text(source, label, expected_count):
    pattern = re.compile(
        r"'label'\s*=>\s*'" + re.escape(label) + r"'\s*,\s*"
        r"'format'\s*=>\s*'text'",
        re.S,
    )
    matches = pattern.findall(source)
    if len(matches) != expected_count:
        raise AssertionError(
            f"{label} should use text format {expected_count} time(s); "
            f"found {len(matches)}",
        )


payment_view = read("backend/views/payment/view.php")
refund_view = read("backend/views/refund/view.php")

assert_label_uses_text(payment_view, "Store Name", 1)
assert_label_uses_text(payment_view, "Customer Name", 1)
assert_label_uses_text(refund_view, "Store Name", 2)
assert_label_uses_text(refund_view, "Customer Name", 1)

for path, source in {
    "backend/views/payment/view.php": payment_view,
    "backend/views/refund/view.php": refund_view,
}.items():
    for label in ("Store Name", "Customer Name"):
        raw_pattern = re.compile(
            r"'label'\s*=>\s*'" + re.escape(label) + r"'\s*,\s*"
            r"'format'\s*=>\s*'raw'",
            re.S,
        )
        if raw_pattern.search(source):
            raise AssertionError(f"{path} still renders {label} as raw")

print("Payment/refund detail escaping guard passed.")
