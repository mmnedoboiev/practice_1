resource "google_sql_database_instance" "master" {
  name             = "master-instance"
  database_version = "POSTGRES_15"
  region           = "us-west1"

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = "db-f1-micro"
  }
  deletion_protection=false
}

resource "google_sql_database" "database" {
  name = "flask-db"
  instance = google_sql_database_instance.master.name
}