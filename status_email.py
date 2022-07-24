import smtplib
from configuration import Configuration


class StatusEmail:
    """"Status email class used send email messages for status updates."""

    def __init__(self):
        """Method to initialize the status email class."""

        # Get the configuration from the configuration file.
        self.configuration = Configuration().get_configuration()

        # The email host used to send the email message.
        self.host = self.configuration["email"]["host"]

        # The email host port number.
        self.port = self.configuration["email"]["port"]

        # The email sender.
        self.sender = self.configuration["email"]["sender"]

        # The email sender password.
        self.password = self.configuration["email"]["password"]

        # The email recipients list.
        self.recipients = self.configuration["email"]["updateRecipients"]

    def send_email(self, subject, body):
        """Method used to send an email.

        :param subject: The email message subject.
        :param body: The email message body.
        """

        # Try with the SMTP connection as a resource to connect the the SMTP server.
        with smtplib.SMTP_SSL(self.host, self.port) as smtp_server:

            # Login to the SMTP server.
            smtp_server.login(self.sender, self.password)

            # Build the message
            message = f"Subject: {subject}\n\n{body}"

            # Send the email.
            smtp_server.sendmail(self.sender, self.recipients, message)
