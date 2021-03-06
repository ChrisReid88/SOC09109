import kivy
from kivy.app import App
from kivy.config import Config
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
import urllib
import json

kivy.require('1.10.0')

# Makes window unable to be fullscreen and sets the size
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '850')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')


class LoginPage(Screen):
    inputStringUsername = ObjectProperty()
    inputStringPassword = ObjectProperty()

    def output_username(self):  # ACCESS TO THE USERNAME FROM LOGIN SCREEN
        print(self.inputStringUsername.text)

    def output_password(self):  # ACCESS TO THE PASSWORD FROM LOGIN SCREEN
        print(self.inputStringPassword.text)

    def username_and_password_check(self, username, password):  # IF STATEMENT TO HANDLE GOOD/BAD LOGIN ATTEMPTS
        if username == " " and password == " ":
            self.manager.current = 'menu'
            self.clear_details()
        else:
            Factory.BadDetailsPopup().open()

    def clear_details(self):
        self.inputStringUsername.text = ""
        self.inputStringPassword.text = ""


class MainMenuPage(Screen):
    pass


class AddFirearmPage(Screen):
    inputStringLicenceNumber: ObjectProperty()
    inputStringTransactionNumber: ObjectProperty()
    inputStringFirearmModel: ObjectProperty()
    inputStringSerialNumber: ObjectProperty()
    inputStringStoreID: ObjectProperty()
    inputStringEmployeeID: ObjectProperty()

    verified = False

    def output_form_details(self, username, password):  # NEED THIS TO CHECK A LIST WITH STORED LOGIN DETAILS
        if username == " " and password == " ":
            self.verified = True
        else:
            Factory.BadDetailsPopup().open()

    def add_to_the_blockchain(self):  # ADD CODE TO ADD INPUT INFO TO THE BLOCK IN THIS FUNCTION
        if self.verified is True:
            # VALUES NEED VALIDATED BEFORE BEING ADDED TO THE BLOCKCHAIN
            # CALL THIS FUNCTION [ Factory.BadDetailsPopup().open() ] IF VALIDATION FAILS

            # FUNCTION TO ACTUALLY ADD VALUES TO THE BLOCKCHAIN NEEDS TO GO HERE
            # TODO: validation
            values = {"licence_no": self.inputStringLicenceNumber.text,
                      "trans_no": self.inputStringTransactionNumber.text,
                      "serial_no": self.inputStringSerialNumber.text,
                      "firearm_model": self.inputStringFirearmModel.text,
                      "store_id": self.inputStringStoreID.text,
                      "emp_id": self.inputStringEmployeeID.text}
            params = json.dumps(values)
            headers = {'Content-type': 'application/json',
                       'Accept': 'text/plain'}
            req = UrlRequest("http://localhost:5000/new", req_body=params, req_headers=headers)
            req.wait()
            print(params)
            print("Added to the block")

            # RESETS THE BOOLEAN VALUE SO MULTIPLES CANNOT BE ADDED
            self.verified = False

            # CLEARS THE TEXTBOXES AFTER DETAILS HAVE BEEN ADDED TO THE BLOCKCHAIN
            self.inputStringLicenceNumber.text = ""
            self.inputStringTransactionNumber.text = ""
            self.inputStringFirearmModel.text = ""
            self.inputStringSerialNumber.text = ""
            self.inputStringStoreID.text = ""
            self.inputStringEmployeeID.text = ""
        else:
            Factory.NotVerifiedPopup().open()

        def add_txn(self):
            pass



class ViewBlockchainPage(Screen):
    outputStringBlockID: ObjectProperty()
    outputStringDate: ObjectProperty()
    outputStringLicenceNumber: ObjectProperty()
    outputStringTransactionNumber: ObjectProperty()
    outputStringFirearmModel: ObjectProperty()
    outputStringSerialNumber: ObjectProperty()
    outputStringStoreID: ObjectProperty()
    outputStringEmployeeID: ObjectProperty()

    #####################################################################################################################
    # FUNCTION TO CALL POPUP FOR MISSING BLOCK !!!!!!!!!
    #Factory.BlockNotFoundPopup().open()
    #####################################################################################################################

    user_selection = "block_id"
    search_string = "te"


    def get_chain(self):
        # Returns the chain from the route
        req = UrlRequest("http://localhost:5000/chain")
        req.wait(delay=0.01)
        return req.result

    def output_to_label(self):

        chain = self.get_chain()
        # Initializing variables to store data from the blocks.
        no_block = True
        index = ""
        date = ""
        # Empty block to display unless the search is successful.
        block = {
            'block_id': '',
            'licence_no': '',
            'trans_no': '',
            'serial_no': '',
            'firearm_model': '',
            'store_id': '',
            'emp_id': ''
        }

        # Searches through all the data in the blockchain
        for items in chain["chain"]:
            for item in items["data"]:
                if self.search_string == str(items["index"]):
                    # If the value being searched is the index, return the block associated with the block_id.
                    # No_block set to false to call the 'Not found' pop up box.
                    print("PASSED")
                    block = item
                    index = items["index"]
                    date = items["timestamp"]
                    no_block = False
                elif self.user_selection != "block_id":
                    if item[self.user_selection] == self.search_string:
                        # If it is not block_id and the key value is found return the block with the details.
                        # No_block set to false to call the 'Not found' pop up box.
                        index = items["index"]
                        date = items["timestamp"]
                        print(date)
                        block = item
                        no_block = False

        # Search returned nothing, display the pop up.
        if no_block is True:
            Factory.BlockNotFoundPopup().open()

        # Fill the text boxes with the block data.
        self.outputStringBlockID.text = str(index)
        self.outputStringDate.text = str(date)
        self.outputStringLicenceNumber.text = block["licence_no"]
        self.outputStringTransactionNumber.text = block["trans_no"]
        self.outputStringFirearmModel.text = block["firearm_model"]
        self.outputStringSerialNumber.text = block["serial_no"]
        self.outputStringStoreID.text = block["store_id"]
        self.outputStringEmployeeID.text = block["emp_id"]

    def next_block(self):
        print("NEXT BLOCK SHOWS")

    def previous_block(self):
        print("PREVIOUS BLOCK SHOWS")

    def user_search_input(self, searchString):
        if searchString != "":
            self.search_string = searchString
            self.output_to_label()

    def selected_search_field_block_id(self, state):
        if state:
            self.user_selection = "block_id"

    def selected_search_field_licence_no(self, state):
        if state:
            self.user_selection = "licence_no"

    def selected_search_field_transaction_no(self, state):
        if state:
            self.user_selection = "trans_no"

    def selected_search_field_serial_no(self, state):
        if state:
            self.user_selection = "serial_no"

    def selected_search_field_firearm_model(self, state):
        if state:
            self.user_selection = "firearm_model"

    def selected_search_field_store_id(self, state):
        if state:
            self.user_selection = "store_id"

    def selected_search_field_employee_id(self, state):
        if state:
            self.user_selection = "emp_id"

class Manager(ScreenManager):
    screen_one = ObjectProperty(None)  # Login Page
    screen_two = ObjectProperty(None)  # Main Menu Page
    screen_three = ObjectProperty(None)  # Add Firearm Page
    screen_four = ObjectProperty(None)  # View Blockchain Page


class GroupProjectApp(App):

    def build(self):
        m = Manager(transition=WipeTransition())
        return m


if __name__ == '__main__':
    GroupProjectApp().run()
