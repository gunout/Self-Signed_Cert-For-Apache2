# Self-Signed_Cert-For-Apache2
Config SSL _ Self Signed Certificate with Python3

Étapes à suivre manuellement avant d'utiliser le script :

Vérifie que Apache2 est installé sur ton serveur. Si ce n'est pas déjà fait :
    sudo apt update
    sudo apt install apache2

Vérifie si Apache est activé et fonctionne :
    sudo systemctl start apache2
    sudo systemctl enable apache2

Installe OpenSSL si ce n'est pas déjà fait : OpenSSL est nécessaire pour créer un certificat SSL auto-signé :
    sudo apt install openssl

