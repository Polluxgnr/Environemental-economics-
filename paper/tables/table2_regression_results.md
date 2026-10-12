# Table 2: Econometric Panel Regression Results (12 Countries, 1960-2023)

*Notes: Standard errors clustered at the country level reported in parentheses (G=12 clusters). Inference conducted using small-sample cluster critical values from t(G-1) = t(11) (Cameron, Gelbach, & Miller, 2008). * p < 0.10, ** p < 0.05, *** p < 0.01. Dependent variable in Columns (1)-(4) is Annual Real GDP per Capita Growth (%). Dependent variable in Column (5) is Agriculture Value Added as a % of GDP. Dependent variable in Column (6) is Crop Production Annual Growth (%). 95% Confidence Intervals reported in brackets based on t(11). Sample covers 1960-2023 across 12 countries.*

| Variable                      | (1) Pooled OLS     | (2) Country FE     | (3) Two-Way FE    | (4) Continental TWFE   | (5) Agri Share TWFE   | (6) Crop Growth TWFE   |
|:------------------------------|:-------------------|:-------------------|:------------------|:-----------------------|:----------------------|:-----------------------|
| Temperature Anomaly (deg C)   | -0.6883***         | -0.8239***         | -0.6547*          | Interacted             | 0.9298                | -1.9002*               |
| (Cluster SE)                  | (0.1329)           | (0.0979)           | (0.2992)          | -                      | (0.7389)              | (0.8640)               |
| [95% CI with t(11)]           | [-0.9808, -0.3959] | [-1.0395, -0.6084] | [-1.3133, 0.0039] | -                      | [-0.6966, 2.5561]     | [-3.8017, 0.0014]      |
| p-value (t(11))               | 0.0003             | 0.0000             | 0.0512            | -                      | 0.2343                | 0.0501                 |
| x Europe                      | -                  | -                  | -                 | -0.6494*               | -                     | -                      |
| (Cluster SE)                  | -                  | -                  | -                 | (0.3216)               | -                     | -                      |
| x Africa                      | -                  | -                  | -                 | -0.6511*               | -                     | -                      |
| (Cluster SE)                  | -                  | -                  | -                 | (0.3564)               | -                     | -                      |
| x Asia-Pacific                | -                  | -                  | -                 | -0.3787                | -                     | -                      |
| (Cluster SE)                  | -                  | -                  | -                 | (0.3229)               | -                     | -                      |
| x Americas                    | -                  | -                  | -                 | -0.9226**              | -                     | -                      |
| (Cluster SE)                  | -                  | -                  | -                 | (0.4063)               | -                     | -                      |
| Precipitation Anomaly (100mm) | 0.0403             | 0.0417             | 0.0529            | 0.0519                 | -0.1704               | 0.7015                 |
| (Cluster SE)                  | (0.0747)           | (0.0729)           | (0.0658)          | (0.0678)               | (0.1734)              | (0.4221)               |
| p-value (t(11))               | 0.6006             | 0.5786             | 0.4390            | 0.4604                 | 0.3471                | 0.1247                 |
| Country Fixed Effects         | No                 | Yes                | Yes               | Yes                    | Yes                   | Yes                    |
| Year Fixed Effects            | No                 | No                 | Yes               | Yes                    | Yes                   | Yes                    |
| Clustered SEs (Country)       | Yes (G=12)         | Yes (G=12)         | Yes (G=12)        | Yes (G=12)             | Yes (G=12)            | Yes (G=12)             |
| Observations (N)              | 732                | 732                | 732               | 732                    | 602                   | 744                    |
| R-squared (overall)           | 0.0262             | 0.1391             | 0.3431            | 0.3442                 | 0.9038                | 0.1400                 |
| Within R-squared              | -                  | 0.0385             | 0.0218            | -                      | -                     | -                      |