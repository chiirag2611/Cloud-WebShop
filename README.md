This is a full stack web application designed to manage e-commerce or store functionality. It includes features such as adding products to a shopping cart, updating cart quantities, managing product inventory, filtering of products and payment gateway. It is hosted using cloud AWS EC2 Beanstalk with free tier version.

To run this project follow below steps:

1. **Export your database**: 
```python 
python manage.py dumpdata > data.json
```

2. **Export your media files** (product images)
Create a zip file containing your media folder for storage purpose.

3. **Create requirements.txt**:
```bash
pip freeze > requirements.txt
```

4. **Instructions for others** (create a README.md for new instruction if any):
```markdown
# E-commerce Project Setup Instructions

## Prerequisites
- Python 3.x
- pip

## Setup Steps

1. Clone the repository
```bash
git clone https://github.com/chiirag2611/Cloud-WebShop.git
cd Cloud-Webshop
```

2. Create and activate virtual environment
```bash
python -m venv env

# For Windows
env\Scripts\activate

# For Mac/Linux
source env/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
pip install django
pip install pillow
```

4. Create database
```bash
python manage.py migrate
```

5. Load the data
```bash
python manage.py loaddata data.json
```

6. Extract media files
- Unzip the media.zip file into the project root directory

7. Create superuser (admin)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account (follow below to access my admin profile)
Email: c*************1@gmail.com
First name: Chirag
Last Name: Chawla
Password: ********
```

8. Run the server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin to access the admin panel
Visit http://127.0.0.1:8000 to view the store

## Admin Access
Username: [****]
Password: [****]
```

5. **Files included in our project**:
- Our entire project code
- requirements.txt
- data.json (database dump)
- media.zip (containing all product images)
- README.md


Let me know if you need help with any of these steps!