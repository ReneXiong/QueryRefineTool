# QueryRefineTool
A python tool for querying a certain amount of results in a postgresql database, utilizing psycopg2 library.
## Setup
```
pip install psycopg2
```
You also need a postgresql database setup (with data) and connectable for queries.
## How to use
Please check specification.md
## Improvements could be done:

  - Making better suggestions with the highest data density
    (It is starting from the minimum value of the column now)
  - Tests and comments
  - Refactor UI for better efficiency and readability
  - Probably a webui (with a backend) will be more intuitive
  - Making suggestions based on user-chosen attributes
  - Suggesting function rewrite for better performance