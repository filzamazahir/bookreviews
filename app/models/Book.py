""" 
    Book Model File
"""
from system.core.model import Model

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()

    #Get the 3 most recent reviews added to display on the home page
    def get_recent3_reviews(self):
        query = "SELECT users.id AS userid, users.alias, books.id AS bookid, books.title, reviews.id AS reviewid, reviews.content, reviews.rating, reviews.created_at FROM reviews JOIN users ON reviews.user_id = users.id JOIN books ON reviews.book_id = books.id ORDER BY reviews.id DESC LIMIT 3"
        recent3_reviews = self.db.query_db(query)
        return recent3_reviews


    #Get all the books that have a review attached to it
    def get_allbooks_with_reviews(self):
        query = "SELECT books.id as bookid, books.title FROM reviews JOIN books ON reviews.book_id = books.id GROUP BY reviews.book_id"
        books_with_reviews = self.db.query_db(query)
        return books_with_reviews

    #Get all authors in the authors table
    def get_all_authors(self):
        authors = self.db.query_db("SELECT * FROM authors")
        return authors

    def get_all_books(self):
        books = self.db.query_db("SELECT * FROM books")
        return books

    #Get a book's title and author's name given a book id.
    def get_authorname_booktitle(self, bookid):
        books = self.db.query_db("SELECT * FROM books WHERE id = %s", [bookid])
        booktitle = books[0]['title']
        bookid = books[0]['id']

        authorname_col = self.db.query_db("SELECT authors.name FROM books JOIN authors ON authors.id = books.author_id WHERE books.id = %s", [bookid])
        authorname = authorname_col[0]['name']

        return {'title': booktitle, 'bookid': bookid, 'author':authorname}


    #Get all the books reviewed by a given user
    def get_booksreviewed_byuser(self, userid):
        query = "SELECT books.id AS bookid, books.title FROM reviews JOIN books ON reviews.book_id = books.id WHERE reviews.user_id = %s"
        books = self.db.query_db(query, [userid])
        return books

    #Get all reviews for a given book
    def get_reviews_bybook(self, bookid):
        query = "SELECT users.id AS userid, users.alias, books.id AS bookid, books.title, reviews.id AS reviewid, reviews.content, reviews.rating, reviews.created_at FROM reviews JOIN users ON reviews.user_id = users.id JOIN books ON reviews.book_id = books.id WHERE book_id = %s"
        reviews = self.db.query_db(query, [bookid])
        return reviews


    #Add a book and a review, including add the author if he/she doesn't exist in db
    def add_new_book_and_review(self, book_review, loggedin_userid):
        new_title = book_review['new_title']
        # title_list = book_review['title_list']
        new_author = book_review['new_author']
        # author_list = book_review ['author_list']
        review_content = book_review['review_content']
        rating = book_review['review_rating']
        title = ""
        author = ""
        error_list = []
        error = False
        new_book_added = False
        new_author_added = False
        
        # if title_list == 'None-Add New':
        title = new_title
        new_book_added = True
        # else:
        #     title = title_list

        # if author_list == 'None-Add New':
        author = new_author
        new_author_added = True
        # else:
        #     author = author_list

        #Validate the new book and review
        book_check = self.db.query_db("SELECT * FROM books WHERE title = %s", [title])
        if len(book_check)> 0 and new_book_added == True:
            error_list.append ("Book already exists in database. Please select from the right menu to add review")
            error = True
            
        if len(title) == 0 or len(author)==0 or len(review_content) == 0:
            error_list.append ("All fields must be entered")
            error = True

        

        # author_check = self.db.query_db("SELECT * FROM authors WHERE name = %s", [author])
        # if len(author_check) >0 and new_author_added == True:
        #     error_list.append("Author already exists in database. Please select from drop down")
        #     error = True

        #Return at this point if there are any errors
        if error == True:
            return {'status': False, 'error_list': error_list}

        #Add the author if its a new one and get the author id
        author_data = [author]
        print author
        print author_data
        if new_author_added == True:
            insert_author_query = "INSERT INTO authors (name, created_at, updated_at) VALUES (%s, NOW(), NOW())"
            self.db.query_db(insert_author_query, author_data)

        #Get author id of the author that was added by name
        get_authorid_query = "SELECT id FROM authors WHERE name = %s"
        authorid_col = self.db.query_db(get_authorid_query, author_data)
        authorid = authorid_col[0]['id']

        #Add the book into db if its a new book title
        if new_book_added == True:
            insert_book_query = "INSERT INTO books (author_id, title, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())"
            book_data = [authorid, title]
            self.db.query_db(insert_book_query, book_data)

        #Get book id of last book just added
        bookid_col = self.db.query_db("SELECT id FROM books WHERE title = %s", [title])
        bookid = bookid_col[0]['id']

        #Add the review
        insert_review_query = "INSERT INTO reviews (book_id, user_id, content, rating, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(), NOW())"
        review_data = [bookid, loggedin_userid, review_content, rating]
        self.db.query_db(insert_review_query, review_data)

        return {'status': True, 'bookid': bookid}


    #Add a review for a given book
    def add_review (self, review, bookid, loggedin_userid):
        error_list = []
        if len(review['content']) == 0:
            error_list.append ('Please enter a review to add the review')
            return {'status': False, 'error_list': error_list}
        insert_review_query = "INSERT INTO reviews (book_id, user_id, content, rating, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(), NOW())"
        review_data = [bookid, loggedin_userid, review['content'], review['rating']]
        self.db.query_db(insert_review_query, review_data)   

        return {'status': True}


    #Delete a given review
    def delete_review(self, reviewid):
        delete_review_query = "DELETE FROM reviews WHERE id = %s"
        self.db.query_db(delete_review_query, [reviewid])
        return



