""" 
    User Model File
"""
from system.core.model import Model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$') 

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def login_user(self, login_info):
        email = login_info['email']
        password = login_info['password']
        error_dict = {}
        error = False

        #Check if both fields are inputted
        if len(email) ==0 or len(password) == 0:
            error_dict ['login'] = "All fields are required! Please try again."
            return {"status": False, "error_dict": error_dict}

        #Validate email
        if not EMAIL_REGEX.match(email): 
            error_dict ['email_login'] = "Invalid email address."
            error = True

        #Check if user exists with the given email and password
        current_user = self.db.query_db("SELECT * FROM users WHERE email = %s", [email])           
        if len(current_user) == 0:
            error_dict['login'] = "Wrong email or password entered. Please try again"
            error = True

        elif not self.bcrypt.check_password_hash(current_user[0]['password'], password):
                error_dict['login'] = "Wrong email or password entered. Please try again"
                error = True

        if error == True: 
            return {"status":False, "error_dict": error_dict}

        #User has been authenticated, log the user in
        id_col = self.db.query_db("SELECT id FROM users WHERE email = %s", [email])
        loggedin_user_id = id_col[0]['id']

        return {"status": True, "id":loggedin_user_id}

    def get_a_user (self, id):
        query = "SELECT * FROM users WHERE id = %s"
        data = [id]
        user = self.db.query_db(query, data)
        return user[0]

    def register(self, register_info):

        name = str(register_info['name'])
        alias = str(register_info['alias'])
        email = register_info['email']
        password = register_info['password']
        conf_password = register_info['conf_password']

        error_dict = {}
        error = False

        #Check if all fields are inputted, return right away if any field is missing
        if len(name)==0 or len(alias) ==0 or len(email) ==0 or len(password)==0 or len(conf_password)==0:
            error_dict['register'] = "All fields are required! Please try again."
            error = True
            return {"status" : False, "error_dict": error_dict}

        #Check first name is atleast 2 chars
        if len(name) < 2:
            error_dict['name'] = "Name must be atleast 2 characters. Please try again."
            error = True

        # elif str.isalpha(name)==False:
        #     error_dict['name'] = "Names must not contain numbers. Please try again."
        #     error = True

        #Check last name is atleast 2 chars & all characters
        if len(alias) < 2:
            error_dict['alias'] = "Alias must be atleast 2 characters. Please try again."
            error = True

        elif str.isalpha(alias)==False:
            error_dict['alias'] = "Alias must not contain numbers. Please try again."
            error = True

        #Validate email
        if not EMAIL_REGEX.match(email):
            error_dict['email_register'] = "Invalid email address."
            error = True

        #Check if email already exists in database
        query = "SELECT * FROM users WHERE email = %s"
        data = [email]
        user = self.db.query_db(query, data)
        if len(user) > 0:
            error_dict['email_register'] = "Email address already exists. Please try registering with another email, or login using this email."
            error = True

        #Validate password
        num_in_pass = False
        upper_in_pass = False
        for char in str(password):
            if str.isupper(char):
                upper_in_pass = True
            if str.isdigit(char):
                num_in_pass = True

        if len(password) < 8:
            error_dict['password_register'] = "Password must be 8 characters."
            error = True

        elif password != conf_password:
            error_dict['password_register'] = "Passwords do not match."
            error = True

        elif num_in_pass == False or upper_in_pass == False:
            error_dict['password_register'] = "Please use atleast 1 uppercase letter and 1 numeric value in your password."
            error = True


        #Check if there were any errors in the previous validation process
        if error == True:
            return {"status" : False, "error_dict": error_dict}

        #Add user to database if no errors then return the id for login purposes
        pw_hash = self.bcrypt.generate_password_hash(password)
        insert_query = "INSERT INTO users (name, alias, email, password, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(), NOW())"
        data = [name, alias, email, pw_hash]
        self.db.query_db(insert_query, data)

        last_id_col = self.db.query_db("SELECT id FROM users ORDER BY id DESC LIMIT 1")
        last_user_id = last_id_col[0]['id']

        return {"status": True, "id":last_user_id}


    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """
