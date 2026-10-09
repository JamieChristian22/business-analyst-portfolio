# Reproducible analysis results

Results are computed from supplied repository CSVs. Amounts are portfolio-assumed USD. Empty tables indicate no rows returned; they are not proof of production approval.

## Q01: Control totals
[SQL](../SQL/Q01.sql) | [Full CSV output](Q01.csv)

| records | orders | units | gmv | platform_revenue | weighted_take_rate | aov |
| --- | --- | --- | --- | --- | --- | --- |
| 5500 | 5500.0 | 6803.0 | 239161.36 | 33393.15 | 0.13962602487291426 | 43.483883636363636 |

## Q02: Monthly marketplace metrics
[SQL](../SQL/Q02.sql) | [Full CSV output](Q02.csv)

| month | gmv | platform_revenue | orders | prior_gmv | weighted_take_rate | aov | mom_gmv_change |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-07 | 41096.54 | 5798.31 | 954.0 |  | 0.1410899798377187 | 43.078134171907756 |  |
| 2025-08 | 40022.16 | 5641.7 | 930.0 | 41096.54 | 0.14096440571923152 | 43.03458064516129 | -0.026142833435612762 |
| 2025-09 | 38572.5 | 5369.03 | 884.0 | 40022.16 | 0.13919320759608528 | 43.634049773755656 | -0.03622143332593752 |
| 2025-10 | 40225.22 | 5526.82 | 935.0 | 38572.5 | 0.13739688682871093 | 43.0216256684492 | 0.04284710609890469 |
| 2025-11 | 38156.6 | 5323.44 | 875.0 | 40225.22 | 0.13951557528710629 | 43.60754285714285 | -0.05142594620986542 |
| 2025-12 | 41088.34 | 5733.85 | 922.0 | 38156.6 | 0.1395493222651487 | 44.56436008676789 | 0.07683441396770148 |

## Q03: Seller contribution
[SQL](../SQL/Q03.sql) | [Full CSV output](Q03.csv)

| seller | gmv | platform_revenue | orders | gmv_share | weighted_take_rate |
| --- | --- | --- | --- | --- | --- |
| Apex Outdoor | 60512.15 | 8453.6 | 1347.0 | 0.25301808787171975 | 0.13970086999057216 |
| Apex Value | 59789.51 | 8295.05 | 1376.0 | 0.24999652953972165 | 0.1387375477738486 |
| Apex Prime | 59630.57 | 8387.96 | 1381.0 | 0.24933195730280178 | 0.1406654338538102 |
| Apex Essentials | 59229.13 | 8256.54 | 1396.0 | 0.24765342528575687 | 0.13939998781005228 |

## Q04: Product Pareto contribution
[SQL](../SQL/Q04.sql) | [Full CSV output](Q04.csv)

| product_id | gmv | product_rank | cumulative_gmv_share |
| --- | --- | --- | --- |
| Product-008 | 4212.18 | 1 | 0.017612293223286574 |
| Product-009 | 3870.02 | 2 | 0.03379392055639758 |
| Product-001 | 3818.82 | 3 | 0.04976146648438527 |
| Product-057 | 3780.51 | 4 | 0.06556882767350045 |
| Product-038 | 3708.19 | 5 | 0.08107379887787894 |
| Product-079 | 3665.15 | 6 | 0.09639880790107568 |
| Product-078 | 3612.0 | 7 | 0.11150158202813366 |
| Product-029 | 3575.52 | 8 | 0.12645182315404127 |
| Product-054 | 3570.7 | 9 | 0.14138191052266974 |
| Product-006 | 3562.43 | 10 | 0.15627741872683784 |
| Product-077 | 3561.98 | 11 | 0.1711710453561562 |
| Product-020 | 3548.61 | 12 | 0.1860087683060508 |
| Product-035 | 3509.75 | 13 | 0.20068400681447873 |
| Product-049 | 3496.71 | 14 | 0.21530472146503934 |
| Product-055 | 3489.91 | 15 | 0.22989700342898203 |
| Product-045 | 3468.0 | 16 | 0.24439767360413073 |
| Product-052 | 3437.34 | 17 | 0.25877014581285207 |
| Product-023 | 3391.37 | 18 | 0.2729504046974813 |
| Product-040 | 3334.73 | 19 | 0.28689383602769275 |
| Product-036 | 3254.54 | 20 | 0.3005019707196849 |
First 20 of 80 result rows shown. Full output is in the linked CSV.

## Q05: Category and seller drilldown
[SQL](../SQL/Q05.sql) | [Full CSV output](Q05.csv)

| category | seller | gmv | platform_revenue | orders | weighted_take_rate |
| --- | --- | --- | --- | --- | --- |
| Electronics | Apex Outdoor | 19570.93 | 2731.14 | 252.0 | 0.1395508542516886 |
| Electronics | Apex Value | 18555.92 | 2602.81 | 231.0 | 0.14026844263178545 |
| Electronics | Apex Essentials | 16731.51 | 2345.37 | 216.0 | 0.1401768280328554 |
| Electronics | Apex Prime | 15326.37 | 2143.28 | 204.0 | 0.13984263723243012 |
| Fitness | Apex Prime | 12874.21 | 1804.29 | 223.0 | 0.14014762847584436 |
| Fitness | Apex Essentials | 12379.19 | 1688.36 | 218.0 | 0.13638695261967865 |
| Fitness | Apex Outdoor | 12319.95 | 1729.94 | 214.0 | 0.1404177776695522 |
| Fitness | Apex Value | 12191.26 | 1680.48 | 230.0 | 0.13784301212507977 |
| Home | Apex Prime | 10209.47 | 1460.58 | 236.0 | 0.14306129505253457 |
| Home | Apex Essentials | 10184.63 | 1448.99 | 240.0 | 0.14227222785707483 |
| Home | Apex Outdoor | 9658.98 | 1331.17 | 225.0 | 0.13781682952030133 |
| Home | Apex Value | 9577.45 | 1327.44 | 218.0 | 0.1386005669567578 |
| Kitchen | Apex Prime | 8736.5 | 1220.53 | 244.0 | 0.13970468723172896 |
| Kitchen | Apex Outdoor | 8480.87 | 1187.84 | 227.0 | 0.1400611022218239 |
| Kitchen | Apex Value | 8164.25 | 1132.67 | 235.0 | 0.13873534004960653 |
| Kitchen | Apex Essentials | 7505.34 | 1040.49 | 230.0 | 0.13863329309531613 |
| Beauty | Apex Essentials | 7167.22 | 989.66 | 258.0 | 0.13808143185223837 |
| Beauty | Apex Prime | 7033.55 | 999.87 | 249.0 | 0.14215723212318104 |
| Beauty | Apex Value | 5888.65 | 811.16 | 217.0 | 0.13774973890450273 |
| Beauty | Apex Outdoor | 5456.01 | 766.89 | 214.0 | 0.14055875997294726 |
First 20 of 24 result rows shown. Full output is in the linked CSV.
