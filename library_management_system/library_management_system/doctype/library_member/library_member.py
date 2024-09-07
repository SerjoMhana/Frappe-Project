# Copyright (c) 2024, seraj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):
    #this method will run every time a document is saved
    def before_save(self):
        self.full_name = f'{self.first_name} {self.last_name or ""}'
        
    def on_submit(self):
        try:
            self.create_customer(self.name, self.first_name, self.last_name)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Error creating Customer for Library Member {self.name}")
            frappe.throw(title="LMS ERROR", msg=f"Error creating Customer for Library Member {self.name}: {e}")

    def create_customer(self, library_member_name: str, first_name: str, last_name: str) -> str:
        try:
            # Create a new Customer document
            customer = frappe.new_doc("Customer")
            customer.customer_name = f"{first_name} {last_name}"
            customer.custom_is_library_member = 1  # Set the custom field to True
            customer.custom_lms_library_member = library_member_name  # Link to the Library Member
            customer.insert()
            frappe.msgprint(f"Customer '{customer.customer_name}' created successfully.")
            return customer.name
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Error creating Customer for Library Member {library_member_name}")
            frappe.throw(title="LMS ERROR", msg=f"Error creating Customer for Library Member {library_member_name}: {e}")
            return None
                
                
