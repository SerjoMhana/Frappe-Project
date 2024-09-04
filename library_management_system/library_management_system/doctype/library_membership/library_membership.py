import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe import db, utils

class LibraryMembership(Document):
    def validate(self):
        # Check for existing active memberships, excluding the current document
        if self.library_member:  # Only check if library_member is set
            existing_membership = frappe.db.exists(
                "Library Membership",
                {
                    "library_member": self.library_member,
                    "docstatus": DocStatus.submitted(),
                    "name": ("!=", self.name), 
                },
            )
            if existing_membership:
                frappe.throw("There is already an active membership for this member.")

    def before_submit(self):
        # This will handle cases where the membership is created and submitted directly
        if self.paid: 
            self.update_library_member_validity(True)

    def on_update(self):
        # This will handle cases where the 'paid' field is updated after submission
        if self.paid:
            self.update_library_member_validity(True)

    def on_cancel(self):
        # Uncheck "Is Membership Valid" if membership is canceled
        self.update_library_member_validity(False)

    def update_library_member_validity(self, is_valid):
        if self.library_member:
            frappe.db.set_value(
                "Library Member", 
                self.library_member, 
                "is_membership_valid", 
                is_valid
            )