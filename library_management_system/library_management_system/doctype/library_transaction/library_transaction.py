import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            # set the article status to be Issued
            article = frappe.get_doc("Article", self.article)
            article.status = "Issued"
            article.save()

        elif self.type == "Return":
            self.validate_return()
            # set the article status to be Active
            article = frappe.get_doc("Article", self.article)
            article.status = "Active"
            article.save()

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # article cannot be issued if it is already issued
        if article.status == "Issued":
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # article cannot be returned if it is not issued first
        if article.status == "Active":
            frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Issue", "docstatus": DocStatus.submitted()},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exist for this library member
        existing_membership = frappe.db.exists(
                "Library Membership",
                {
                    "library_member": self.library_member,
                    "docstatus": DocStatus.submitted(),
                    "name": ("!=", self.name), 
                },
            )
        if not existing_membership:
            frappe.throw("The member does not have a valid membership")



def __init__(self, *args, **kwargs):
        super(LibraryTransaction, self).__init__(*args, **kwargs)
        self.fields_dict["library_member"].get_query = self.get_valid_library_members

        def get_valid_library_members(self, doctype, txt, searchfield, start, page_len, filters):
            filters = {"is_membership_valid": 1} 
            if txt:
                filters["name"] = ("like", f"%{txt}%")  # Apply search filter only if txt is provided
        return frappe.db.get_all(
            "Library Member",
            filters=filters,
            fields=["name as value", "member_name as label"], 
            limit_start=start,
            limit_page_length=page_len,
            order_by="name",
        )




