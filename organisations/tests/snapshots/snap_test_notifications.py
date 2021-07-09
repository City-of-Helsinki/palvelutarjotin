# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_myprofile_creation_email 1"] = [
    """no-reply@hel.ninja|['xrubio@yahoo.com']|My profile creation FI|
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
    <li>Bell, Price and Dixon</li>
    <li>Perry Ltd</li>
</ul>
<p>Muokataksesi luotua käyttäjätunnusta,
klikkaa <a href="http://localhost/admin/organisations/user/123/change/" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa
<a href="http://localhost/admin/organisations/user/" target="_blank">tästä</a>.</p>""",
    """no-reply@hel.ninja|['brownheather@villarreal.com']|My profile creation FI|
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
    <li>Bell, Price and Dixon</li>
    <li>Perry Ltd</li>
</ul>
<p>Muokataksesi luotua käyttäjätunnusta,
klikkaa <a href="http://localhost/admin/organisations/user/123/change/" target="_blank">tästä</a>!</p>
<p>Nähdäksesi listan käyttäjistä, klikkaa
<a href="http://localhost/admin/organisations/user/" target="_blank">tästä</a>.</p>""",
]
