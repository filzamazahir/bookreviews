"""
    Routes Configuration File
"""
from system.core.router import routes


routes['default_controller'] = 'Users'
routes['POST']['/users/login'] = 'Users#login'
routes['POST']['/users/register'] = 'Users#register'
routes ['/users/<int:id>'] = 'Users#show'
routes['/users/logoff'] = 'Users#logoff'
routes['/books'] = 'Books#index'
routes['/books/new'] = 'Books#new'
routes['/books/<int:bookid>'] = 'Books#show'
routes['POST']['/books/create'] = 'Books#create_book_review'
routes['POST']['/books/create_review/<int:bookid>'] = 'Books#create_review'
routes['/books/delete/<int:bookid>/<int:reviewid>'] = 'Books#destroy_review'







"""
    You can add routes and specify their handlers as follows:

    routes['VERB']['/URL/GOES/HERE'] = 'Controller#method'

    Note the '#' symbol to specify the controller method to use.
    Note the preceding slash in the url.
    Note that the http verb must be specified in ALL CAPS.
    
    If the http verb is not provided pylot will assume that you want the 'GET' verb.

    You can also use route parameters by using the angled brackets like so:
    routes['PUT']['/users/<int:id>'] = 'users#update'

    Note that the parameter can have a specified type (int, string, float, path). 
    If the type is not specified it will default to string

    Here is an example of the restful routes for users:

    routes['GET']['/users'] = 'users#index'
    routes['GET']['/users/new'] = 'users#new'
    routes['POST']['/users'] = 'users#create'
    routes['GET']['/users/<int:id>'] = 'users#show'
    routes['GET']['/users/<int:id>/edit' = 'users#edit'
    routes['PATCH']['/users/<int:id>'] = 'users#update'
    routes['DELETE']['/users/<int:id>'] = 'users#destroy'
"""
