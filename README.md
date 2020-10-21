# Urban Kit 

**An out-of-box analysis tool for urban sensory data.**





## Features

- Data Support
  - CSV File, including `id`,`longitude`,`latitude` columns and any attributes column.

- Statistic
  - Max/Min/Avg/Medium/Q1/Q3/Variance Dynamic Calculation.
  - Correlation Analysis: DTW/Pearson
- Learning Model
  - Timeseries Prediction: LSTM. LgihtGBM
  - Anomaly Detection: Islation Forest
  - Sptial Interpolation: SI-AGAN



## Tech Stack

- Front end
  - Dev: Vue.js
  - Visualization: E-Charts
  - UI: Element-UI
- Back end
  - Dev: Django
  - Leanring Model: PyTorch, Scikit-Learn
- Databse
  - MongoDB



## Design

- Front End

  <img src="figs\frontend.png" alt="frontend" style="zoom:100%;" />

- Back End

  <img src="figs\backend.png" alt="frontend" style="zoom:100%;" />



## Demo

- Core Operation

  <img src="figs\1.gif" alt="Main" style="zoom:100%;" />

- Correlation Analysis

  <img src="figs\corr.gif" alt="Correlation" style="zoom:100%;" />

- Anomaly Detection

  <img src="figs\det.gif" alt="Detection" style="zoom:100%;" />

- Spatial Interpolation

  <img src="figs\inter.gif" alt="Interpolation" style="zoom:100%;" />

- Timeseries Prediction

  <img src="figs\tsp.gif" alt="Prediction" style="zoom:100%;" />



## Reference

1. Yujia Gao, Liang Liu, Chi Zhang, Xiao Wang, Huadong Ma. "SI-AGAN: Spatial Interpolation with Attentional Generative Adversarial Networks for Environment Monitoring", In ECAI, 2020.
2. Ruiyuan Li, Huajun He, Rubin Wang, Yuchuan Huang, Junwen Liu, Sijie Ruan, Tianfu He, Jie Bao, and Yu Zheng. "JUST: JD Urban Spatio-Temporal Data Engine", In ICDE. IEEE, 2020.
3. Y. Zheng, L. Capra, O. Wolfson, and H. Yang. 2014b. "Urban computing: Concepts, methodologies, and applications". ACM Transactions on Intelligent Systems and Technology 5, 3 (2014), 38--55.
4. Liu, Fei Tony, Kai Ming Ting, and Zhi-Hua Zhou. "Isolation forest", 2008 Eighth IEEE International Conference on Data Mining. IEEE, 2008.