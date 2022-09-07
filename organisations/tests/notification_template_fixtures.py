import pytest

from common.tests.utils import create_notification_template_in_language
from organisations.consts import NotificationTemplate

MYPROFILE_CREATED_NOTIFICATION_BODY_TEXT_FI = """
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
klikkaa <a href="{{user_change_form_url}}" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa
<a href="{{user_list_url}}" target="_blank">tästä</a>.</p>
"""

MYPROFILE_CREATED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI = (
    MYPROFILE_CREATED_NOTIFICATION_BODY_TEXT_FI
    + """
    {% if custom_message %}
    <p>Erityisviesti: {{ custom_message }}</p>
    {% endif %}
"""
)


MYPROFILE_CREATED_NOTIFICATION_BODY_TEXT_EN = """
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
click <a href="{{user_change_form_url}}" target="_blank">here</a>!</p>
<p>To see a full list of users, click
<a href="{{user_list_url}}" target="_blank">here</a>.</p>
"""

MYPROFILE_CREATED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN = (
    MYPROFILE_CREATED_NOTIFICATION_BODY_TEXT_EN
    + """
    {% if custom_message %}
    <p>Custom message: {{ custom_message }}</p>
    {% endif %}
"""
)


@pytest.fixture
def notification_template_myprofile_creation_fi():
    return create_notification_template_in_language(
        NotificationTemplate.MYPROFILE_CREATION,
        "fi",
        subject="My profile creation FI",
        body_text=MYPROFILE_CREATED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
    )


@pytest.fixture
def notification_template_myprofile_creation_en():
    return create_notification_template_in_language(
        NotificationTemplate.MYPROFILE_CREATION,
        "en",
        subject="My profile creation EN",
        body_text=MYPROFILE_CREATED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
    )


MYPROFILE_ACCEPTED_NOTIFICATION_BODY_TEXT_FI = """
<p>Hei {{person.name}}!</p>
<p>Sinun käyttäjäsi on nyt valmis käytettäväksi Kultuksessa
seuraavilla organisaatioille:</p>
<ul>
    {% for organisation in person.organisations.all()%}
    <li>{{organisation.name}}</li>
    {% endfor %}
</ul>
"""
MYPROFILE_ACCEPTED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI = (
    MYPROFILE_ACCEPTED_NOTIFICATION_BODY_TEXT_FI
    + """
    {% if custom_message %}
    <p>Erityisviesti: {{ custom_message }}</p>
    {% endif %}
    """
)

MYPROFILE_ACCEPTED_NOTIFICATION_BODY_TEXT_EN = """
<p>Hi {{person.name}}!</p>
<p>Your account is now ready to be used in Kultus
with the following organisations linked to your account:</p>
<ul>
    {% for organisation in person.organisations.all()%}
    <li>{{organisation.name}}</li>
    {% endfor %}
</ul>
"""
MYPROFILE_ACCEPTED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN = (
    MYPROFILE_ACCEPTED_NOTIFICATION_BODY_TEXT_EN
    + """
    {% if custom_message %}
    <p>Custom message: {{ custom_message }}</p>
    {% endif %}
    """
)


@pytest.fixture
def notification_template_myprofile_accepted_fi():
    return create_notification_template_in_language(
        NotificationTemplate.MYPROFILE_ACCEPTED,
        "fi",
        subject="My profile accepted FI",
        body_text=MYPROFILE_ACCEPTED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
    )


@pytest.fixture
def notification_template_myprofile_accepted_en():
    return create_notification_template_in_language(
        NotificationTemplate.MYPROFILE_ACCEPTED,
        "en",
        subject="My profile accepted EN",
        body_text=MYPROFILE_ACCEPTED_NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
    )
