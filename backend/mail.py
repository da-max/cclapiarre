"""
Source : https://stackoverflow.com/a/4447147
Thanks !
"""
import threading
from threading import Thread

from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    """ This class create Thread for send async mail.

    Attributes
    ----------
    subject : str
      Subject of the mail.
    html_content : str
      Body of the mail, support html.
    recipient_list : list
      List of recipient of the mail.

    """

    def __init__(self, subject: str, html_content: str, recipient_list: list) -> None:
        self.subject = subject
        self.html_content = html_content
        self.recipient_list = recipient_list
        super().__init__()

    def run(self):
        msg = EmailMessage(self.subject, self.html_content,
                           to=self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()


def async_send_mail(subject: str, html_content: str, recipient_list: list) -> None:
    """ Function for create and start EmailThread.

    Parameters
    ----------
    subject : str
      Subject of the mail.
    html_content : str
      Body of the mail.
    recipient_list : list
      List of recipient.

    """
    EmailThread(subject, html_content, recipient_list).start()
