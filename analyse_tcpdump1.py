import csv

CSV_FILE = "resultats.csv"
MARKDOWN_FILE = "rapport.md"

total_packets = 0
total_volume = 0
rows = []

# Lecture du CSV avec séparateur ;
with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        ip = row["IP_source"]
        packets = int(row["Nombre_paquets"])
        volume = int(row["Volume_total_octets"])

        total_packets += packets
        total_volume += volume

        rows.append((ip, packets, volume))

# Génération du Markdown
with open(MARKDOWN_FILE, "w", encoding="utf-8") as md:
    md.write("# 📊 Network Traffic Analysis Report\n\n")

    md.write("## 🔍 Summary\n")
    md.write(f"- Total packets: **{total_packets}**\n")
    md.write(f"- Total traffic volume: **{total_volume} bytes**\n\n")

    md.write("## 📡 Traffic by Source IP\n")
    md.write("| Source IP | Packets | Total volume (bytes) |\n")
    md.write("|----------|---------|----------------------|\n")

    for ip, packets, volume in rows:
        md.write(f"| {ip} | {packets} | {volume} |\n")

    md.write("\n## 🚨 Suspicious activity (high traffic)\n")

    threshold = total_packets * 0.3  # 30% du trafic total
    suspicious = [(ip, p, v) for ip, p, v in rows if p > threshold]

    if suspicious:
        md.write("The following IP addresses generate an unusually high amount of traffic:\n\n")
        for ip, packets, volume in suspicious:
            md.write(f"- **{ip}** → {packets} packets, {volume} bytes\n")
    else:
        md.write("No abnormal traffic detected.\n")

print("✅ Markdown report generated: rapport.md")