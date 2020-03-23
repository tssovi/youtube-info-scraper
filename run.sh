# Get OS type
os=""
case "$OSTYPE" in
 solaris*) os=SOLARIS ;;
 darwin*)  os=OSX ;;
 linux*)   os=LINUX ;;
 bsd*)     os=BSD ;;
 msys*)    os=WINDOWS ;;
 *)        os=unknown: $OSTYPE ;;
esac

if [[ "$os" == 'LINUX' ]]; then
   # Make a directory named venvs
   mkdir venvs
   # Install virtualenv
   pip3 install virtualenv --user
   # Install virtualenv globally
   sudo apt install virtualenv
   # Create a virtualenv named youtube_env
   virtualenv -p python3 venvs/youtube_env
   # Activate the created env
   source venvs/youtube_env/bin/activate
elif [[ "$os" == 'WINDOWS' ]]; then
   # Make a directory named venvs
   mkdir \venvs
   # Install virtualenv
   pip install virtualenv
   pip install virtualenvwrapper-win
   # Create a virtualenv named youtube_env
   virtualenv \venvs\youtube_env
   # Activate the created env
   \venvs\youtube_env\Scripts\activate
fi

# Clone project from git
git clone https://github.com/tssovi/youtube_info_scraper.git

# Go to project directory
cd youtube_info_scraper

# Copy example_env.py as env.py
cp -v youtube_scraper/env_example.py youtube_scraper/env.py

echo Please Provide Your Existing Database Name:
read db_name
sed -i -- "s/database_name/$db_name/g" youtube_scraper/env.py

echo Please Provide Your Existing Database Username:
read db_user
sed -i -- "s/db_username/$db_user/g" youtube_scraper/env.py

echo Please Provide Your Existing Database Password:
read db_pass
sed -i -- "s/db_password/$db_pass/g" youtube_scraper/env.py

echo Please Provide Your Secret Youtube API Key:
read api_key
sed -i -- "s/your_secret_api_key/$api_key/g" youtube_scraper/env.py

# Install required packages
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Migrate database
python manage.py migrate

# Run python shell to seed wiki data
python manage.py data-scraper

# Run tests for this project
python manage.py test

# Run project
python manage.py runserver
