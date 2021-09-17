# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_myprofile_creation_email 1"] = [
    """no-reply@hel.ninja|['fmartinez@hotmail.com']|My profile creation FI|
<p>Hyvä Kultus ylläpitäjä!</p>
<p>Uusi palveluntarjoajan tunnus on luotu!</p>
<address>
    William Brewer<br />
    <a href="mailto:stephanieskinner@gmail.com">stephanieskinner@gmail.com</a>
    Käyttäjätunnus: ariley
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
    <li>Bartlett and Sons</li>
    <li>Thomas, Ochoa and Peters</li>
</ul>
<p>Muokataksesi luotua käyttäjätunnusta,
klikkaa <a href="https://test-domain/admin/organisations/user/123/change/" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa
<a href="https://test-domain/admin/organisations/user/" target="_blank">tästä</a>.</p>

    <p>Erityisviesti: custom message</p>
""",
    """no-reply@hel.ninja|['velezsusan@hotmail.com']|My profile creation FI|
<p>Hyvä Kultus ylläpitäjä!</p>
<p>Uusi palveluntarjoajan tunnus on luotu!</p>
<address>
    William Brewer<br />
    <a href="mailto:stephanieskinner@gmail.com">stephanieskinner@gmail.com</a>
    Käyttäjätunnus: ariley
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
    <li>Bartlett and Sons</li>
    <li>Thomas, Ochoa and Peters</li>
</ul>
<p>Muokataksesi luotua käyttäjätunnusta,
klikkaa <a href="https://test-domain/admin/organisations/user/123/change/" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa
<a href="https://test-domain/admin/organisations/user/" target="_blank">tästä</a>.</p>

    <p>Erityisviesti: custom message</p>
""",
    """no-reply@hel.ninja|['deborah29@hotmail.com']|My profile creation EN|
<p>Dear Kultus Admin!</p>
<p>A new Kultus provider user profile is created!</p>
<address>
    William Brewer<br />
    <a href="mailto:stephanieskinner@gmail.com">stephanieskinner@gmail.com</a>
    Username: ariley
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
    <li>Bartlett and Sons</li>
    <li>Thomas, Ochoa and Peters</li>
</ul>
<p>To edit the newly created user profile,
click <a href="https://test-domain/admin/organisations/user/123/change/" target="_blank">here</a>!</p>
<p>To see a full list of users, click
<a href="https://test-domain/admin/organisations/user/" target="_blank">here</a>.</p>

    <p>Custom message: custom message</p>
""",
]

snapshots["test_myprofile_accepted_email[fi] 1"] = [
    """no-reply@hel.ninja|['patrick24@yahoo.com']|My profile accepted FI|
<p>Hei Amanda George!</p>
<p>Sinun käyttäjäsi on nyt valmis käytettäväksi Kultuksessa
seuraavilla organisaatioille:</p>
<ul>
    <li>Black Ltd</li>
    <li>Burns, Gomez and Roach</li>
</ul>

    <p>Erityisviesti: custom message</p>
    """
]

snapshots["test_myprofile_accepted_email[en] 1"] = [
    """no-reply@hel.ninja|['patrick24@yahoo.com']|My profile accepted EN|
<p>Hi Amanda George!</p>
<p>Your account is now ready to be used in Kultus
with the following organisations linked to your account:</p>
<ul>
    <li>Black Ltd</li>
    <li>Burns, Gomez and Roach</li>
</ul>

    <p>Custom message: custom message</p>
    """
]
