# Copyright 2015 by Toben "Narcolapser" Archer. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its documentation for any purpose 
# and without fee is hereby granted, provided that the above copyright notice appear in all copies and 
# that both that copyright notice and this permission notice appear in supporting documentation, and 
# that the name of Toben Archer not be used in advertising or publicity pertaining to distribution of 
# the software without specific, written prior permission. TOBEN ARCHER DISCLAIMS ALL WARRANTIES WITH 
# REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT 
# SHALL TOBEN ARCHER BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES 
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE 
# OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from contact import Contact
import logging
import json
import requests

logging.basicConfig(filename='o365.log',level=logging.DEBUG)

log = logging.getLogger(__name__)

class Group( object ):
	'''
	A wrapper class that handles all the contacts associated with a single Office365 account.
	
	Methods:
		constructor -- takes your email and password for authentication.
		getContactss -- begins the actual process of downloading contacts.
	
	Variables:
		con_url -- the url that is requested for the retrival of the contacts.
	'''
	con_url = 'https://outlook.office365.com/api/v1.0/me/contacts'

	def __init__(self, email, password):
		'''Creates a group class for managing all contacts associated with email+password.'''
		log.debug('setting up for the schedule of the email %s',email)
		self.auth = (email,password)
		self.contacts = []


	def getContact(self):
		'''Begin the process of downloading contact metadata.'''
		log.debug('fetching contacts.')
		response = requests.get(self.con_url,auth=self.auth)
		log.info('Response from O365: %s', str(response))

		for contact in response.json()['value']:
			duplicate = False
			log.debug('Got a contact Named: {0}'.format(contact['DisplayName']))
			for existing in self.contacts:
				if existing.json['Id'] == contact['Id']:
					log.info('duplicate contact')
					duplicate = True
					break

			if not duplicate:
				self.contacts.append(Contact(contact,self.auth))
			
			log.debug('Appended Contact.')
				
			
		log.debug('all calendars retrieved and put in to the list.')
		return True

#To the King!