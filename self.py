import subprocess
import os

# Variables
domain = "ton_domaine.com"  # Remplace par ton domaine ou ton IP publique
ssl_dir = "/etc/ssl/certs"  # Dossier où les certificats SSL seront stockés
key_dir = "/etc/ssl/private"  # Dossier où la clé privée sera stockée
config_file = "/etc/apache2/sites-available/default-ssl.conf"  # Fichier de configuration SSL d'Apache

# 1. Créer le certificat SSL auto-signé et la clé privée
def create_ssl_cert():
    print("Création du certificat SSL auto-signé et de la clé privée...")
    
    # Générer la clé privée
    subprocess.run(["sudo", "openssl", "genpkey", "-algorithm", "RSA", "-out", os.path.join(key_dir, "apache.key")])
    
    # Générer le certificat SSL auto-signé
    subprocess.run([
        "sudo", "openssl", "req", "-new", "-x509", "-key", os.path.join(key_dir, "apache.key"),
        "-out", os.path.join(ssl_dir, "apache.crt"), "-days", "365", 
        "-subj", "/C=FR/ST=Region/L=City/O=Company/OU=Org/CN={}".format(domain)
    ])
    
    print("Certificat SSL et clé privée générés avec succès.")

# 2. Configurer Apache pour utiliser SSL
def configure_apache_ssl():
    print("Configuration d'Apache pour SSL...")
    
    # Activer les modules nécessaires
    subprocess.run(["sudo", "a2enmod", "ssl"])
    subprocess.run(["sudo", "a2enmod", "rewrite"])
    
    # Activer le site SSL
    subprocess.run(["sudo", "a2ensite", "default-ssl.conf"])
    
    # Modifier la configuration SSL pour pointer vers les fichiers de certificat
    with open(config_file, "r") as file:
        config_data = file.read()
    
    # Remplacer les chemins des certificats dans la configuration Apache
    config_data = config_data.replace("SSLCertificateFile    /etc/ssl/certs/ssl-cert-snakeoil.pem",
                                      "SSLCertificateFile    {}".format(os.path.join(ssl_dir, "apache.crt")))
    config_data = config_data.replace("SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key",
                                      "SSLCertificateKeyFile {}".format(os.path.join(key_dir, "apache.key")))
    
    with open(config_file, "w") as file:
        file.write(config_data)
    
    print("Configuration Apache pour SSL terminée.")

# 3. Redémarrer Apache pour appliquer les modifications
def restart_apache():
    print("Redémarrage d'Apache pour appliquer les modifications...")
    subprocess.run(["sudo", "systemctl", "restart", "apache2"])
    print("Apache redémarré avec succès.")

# 4. Tester la configuration
def test_ssl():
    print("Test de la configuration SSL...")
    subprocess.run(["sudo", "apache2ctl", "configtest"])
    print("Test de la configuration réussi.")

# Fonction principale pour exécuter tout le processus
def main():
    # Créer le certificat SSL auto-signé
    create_ssl_cert()
    
    # Configurer Apache pour utiliser le certificat SSL
    configure_apache_ssl()
    
    # Redémarrer Apache
    restart_apache()
    
    # Tester la configuration d'Apache
    test_ssl()
    
    print("SSL configuré avec succès sur Apache.")

# Exécution du script
if __name__ == "__main__":
    main()
