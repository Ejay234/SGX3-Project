# Austin Traffic Data Web Service

This Flask-based API provides access to cleaned and filtered traffic incident data from Austin, Texas. It allows querying data by time, location, column values, and more.

## 🚀 Features

- Load and clean Austin traffic CSV data
- Query incident data by:
  - Column values and year
  - Hour of day
  - Geographic proximity (within 1 km of given coordinates)
- View dataset info, shape, columns, and unique values

## 📁 Dataset

Ensure a file named `atxtraffic.csv` is present in the same directory. It should contain:
- `Published Date`: datetime of incident
- `Latitude`, `Longitude`: location of incident
- Other descriptive columns like `Issue Reported`, `Traffic Report ID`, etc.

---

## 🔧 Setup

1. Clone this repository or download the files.
2. Install dependencies:
   ```bash
   pip install flask pandas
