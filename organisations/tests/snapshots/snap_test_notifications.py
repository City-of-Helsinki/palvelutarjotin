# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_myprofile_accepted_email[en] 1"] = [
    """no-reply@hel.ninja|['sreyes@example.com']|My profile accepted EN|
<p>Hi Kyle Walls!</p>
<p>Your account is now ready to be used in Kultus
with the following organisations linked to your account:</p>
<ul>
    <li>Graves and Sons</li>
    <li>Valdez-Thompson</li>
</ul>

    <p>Custom message: custom message</p>
    """
]

snapshots["test_myprofile_accepted_email[fi] 1"] = [
    """no-reply@hel.ninja|['sreyes@example.com']|My profile accepted FI|
<p>Hei Kyle Walls!</p>
<p>Sinun käyttäjäsi on nyt valmis käytettäväksi Kultuksessa
seuraavilla organisaatioille:</p>
<ul>
    <li>Graves and Sons</li>
    <li>Valdez-Thompson</li>
</ul>

    <p>Erityisviesti: custom message</p>
    """
]

snapshots["test_myprofile_creation_email 1"] = [
    """no-reply@hel.ninja|['jennifer62@example.org']|My profile creation FI|
<p>Hyvä Kultus ylläpitäjä!</p>
<p>Uusi palveluntarjoajan tunnus on luotu!</p>
<address>
    Amanda Newton<br />
    <a href="mailto:hutchinsonrachel@example.org">hutchinsonrachel@example.org</a>
    Käyttäjätunnus: jeffersonkimberly_3MmHFh
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
    <li>Smith, Wood and Baker</li>
    <li>Wolfe, Rogers and Morgan</li>
</ul>
<p>Muokataksesi luotua käyttäjätunnusta,
klikkaa <a href="https://test-domain/admin/organisations/user/123/change/" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa
<a href="https://test-domain/admin/organisations/user/" target="_blank">tästä</a>.</p>

    <p>Erityisviesti: custom message</p>
""",
    """no-reply@hel.ninja|['lsimmons@example.com']|My profile creation FI|
<p>Hyvä Kultus ylläpitäjä!</p>
<p>Uusi palveluntarjoajan tunnus on luotu!</p>
<address>
    Amanda Newton<br />
    <a href="mailto:hutchinsonrachel@example.org">hutchinsonrachel@example.org</a>
    Käyttäjätunnus: jeffersonkimberly_3MmHFh
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
    <li>Smith, Wood and Baker</li>
    <li>Wolfe, Rogers and Morgan</li>
</ul>
<p>Muokataksesi luotua käyttäjätunnusta,
klikkaa <a href="https://test-domain/admin/organisations/user/123/change/" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa
<a href="https://test-domain/admin/organisations/user/" target="_blank">tästä</a>.</p>

    <p>Erityisviesti: custom message</p>
""",
    """no-reply@hel.ninja|['patrickkenneth@example.com']|My profile creation EN|
<p>Dear Kultus Admin!</p>
<p>A new Kultus provider user profile is created!</p>
<address>
    Amanda Newton<br />
    <a href="mailto:hutchinsonrachel@example.org">hutchinsonrachel@example.org</a>
    Username: jeffersonkimberly_3MmHFh
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
    <li>Smith, Wood and Baker</li>
    <li>Wolfe, Rogers and Morgan</li>
</ul>
<p>To edit the newly created user profile,
click <a href="https://test-domain/admin/organisations/user/123/change/" target="_blank">here</a>!</p>
<p>To see a full list of users, click
<a href="https://test-domain/admin/organisations/user/" target="_blank">here</a>.</p>

    <p>Custom message: custom message</p>
""",
]
