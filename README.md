# Content Review System
* upload Movie data as CSV file
* list movies as paginated response along with filter/sorting capabilities

---
## SETUP

* Clone project: `git clone <repo_url>`
* Create virtual environment: `python -m venv venv
`
* Activate virtual enviroment: `venv\Scripts\activate
`
* Install dependencies: `pip install -r requirements.txt
`
* Apply Migrations: `python manage.py migrate
`
* Run server: `python manage.py runserver
`
---
## Supported APIs
* GET `/movie/list`
  * params
    * page: To access specific page in paginated response
      * Example: 1
    * languages: Filter by comma seperated string of languages
      * Example: English OR English, French, ......
    * year_of_release: Filter by comma seperated values for years
      * Example: 2020 or 2020, 2021, ....
    * sort_by_ratings: sort by ratings in both ascending/descending order
      * "true": descending order
      * "false": ascending order
    * sort_by_release: sort by release date in both ascending/descending order
      * "true": descending order
      * "false": ascending order
* POST `/movie/upload/`
  * body [form-data]
    * key: "file", type: "File", value: example.csv
