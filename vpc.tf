# Provide a reference to your default VPC
resource "aws_default_vpc" "default_vpc" {
    tags = {
        Name  = "Production"
    }
}

# Provide references to your default subnets
resource "aws_default_subnet" "subnet_a" {
  # Use your own region here but reference to subnet 1a
  availability_zone = "ap-south-1"
}
