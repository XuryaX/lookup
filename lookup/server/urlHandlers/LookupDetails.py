'''
Created on May 17, 2016

@author: Shauryadeep Chaudhuri
'''
import tornado


class LookupDetails(tornado.web.RequestHandler):
    '''
    classdocs
    '''

    def get(self):
        response = {
            'author': 'Shauryadeep Chaudhuri',
            'contact': 'shauryadeepc@hotmail.com',
            'version': '0.2 Aplha'}
        self.write(response)
