import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryTransaction(Document):
    def before_submit(self):
        if self.transaction_type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            # Set the article status to Inactive (since it's issued)
            article = frappe.get_doc("Article", self.article)
            article.status = "Inactive"
            article.save()
            frappe.db.commit()  # Ensure the status change is committed to the database
            frappe.log_error(f"Article {article.name} status changed to Inactive", "Library Transaction")

        elif self.transaction_type == "Return":
            self.validate_return()
            # Set the article status to Active (since it's returned)
            article = frappe.get_doc("Article", self.article)
            article.status = "Active"
            article.save()
            frappe.db.commit()  # Ensure the status change is committed to the database
            frappe.log_error(f"Article {article.name} status changed to Active", "Library Transaction")

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # Article cannot be issued if it is already inactive (issued)
        if article.status == "Inactive":
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # Article cannot be returned if it is Active (not issued)
        if article.status == "Active":
            frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Management Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "transaction_type": "Issue", "docstatus": DocStatus.submitted()},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # Check if a valid membership exists for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<=", self.transaction_date),
                "to_date": (">=", self.transaction_date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
