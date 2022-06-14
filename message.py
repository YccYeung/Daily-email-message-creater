import content
import datetime
from email.message import EmailMessage
import smtplib
import ssl

class DailyDigestEmail:

    def __init__(self):
        self.content = {'quote':{'include': True, 'content': content.get_random_quote()},
                        'weather':{'include': True, 'content': content.get_weather_forecast()},
                        'wiki':{'include': True, 'content': content.get_wikipedia_article()}
                        }

        self.recipients_list = ['email1','email2']

        self.sender_credentials = {'email':'youremail@gmail.com',
                                   'password':'123123'}
    def send_email(self):

        msg = EmailMessage()
        msg['Subject'] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg['From'] = self.sender_credentials['email']
        msg['To'] = self.recipients_list

        msg_body = self.format_message()
        msg.set_content(msg_body['text'])
        msg.add_alternative(msg_body['html'], subtype='html')

        # secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(self.sender_credentials['email'],
                         self.sender_credentials['password'])
            server.send_message(msg)

    def format_message(self):

        ###PlainText Format###
        text = f'*~*~*~*~* Daily Digest - {datetime.date.today().strftime("%b %d %Y")} *~*~*~*~*\n\n'

        if self.content['quote']['include'] and self.content['quote']['content']:
            text += '*~*~* Quote of the Day *~*~*\n'
            text += f'"{self.content["quote"]["content"]["quote"]}" - {self.content["quote"]["content"]["author"]}\n\n'

        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'Weather forecast for next 24 hours\n'
            for forecast in self.content['weather']['content']['periods']:
                text += f'{forecast["timestamp"].strftime("%d %b %H%M")} - {forecast["temp"]}\u00B0C | {forecast["description"]}\n'
            text += '\n'

        if self.content['wiki']['include'] and self.content['wiki']['content']:
            text += f'Wiki article of the day\n'
            text += f'Title: {self.content["wiki"]["content"]["title"]}\nSummary: {self.content["wiki"]["content"]["extract"]}\n' \
                    f'Link to the page: {self.content["wiki"]["content"]["url"]}'

        ###HTML format###

        html = f"""<html>
    <body>
    <center>
        <h1>Daily Digest - {datetime.date.today().strftime('%d %b %Y')}</h1>
        """

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""
        <h2>Quote of the Day</h2>
        <i>"{self.content['quote']['content']['quote']}"</i> - {self.content['quote']['content']['author']}
        """

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['city']}, {self.content['weather']['content']['country']}</h2> 
        <table>
                    """

            for forecast in self.content['weather']['content']['periods']:
                html += f"""
            <tr>
                <td>
                    {forecast['timestamp'].strftime('%d %b %H%M')}
                </td>
                <td>
                    <img src="{forecast['icon']}">
                </td>
                <td>
                    {forecast['temp']}\u00B0C | {forecast['description']}
                </td>
            </tr>
                        """

            html += """
            </table>
                    """

        # format Wikipedia article
        if self.content['wiki']['include'] and self.content['wiki']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h3><a href="{self.content['wiki']['content']['url']}">{self.content['wiki']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wiki']['content']['extract']}</td>
            </tr>
        </table>
                    """

        # footer
        html += """
    </center>
    </body>
</html>
                """

        return {'text': text, 'html': html}

if __name__ == '__main__':
    email = DailyDigestEmail()

    ##### test format_message() #####
    print('\nTesting email body generation...')
    message = email.format_message()

    # print Plaintext and HTML messages
    print('\nPlaintext email body is...')
    print(message['text'])
    print('\n------------------------------------------------------------')
    print('\nHTML email body is...')
    print(message['html'])

    # save Plaintext and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(message['html'])

