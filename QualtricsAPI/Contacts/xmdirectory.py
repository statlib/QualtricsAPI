import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser

class XMDirectory(Credentials):

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id

    def create_contact_in_XM(self, first_name=None, last_name=None, email=None, phone=None, language="en", metadata={}):
        '''This function creates a contact in the XM Directory.

        :param first_name: the contacts first name.
        :param last_name: the contacts last name.
        :param email: the contacts email.
        :param phone: the contacts phone number.
        :param language: the native language of the contact. (Default: English)
        :param metadata: any relevant contact metadata.
        :type metadata: dict
        :return: the contact id (contact_id) in XMDirectory.
        '''
        contact_data = {
            "firstName": str(first_name),
            "lastName": str(last_name),
            "email": str(email),
            "phone": str(phone),
            "language": str(language),
            "embeddedData": metadata,
        }
        headers, base_url = self.header_setup(content_type=True)
        url = base_url + "/contacts"
        response = r.post(url, json=contact_data, headers=headers)
        content = response.json()
        contact_id = content['result']['id']
        return contact_id

    def delete_contact(self,contact_id):
        '''This function will delete a user from IQDirectory.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :return: nothing, but prints if successful, and if there was an error.
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/contacts/{str(contact_id)}"
        response = r.delete(url, headers=headers)
        content = response.json()
        if content['meta']['httpStatus'] == '200 - OK':
            print(f'Your XM Contact"{str(contact_id)}" has been deleted from the XM Directory.')
        else:
            raise ValueError(f"ServerError:{content['meta']['error']['errorCode']}, {content['meta']['error']['errorMessage']}")
        return

    def list_contacts_in_directory(self, page_size=10, offset=0, to_df=True):
        '''This function lists the contacts in the XM Directory.

        :param page_size: determines the start number within the directory for the call.
        :return
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/contacts?pageSize={page_size}&offset={offset}"
        response = r.get(url, headers=headers)
        contacts = response.json()
        contact_list = Parser().json_parser(response=contacts,keys=['contactId','firstName', 'lastName', 'email', 'phone', 'unsubscribed', 'language', 'extRef'])
        col_names = ['contact_id','first_name','last_name','email','phone','unsubscribed','language','external_ref']
        if to_df is True:
            contact_list = pd.DataFrame(contact_list, columns=col_names)
            return contact_list
        else:
            return contact_list

    def get_contact(self, contact_id=None, embedded_data=False):
        ''''''
        #IMprove this
        static_keys = ['contactId', 'creationDate', 'lastModified', 'firstName', 'lastName', 'email', 'emailDomain',
                'phone', 'language', 'writeBlanks', 'extRef', 'transactionData', 'skipped','directoryUnsubscribed',
                'directoryUnsubscribeDate','AvgTimeToRespond', 'DataIntegrity', 'EmailCount', 'InviteCount',
                'LastEmailDate', 'LastInviteDate', 'LastResponseDate', 'MonthEmailCount', 'MonthInviteCount',
                'Points', 'ResponseCount', 'ResponseRate']

        headers, base_url = self.header_setup()
        url = base_url + f'/contacts/{str(contact_id)}'
        response = r.get(url, headers=headers)
        contact = response.json()
        dynamic_keys = self.extract_keys(contact['result']['embeddedData'])
        if embedded_data is False:
            static_elements = self.json_parser(contact, keys)
        #else:
      #      dynamic_elements = self.json_parser()
       #     df = pd.DataFrame(elements).transpose()
       # dynamic_keys = self.extract_keys(contact['result']['embeddedData'])
        #df.columns = keys
        return dynamic_keys

    def get_contact_history(self):
        ''''''

        return
