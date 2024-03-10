resource "google_compute_instance" "flask_instance" {
  name         = "flask-instance-terraform"
  machine_type = "f1-micro"
  zone         = "us-west4-b"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Вказуємо, що потрібна публічна IP-адреса
      network_tier = "PREMIUM"
    }
  }

  metadata_startup_script = "sudo curl -sSL https://get.docker.com | sh ; sudo curl -L \"https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose; sudo chmod +x /usr/local/bin/docker-compose; sudo mkdir /app; sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config;"

  tags = ["web", "dev"]
}