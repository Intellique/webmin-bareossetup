# webmin-bareossetup

This is a webmin module to automatically add client machines to a bareos backup server director configuration.

Cet outil nécessite Webmin et Bareos. Préalablement, installez [Webmin](http://webmin.com) et [Bareos](http://bareos.org).
Configurez et lancez le serveur Bareos.


**Installation du module**

Testé uniquement sur un serveur Webmin/Bareos Debian 8 Jessie.

Clonez le dépôt webmin-bareossetup.

Dans les scripts bareos-client-install et BareosClientInstall.ps1, remplacez le nom du serveur par le nom ou l'adresse IP de votre serveur.

Exportez le dépôt dans un fichier tar (à tester):

  `git archive master > bareossetup.wbm`
  
Dans Webmin, section *Webmin*, *Modules*, choisissez *Installer un module depuis un fichier local*, choisissez le fichier *bareossetup.wbm*.

**Configuration de Webmin**

Créez un utilisateur *bareos* n'ayant accès qu'au module *bareossetup*.
Dans la section *Webmin* -> *Accès anonyme aux modules*, ajoutez le chemin */bareossetup/* et choisissez d'accéder en tant qu'utilisateur *bareos*.

Vérifiez que vous accédez bien au module en pointant un navigateur vers
`https://<serveur>:10000/bareossetup/index.cgi`

Il ne doit pas être demandé de mot de passe.

**Utilisation du module**

 * depuis un poste Linux:
 
 `curl -k https://<serveur>:10000/bareossetup/bareos-client-install | sudo bash`
 
 * depuis un poste Windows (à préciser):

 `curl -k https://<serveur>:10000/bareossetup/BareosClientInstall.ps1 `
 

