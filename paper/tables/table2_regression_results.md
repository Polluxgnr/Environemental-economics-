# Table 2: Econometric Panel Regression Results

*Standard errors clustered at the country level reported in parentheses. Inference conducted using small-sample cluster critical values from t(G-1) = t(7). * p < 0.10, ** p < 0.05, *** p < 0.01. Dependent variable in Columns (1)–(3) is Annual Real GDP per Capita Growth (%). Dependent variable in Column (4) is Agriculture Value Added as a % of GDP. Dependent variable in Column (5) is Crop Production Annual Growth (%). 95% Confidence Intervals reported in brackets based on t(7). Sample covers 1960–2023 across 8 countries (1960 dropped because growth is first-differenced; Column 4 restricted by historical WDI reporting inception).*

| Variable                      | (1) Pooled OLS     | (2) Country FE     | (3) Two-Way FE (Preferred)   | (4) Agri Share TWFE   | (5) Crop Growth TWFE   |
|:------------------------------|:-------------------|:-------------------|:-----------------------------|:----------------------|:-----------------------|
| Temperature Anomaly (°C)      | -0.5009**          | -0.4904**          | -0.0325                      | 0.7827                | -1.2883                |
| (Cluster SE)                  | (0.1780)           | (0.1875)           | (0.4301)                     | (1.0898)              | (0.9516)               |
| [95% CI with t(7)]            | [-0.9219, -0.0800] | [-0.9338, -0.0470] | [-1.0496, 0.9847]            | [-1.7943, 3.3597]     | [-3.5384, 0.9618]      |
| p-value (t(7))                | 0.0260             | 0.0346             | 0.9419                       | 0.4959                | 0.2179                 |
| Precipitation Anomaly (100mm) | 0.0596             | 0.0347             | 0.0635                       | -0.0766               | 0.5681*                |
| (Cluster SE)                  | (0.0703)           | (0.0634)           | (0.0550)                     | (0.1121)              | (0.2769)               |
| p-value (t(7))                | 0.4244             | 0.6012             | 0.2857                       | 0.5164                | 0.0793                 |
| Country Fixed Effects         | No                 | Yes                | Yes                          | Yes                   | Yes                    |
| Year Fixed Effects            | No                 | No                 | Yes                          | Yes                   | Yes                    |
| Clustered SEs (Country)       | Yes (G=8)          | Yes (G=8)          | Yes (G=8)                    | Yes (G=8)             | Yes (G=8)              |
| Observations (N)              | 504                | 504                | 504                          | 373                   | 488                    |
| R-squared (overall)           | 0.0210             | 0.0444             | 0.3300                       | 0.9170                | 0.1654                 |
| Within R-squared              | -                  | 0.0176             | 0.0030                       | -                     | -                      |