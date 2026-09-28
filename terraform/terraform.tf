terraform {
  # https://releases.hashicorp.com/terraform/
  required_version = "~> 1.15"

  required_providers {
    aws = {
      # https://releases.hashicorp.com/terraform-provider-aws
      # latest: 6.55.0, ..., 5.100.0, ..., 5.0.0, 4.67.0
      source  = "hashicorp/aws"
      # major, should upgrade to 6.55.0
      version = "~> 6"
    }

    archive = {
      # https://releases.hashicorp.com/terraform-provider-archive
      # latest: 2.8.0, 2.7.1, 2.6.0, 2.5.0
      source  = "hashicorp/archive"
      # patch, should upgrade to 2.7.1
      version = "~> 2.8.1"
    }

    null = {
      # https://releases.hashicorp.com/terraform-provider-null
      # latest: 3.3.0, 3.2.4, 3.1.1
      source  = "hashicorp/null"
      # minor, should upgrade to 3.2.4
      version = "~> 3.1"
    }

    local = {
      # https://releases.hashicorp.com/terraform-provider-local
      # latest: 2.9.0, 2.8.0, 2.7.0, 2.6.2, 2.5.3, ..., 1.4.0, 1.3.0, 1.2.2, 1.1.0
      source  = "hashicorp/local"
      # patch, should upgrade to 1.2.2
      version = ">= 1.2.0"
    }

    # https://releases.hashicorp.com/terraform-provider-random
    # latest: 3.9.0, 3.8.0, 3.7.2, ..., 3.0.0, 2.3.1, ..., 2.0.0, 1.3.1, 1.3.0,

  }
}

# https://developer.hashicorp.com/terraform/language/expressions/version-constraints
# =
# !=

# >, <, >=, <=
# Compares to a specified version. Terraform allows versions that resolve to true.
# The operators follow semantic versioning conventions.
# The > and >= operators request newer versions. The < and <= operators request older versions.

# ~> 1.0   == >= 1.0, < 1.1
#     Allows only the right-most version component to increment. Examples:
#        ~> 1.0.4: Allows Terraform to install 1.0.5 and 1.0.10 but not 1.1.0.
#        ~> 1.1: Allows Terraform to install 1.2 and 1.10 but not 2.0.
