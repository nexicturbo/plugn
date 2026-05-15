#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text()


def grid_column_block(source, label, occurrence=1):
    matches = list(
        re.finditer(
            rf"'label'\s*=>\s*'{re.escape(label)}'.*?'value'\s*=>\s*function\s*\(\$data\)\s*\{{.*?\}}\s*\n\s*\]",
            source,
            re.S,
        )
    )
    if len(matches) < occurrence:
        raise AssertionError(f"Could not find {label!r} column occurrence {occurrence}")
    return matches[occurrence - 1].group(0)


def assert_text_column(source, label, occurrence=1):
    block = grid_column_block(source, label, occurrence)
    if "'format' => 'text'" not in block:
        raise AssertionError(f"{label!r} occurrence {occurrence} must use text format")
    if "'format' => 'raw'" in block:
        raise AssertionError(f"{label!r} occurrence {occurrence} must not use raw format")


partner_view = read("backend/views/partner/view.php")
partner_payout_view = read("backend/views/partner-payout/view.php")

assert_text_column(partner_view, "Store Name", 1)
assert_text_column(partner_view, "Customer Name", 1)
assert_text_column(partner_view, "Store Name", 2)

assert_text_column(partner_payout_view, "Store Name", 1)
assert_text_column(partner_payout_view, "Store Name", 2)

print("Partner payment grid escaping guard passed.")
