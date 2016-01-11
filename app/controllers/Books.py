"""
    Books Controller File
"""
from system.core.controller import *

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)
        self.load_model('User')
        self.load_model('Book')

    #Display recent 3 reviews - load view
    #route ['/books']
    def index(self):
        loggedin_user = self.models['User'].get_a_user(session['userid'])
        reviews = self.models['Book'].get_recent3_reviews()
        books_with_reviews = self.models['Book'].get_allbooks_with_reviews()
        return self.load_view('books/index.html', loggedin_user = loggedin_user, reviews = reviews, books_with_reviews = books_with_reviews)


    #Display a form that lets user create a new book and review - load view
    # route ['/books/new']
    def new(self):
        authors = self.models['Book'].get_all_authors()
        books = self.models['Book'].get_all_books()
        return self.load_view('books/new.html', authors = authors, books = books)


    #Display a particular book and its reviews - load view
    # route ['/books/<bookid>']
    def show(self, bookid):
        reviews = self.models['Book'].get_reviews_bybook(bookid)
        book_author = self.models['Book'].get_authorname_booktitle(bookid)
        return self.load_view('books/show.html', reviews=reviews, book_author=book_author)


    #Process the add new book and review form - POST
    #form submitted to route ['/books/create']
    def create_book_review(self):
        book_review = {
            'title_list': request.form['title_list'],
            'new_title': request.form ['new_title'],
            'author_list': request.form['author_list'],
            'new_author': request.form['new_author'],
            'review_content': request.form['review'],
            'review_rating':request.form['rating'],
        }

        add_status = self.models['Book'].add_new_book_and_review(book_review, session['userid'])

        # If validations fail, redirect back to form
        if add_status['status'] == False:
            for message in add_status['error_list']:
                flash(message)
                return redirect ('/books/new')

        #If added successfully, redirect to the book page
        return redirect ('/books/'+str(add_status['bookid']))


    #Process the add review form from the books page - POST
    # route['/books/create_review/<bookid>']
    def create_review (self, bookid):
        review = {
            'content': request.form['review'],
            'rating': request.form['rating']
        }
        add_status = self.models['Book'].add_review (review, bookid, session['userid'])
        # If validations fail, redirect back to form
        if add_status['status'] == False:
            for message in add_status['error_list']:
                flash(message)
        return redirect ('/books/'+str(bookid))



    #Process the delete review link
    # route ['/books/delete/<bookid>/<review_id>']
    def destroy_review(self, bookid, reviewid):
        book_id = self.models['Book'].delete_review(reviewid)
        return redirect ('/books/'+str(bookid))


#   filza.mazahir@gmail.com -> 1qaz2wsX
#   taha.rafiq@gmail.com -> 1qaz2wsX
#   test123@gmail.com -> 1Qaz2wsx

