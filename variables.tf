variable "project" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  type        = string
}

variable "gcs_bucket_name" {
  description = "GCS Bucket Name"
  type        = string
}

variable "gcs_storage_class" {
  description = "Storage Class"
  default     = "STANDARD"
}