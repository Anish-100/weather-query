# weather-query
A text-based weather service that provides weather details based on location or local file data. Uses Nominatim for geolocation and National Weather Service for obtaining weather data. 

Below is a **fully copy-and-paste-ready README section**. No extra commentary, just the instructions.

---

## Program Input Instructions

This program reads input from **standard input**. All input must be provided in the exact order and format described below.

---

### 1. Target Location

The first line of input specifies the target location and must be in **one of the following formats**:

```
TARGET NOMINATIM location
```

* `location` is any non-empty string describing the location to analyze.
* The program will use the Nominatim API to determine latitude and longitude.

OR

```
TARGET FILE path
```

* `path` is the path to a local file containing the result of a previous Nominatim API call.
* The file must exist and be in the same format returned by Nominatim.

---

### 2. Weather Data Source

The second line of input specifies the source of weather data and must be in **one of the following formats**:

```
WEATHER NWS
```

* Uses the National Weather Service API to obtain hourly weather forecasts.

OR

```
WEATHER FILE path
```

* `path` is the path to a local file containing the result of a previous NWS hourly forecast API call.
* The file must exist and be in the same format returned by the NWS API.

---

### 3. Weather Queries

The third line of input must be a weather query.
Subsequent lines may contain additional weather queries.

* At least one weather query will be provided.
* There is no limit to the number of queries.
* Queries may appear in any order and may be duplicated.

Each weather query must be in **one of the following formats**:

#### Air Temperature

```
TEMPERATURE AIR scale length limit
```

#### “Feels Like” Temperature

```
TEMPERATURE FEELS scale length limit
```

* `scale`: `F` (Fahrenheit) or `C` (Celsius)
* `length`: positive integer indicating hours into the future
* `limit`: `MAX` or `MIN`

#### Humidity

```
HUMIDITY length limit
```

* Reported as a percentage.

#### Wind Speed

```
WIND length limit
```

* Reported in miles per hour.

#### Precipitation

```
PRECIPITATION length limit
```

* Reported as an hourly percentage chance.

---

### 4. End of Queries

After all weather queries have been entered, include the following line:

```
NO MORE QUERIES
```

---

### 5. Reverse Geocoding

The final line of input specifies how to determine the nearest weather station location and must be in **one of the following formats**:

```
REVERSE NOMINATIM
```

* Uses the Nominatim API for reverse geocoding.

OR

```
REVERSE FILE path
```

* `path` is the path to a local file containing the result of a previous Nominatim reverse geocoding API call.
* The file must exist and be in the same format returned by Nominatim.

---

### Example Input

```
TARGET NOMINATIM Bren Hall, Irvine, CA
WEATHER NWS
TEMPERATURE AIR F 24 MAX
HUMIDITY 24 MIN
WIND 12 MAX
NO MORE QUERIES
REVERSE NOMINATIM
```

---
