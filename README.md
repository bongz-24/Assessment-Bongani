# Data Scientist Competency Assessment 2026

## Overview

This project focuses on transforming raw healthcare datasets into a structured, patient-level dataset that can be used for analysis and decision-making. The work includes a SQL task, data processing and feature engineering in Python, a visualisation, and written responses based on practical experience.

---

## How to Review This Work

The repository has been organised so that each part of the assessment is easy to locate.

The SQL solution for Question 1 can be found in `sql/update_art.sql`. This contains the query used to update ART drug codes based on the new mapping provided.

The main data processing work is in `src/data_processing.py`. This script handles the full pipeline, starting from loading the raw datasets, cleaning and standardising them, aggregating the data to one row per patient, and then creating the required features such as age groups, medication categories, and the follow-up flag.

The final outputs are located in the `output/` folder. This includes the processed dataset (`final_dataset.csv` and an Excel version), as well as the visualisation created for Question 3 showing the distribution of patients on insulin across age groups and sex.

The written responses for Questions 4 to 6 are in `answers/q4_q5_q6.md`. These cover a real example of a mistake in analysis, working through a challenging team dynamic, and handling tight deadlines.

The original datasets provided for the assessment are stored in the `data/` folder.

---

## Approach

The workflow followed a structured approach.

The first step was to clean and standardise both datasets so that fields such as dates, patient identifiers, and categorical variables were consistent. This made it possible to combine the data reliably.

The next step was aggregation. Since the requirement was to have one row per patient, the data was grouped and summarised to capture key information such as the most recent dispensing date and the latest HbA1c result.

Feature engineering was then applied to create variables that are more meaningful for analysis. This included grouping patients into age categories, classifying medication usage, and defining a follow-up flag based on clinical thresholds and missing treatment.

Finally, a visualisation was created to summarise the distribution of patients receiving insulin treatment across age groups and sex.

---

## Tools Used

Python was used for data processing, primarily with pandas for data manipulation and matplotlib for visualisation. SQL was used for the update query, and Git was used to manage and organise the project.

---

## Notes

The structure of this project reflects how I would approach real and practical data task, while focusing on clarity, reproducibility, and making it easy for someone else to follow the work.
