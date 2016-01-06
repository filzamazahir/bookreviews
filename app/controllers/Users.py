""" 
    Users Controller File
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Book')
 
    def index(self):    

        # Display log in page if not logged in
        if not session.get('userid') or not session['userid']: #second one means if session['userid'] = False
            return self.load_view('users/index.html')

        # If logged in already, display redirect to books index
        return redirect('/books')

    def login(self):

        login_info = {
            "email": request.form['email'], 
            "password": request.form['password']
        }
        login_status = self.models['User'].login_user(login_info)

        #Flash errors if login fails
        if login_status['status'] == False:
            error_dict = login_status['error_dict']
            for key,val in error_dict.items():
                flash(val, key)

        #Log in the user if user is authenticated
        if login_status['status'] == True:
            session['userid'] = login_status['id']

        return redirect ('/')


    def register(self):
        register_info = {
            "name": request.form['name'],
            "alias": request.form['alias'],
            "email": request.form['email'], 
            "password": request.form['password'],
            "conf_password": request.form['conf_password']
        }

        register_status = self.models['User'].register(register_info)

        #Flash errors if registration fails
        if register_status['status'] == False:
            error_dict = register_status['error_dict']
            for key,val in error_dict.items():
                flash(val, key)

        #Log in the user if user is registered successfully
        else:
            session['userid'] = register_status['id']

        return redirect ('/')

    #route ['/users/id']
    def show(self, id):
        user = self.models['User'].get_a_user(id)
        books_reviewed = self.models['Book'].get_booksreviewed_byuser(id)
        count = len(books_reviewed)
        return self.load_view('users/show.html', user = user, books_reviewed = books_reviewed, count = count) 

    def logoff(self):
        session['userid'] = False
        return redirect ('/')


