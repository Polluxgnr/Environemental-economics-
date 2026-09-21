# Table 2: Econometric Panel Regression Results

*Standard errors clustered at the country level reported in parentheses. * p < 0.10, ** p < 0.05, *** p < 0.01. Dependent variable in Columns (1)-(3) is Annual Growth of Real GDP per Capita (%). Dependent variable in Column (4) is Agriculture, Forestry, and Fishing Value Added as a % of GDP. Sample spans 1960–2023 across 8 countries (1960 dropped because growth is first-differenced; Column 4 restricted by historical WDI agricultural data availability).*

| Variable                      | (1) Pooled OLS   | (2) Country FE   | (3) Two-Way FE (Preferred)   | (4) Agri Share TWFE   |
|:------------------------------|:-----------------|:-----------------|:-----------------------------|:----------------------|
| Temperature Anomaly (°C)      | -0.5009***       | -0.4904***       | -0.0325                      | 0.7827                |
|                               | (0.1780)         | (0.1875)         | (0.4301)                     | (1.0898)              |
| Precipitation Anomaly (100mm) | 0.0596           | 0.0347           | 0.0635                       | -0.0766               |
|                               | (0.0703)         | (0.0634)         | (0.0550)                     | (0.1121)              |
| Country Fixed Effects         | No               | Yes              | Yes                          | Yes                   |
| Year Fixed Effects            | No               | No               | Yes                          | Yes                   |
| Clustered SEs (Country)       | Yes              | Yes              | Yes                          | Yes                   |
| Observations (N)              | 504              | 504              | 504                          | 373                   |
| R-squared                     | 0.0210           | 0.0444           | 0.3300                       | 0.9170                |