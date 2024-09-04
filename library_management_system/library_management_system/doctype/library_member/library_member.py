# Copyright (c) 2024, seraj and contributors
# For license information, please see license.txt

#import frappe
from frappe.model.document import Document


class LibraryMember(Document):
    #this method will run every time a document is saved
    def before_save(self):
        self.full_name = f'{self.first_name} {self.last_name or ""}'
        


        # @frappe.whitelist()
        # def get_valid_membership(library_member):
        #     is_valid = frappe.db.get_value("Library Member", library_member, "is_membership_valid")
        #     return is_valid
