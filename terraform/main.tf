# Підключення до GCP
provider "google" {
  credentials = file("./**********************.json")
  project     = "**********************"
  region      = "us-west4"
}

#Create VM instancrs
module "compute" {
  source = "./compute"
}

#Create sql instances
module "sql" {
  source = "./sql"
}


#terraform init
#terraform validate
#terraform plan
#terraform apply -auto-approve
#terraform destroy -auto-approve
