
# Weather-Uncertainty-Aware Indian Crop Yield Prediction Using Climatic Disturbance Indicators
<br>
<p align="center">

  <strong>Report submitted by:</strong>

</p>

<p align="center">

  <strong>Dharani Krishna Sahithi</strong><sup>1A</sup><br>

  <strong>Dorothy</strong><sup>2B</sup><br>

  <strong>Rahul Kumar Yadav</strong><sup>3C</sup><br>

  <strong>Swagato Lahiri</strong><sup>4D</sup>

</p>

<p align="center">

  <em>For the successful completion of the internship as</em><br>

  <strong>Summer (Data Science) Intern 2026</strong><br>

  <strong>[Tenure: 7 weeks]</strong>

</p>

<p align="center">

  <em>Under the supervision of</em><br><br>

  <strong>Mr. Samyabrata Roy</strong><sup>*</sup><br>

  Associate Software Developer<br>

  IDEAS - Institute of Data Engineering, Analytics and Science Foundation,<br>

  Technology Innovation Hub, Indian Statistical Institute, Kolkata

</p>

<br>

<p align="center">

  <strong>Report submitted to:</strong><br><br>

  <strong>

  IDEAS - Institute of Data Engineering, Analytics and Science Foundation,<br>

  Technology Innovation Hub, Indian Statistical Institute,<br>

  Kolkata, West Bengal, India

  </strong>

</p>

<br>

---

<sup>A</sup> BMS Institute of Technology & Management, Bengaluru;  

<sup>B</sup> Jawaharlal Nehru University, Delhi;  

<sup>C</sup> Birla Institute of Technology, Mesra;  

<sup>D</sup> Dr. B C Roy Engineering College, DGP

<sup>1</sup> sahithidharani0404@gmail.com;  

<sup>2</sup> dorothybisht@gmail.com;  

<sup>3</sup> rahulyadavbitmesra4@gmail.com;  

<sup>4</sup> 24f3000419@ds.study.iitm.ac.in;  

<sup>*</sup> sroy@ideas-tih.org

---

# IDEAS-TIH Summer Internship Program 2026

This repository contains the project work completed as part of the **Summer Internship Program 2026** under **IDEAS - Technology Innovation Hub, Indian Statistical Institute, Kolkata**.

The repository includes source code, datasets, notebooks, documentation, reports, references, and other project-related materials developed by the assigned intern team.

---

# Project Details

## Project Title

**Weather-Uncertainty-Aware Indian Crop Yield Prediction Using Climatic Disturbance Indicators**

---

## Project Category

- Machine Learning / Deep Learning Project  

- Research-Oriented Project  

---

# Problem Statement

Accurate crop yield forecasting is hindered by the **uncertainty of climatic disturbances** such as the El Niño–Southern Oscillation (ENSO), Western Disturbances, and Cloudburst events. These phenomena strongly affect rainfall, temperature, and water availability, yet their unpredictable occurrence and intensity make reliable forecasting difficult.

This problem is critical because **agricultural productivity and food security** depend on robust yield predictions. Farmers need forecasts to plan irrigation and crop choices, while policymakers rely on them for climate‑resilient agricultural planning. Without accounting for weather uncertainty, forecasts risk being misleading or incomplete.

To address this, the project develops a **modular, weather‑uncertainty‑aware forecasting framework** that integrates:
- **ENSO forecasting module**: predicts Niño 3.4 SST anomalies and phase probabilities (El Niño, Neutral, La Niña).  
- **Western Disturbance forecasting**: captures seasonal patterns and intensity using lagged meteorological features and time‑series models.  
- **Cloudburst prediction**: handles extreme class imbalance to identify localized high‑impact rainfall events.  

These outputs are combined with **district‑level crop yield data** from ICRISAT to form a unified prediction pipeline. Machine learning models (Random Forest, SARIMAX) and ablation studies evaluate the contribution of each vertical.

The expected solution is an **uncertainty‑aware crop yield forecasting system** that delivers:
- Probabilistic yield predictions at the district level  
- Improved accuracy over baseline models (≈18% RMSE reduction)  
- Region‑specific insights (e.g., ENSO dominance in South India, WD importance in North India, Cloudburst impact in Eastern India)  

This framework serves as a **decision‑support tool** that enhances resilience in agricultural planning by explicitly modelling weather uncertainty.


---
