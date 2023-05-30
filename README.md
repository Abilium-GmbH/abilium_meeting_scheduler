<h1>ReadMe für die Simple-Booking-App for Odoo</h1>
<h2>PSE-Team</h2>
<ul>
  <li>Chief Deliverable Officers: Sandro Calce, Matthias Dani</li>
  <li>Key Account Manager: Nils Neeb</li>
  <li>Master Tracker: Luc Vuilleumier</li>
  <li>Quality Evengalists: Tim Kuhn, Valerio Vontobel</li>
</ul>

<h2>Ziel</h2>
<ul>
    Das Projektziel ist die Entwicklung und Prüfung eines Odoo-Plugins.
    Das Plugin enthält ein Konfigurationsformular für die verfügbaren Zeitfenster und ein Webseitenformular, 
    über das Kunden einen geeigneten Termin auswählen können. Eine Terminbestätigung schließt den Prozess ab. 
    Zusätzlich wird eine Integration von Odoo mit der Telegram Bot API entwickelt, 
    um interne Benachrichtigungen über den Telegram Messenger zu ermöglichen.
</ul>

<h2>Installation</h2>
<ul>
   Um die Simple Booking App zu installieren sind folgende Vorbedingungen zu erfüllen:
<br/><br/> 
<li><a href = "https://www.odoo.com/documentation/14.0/administration/install.html">Odoo 14.0</a> muss installiert sein und funktionieren</li>
<br/><br/>
   Installation:
<br/><br/>

1.	Simple Booking App Code von Github herunterladen
2.	ZIP-Datei entpacken
3.	Alle Inhalte der ZIP-Datei in den Ordner odoo/addons verschieben
4.	Den abilium_meeting_scheduler-main umbenennen zu «meeting_scheduler»  
5.	Odoo starten
6.	Das Modul «Calendar» installieren
7.	Das Modul «Meeting Scheduler» installieren
<br/><br/>
Nach der erfolgreichen Installation der Simple Booking App sollte ein neues Feld mit dem Namen "Meeting Scheduler" im Dropdown-Menü erscheinen. 
Durch Anklicken gelangt man zur Startseite des Moduls "Meeting Scheduler".
Für eine detaillierte Anleitung zur Nutzung des Moduls steht eine Dokumentation zur Verfügung.
</ul>

<h2>Dokumentation</h2>
<ul>
   <li>Funktionalitäten, Verwendung und Ressourcen/Referenzen finden sie im <a href = "https://github.com/Abilium-GmbH/abilium_meeting_scheduler/blob/Dokumentation/Dokumentation/Manual_DE.pdf">Manual-DE</a></li>  
</ul>

<h2>Testing</h2>
<ul>
   <li>Hier noch eine Anleitung zum Unit Testing:<a href = "https://github.com/Abilium-GmbH/abilium_meeting_scheduler/blob/Dokumentation/Dokumentation/Unit%20Testing%20Guide%20-%20V7.pdf">Unit Testing Guide - V7</a></li>  
</ul>

<h2>Version</h2>
<ul>
   <li>Simple-Booking-App for Odoo, Alpha 1.0</li> 
</ul>