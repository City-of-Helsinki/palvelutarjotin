import pytest
from organisations.consts import NotificationTemplate

from common.tests.utils import create_notification_template_in_language

DEFAULT_NOTIFICATION_BODY_TEXT_FI = """
<p>Hyvä Kultus ylläpitäjä!</p>
<p>Uusi palveluntarjoajan tunnus on luotu!</p>
<address>
    {{person.name}}<br />
    <a href="mailto:{{person.email_address}}">{{person.email_address}}</a>
    Käyttäjätunnus: {{person.user.username}}
</address>
<p>Palveluntarjoaja tarvitsee ylläpitäjää (sinua)
hyväksymään luomansa käyttäjätunnuksen käyttöön:</p>
<ol>
    <li>Luo puuttuvat organisaatiot LinkedEventsiin</li>
    <li>Luo puuttuvat organisaatiot Kultukseen</li>
    <li>Liitä organisaatiot käyttäjään</li>
    <li>Lisää käyttäjälle staff-lippu, jotta hän saisi oikeudet
    luoda ja muokata tapahtumia.</li>
</ol>
<p>Käyttäjä haluaisi edustaa seuraavia organisaatioita:</p>
<ul>
    {% for organisation in person.organisationproposal_set.all() %}
    <li>{{organisation.name}}</li>
    {% endfor %}
</ul>
<p>Muokataksesi luotua käyttäjätunnusta,
klikkaa <a href="#" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa <a href="#" target="_blank">tästä</a>.</p>
"""

NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI = (
    DEFAULT_NOTIFICATION_BODY_TEXT_FI
    + """
    {% if custom_message %}
    Erityisviesti: {{ custom_message }}
    {% endif %}
"""
)

NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_FI = (
    "<p>" + NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI + "</p>"
)

DEFAULT_NOTIFICATION_BODY_TEXT_EN = """
<p>Dear Kultus Admin!</p>
<p>A new Kultus provider user profile is created!</p>
<address>
    {{person.name}}<br />
    <a href="mailto:{{person.email_address}}">{{person.email_address}}</a>
    Username: {{person.user.username}}
</address>
<p>The provider who created the user profile needs an admin (you)
to accept the user profile:</p>
<ol>
    <li>Create the missing organisations to LinkedEvents</li>
    <li>Create the missing organisations to Kultus</li>
    <li>Link the user to organisations</li>
    <li>Set the staff -flag so the user would receive the permissions
    to create and edit their events.</li>
</ol>
<p>The user would like to represent these organisations:</p>
<ul>
    {% for organisation in person.organisationproposal_set.all() %}
    <li>{{organisation.name}}</li>
    {% endfor %}
</ul>
<p>To edit the newly created user profile,
click <a href="#" target="_blank">here</a>!</p>
<p>To see a full list of users, click <a href="#" target="_blank">here</a>.</p>
"""

NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN = (
    DEFAULT_NOTIFICATION_BODY_TEXT_EN
    + """
    {% if custom_message %}
    Custom message: {{ custom_message }}
    {% endif %}
"""
)

NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_EN = (
    "<p>" + NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN + "</p>"
)


@pytest.fixture
def notification_template_myprofile_creation_fi():
    return create_notification_template_in_language(
        NotificationTemplate.MYPROFILE_CREATION,
        "fi",
        subject="My profile creation FI",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_FI,
    )


@pytest.fixture
def notification_template_myprofile_creation_en():
    return create_notification_template_in_language(
        NotificationTemplate.MYPROFILE_CREATION,
        "en",
        subject="My profile creation EN",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_EN,
    )
