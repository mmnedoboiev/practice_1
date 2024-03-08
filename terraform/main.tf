# Підключення до GCP
provider "google" {
  credentials = file("./**********************.json")
  project     = "**********************"
  region      = "us-west4"
}

#terraform init
#terraform validate
#terraform plan
#terraform apply -auto-approve
#terraform destroy -auto-approve
