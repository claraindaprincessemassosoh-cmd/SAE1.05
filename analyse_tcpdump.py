import csv

# Nom du fichier tcpdump à analyser
FICHIER_ENTREE = "DumpFile.txt"
FICHIER_SORTIE = "resultats.csv"

trafic = {}

# Lecture du fichier tcpdump
with open(FICHIER_ENTREE, "r") as fichier:
    for ligne in fichier:
        # On ne garde que les lignes utiles
        if " IP " in ligne and "length" in ligne:
            try:
                parties = ligne.split()

                # Heure
                heure = parties[0]

                # Source et destination
                source = parties[2]        # ex: BP-Linux8.ssh
                destination = parties[4]   # ex: 192.168.190.130.50019:

                # Séparation IP / port
                src_ip, src_port = source.rsplit(".", 1)
                dst_ip, dst_port = destination.rstrip(":").rsplit(".", 1)

                # Taille du paquet
                longueur = int(ligne.split("length")[1].strip())

                # Initialisation si nouvelle IP source
                if src_ip not in trafic:
                    trafic[src_ip] = {
                        "paquets": 0,
                        "volume": 0
                    }

                # Mise à jour des statistiques
                trafic[src_ip]["paquets"] += 1
                trafic[src_ip]["volume"] += longueur

            except Exception:
                # Ignore les lignes mal formées
                pass

# Affichage des résultats
print("\n=== Analyse du trafic réseau ===\n")
for ip, data in trafic.items():
    print(f"IP source : {ip}")
    print(f"  Nombre de paquets : {data['paquets']}")
    print(f"  Volume total      : {data['volume']} octets\n")

# Création du fichier CSV pour Excel
with open(FICHIER_SORTIE, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["IP_source", "Nombre_paquets", "Volume_total_octets"])

    for ip, data in trafic.items():
        writer.writerow([ip, data["paquets"], data["volume"]])

print(f"Fichier CSV généré : {FICHIER_SORTIE}")
