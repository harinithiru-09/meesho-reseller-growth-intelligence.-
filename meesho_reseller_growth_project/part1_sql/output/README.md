# Part 1 Output Notes

`monthly_category_revenue.csv` is the direct hand-off to Part 2 and Part 4.

For the zero-order reseller LEFT JOIN demonstration, `COUNT(*)` is 1 because the LEFT JOIN preserves the unmatched reseller as one all-NULL right-side row. `COUNT(order_id)` is 0 because COUNT(column) ignores NULL values. Therefore `COUNT(*)` must not be used to detect a zero-match LEFT JOIN.
