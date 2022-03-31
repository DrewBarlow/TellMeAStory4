# TellMeAStory4
### Authors:
  * Drew Barlow,
  * Kush Shah,
  * Jason Nachman,
  * Kyle Wright, and
  * Joshua Adewunmi.

To explore the project, visit [this Heroku link](https://tellmeastory4.herokuapp.com).<br>

### To run this project:
  1. Clone this repository or download and extract the source code.
  2. Run `python3 pip install -r requirements.txt` to install the necessary dependencies.
  3. Receive an API key from [MapBox](https://docs.mapbox.com/api/accounts/tokens/).
  4. Set `APIKEY = <your_key>` in `story/tellmeastory/constants.py`.
  5. Run `python3 story/manage.py migrate`.
  6. Run `python3 story/manage.py runserver` and visit `localhost:8000`.

### If you wish to run tests:
  * Run `python3 story/manage.py test story/<APP_NAME>/tests`.
  * NOTE: `<APP_NAME>` should be replaced by either `tellmeastory` or `managetags`.
