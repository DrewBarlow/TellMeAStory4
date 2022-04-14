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

### Notes about tests:
  * There must be an image named `"test_image.jpeg"` in `media/storyimages/`.
  * Issues occur in the database when pulling a branch. If this is the case, run these commands:
    1. `cd story`
    2. `python3 manage.py flush`
    3. `rm tellmeastory/migrations/00*`
    4. `rm managetags/migrations/00*`
    5. `python3 manage.py makemigrations`
    6. `python3 manage.py migrate`

