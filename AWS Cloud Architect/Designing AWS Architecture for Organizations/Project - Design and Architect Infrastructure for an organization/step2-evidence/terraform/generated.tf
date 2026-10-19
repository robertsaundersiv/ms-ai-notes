# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "pcx-050e386744395d03c"
resource "aws_vpc_peering_connection_accepter" "usw1_pcx_050e386744395d03c" {
  provider                  = aws.usw1
  auto_accept               = null
  tags                      = {}
  tags_all                  = {}
  vpc_peering_connection_id = "pcx-050e386744395d03c"
  accepter {
    allow_remote_vpc_dns_resolution = false
  }
  requester {
    allow_remote_vpc_dns_resolution = false
  }
}

# __generated__ by Terraform from "fl-0e1b7bd98d02f5204"
resource "aws_flow_log" "usw1_fl_0e1b7bd98d02f5204" {
  provider                   = aws.usw1
  deliver_cross_account_role = null
  eni_id                     = null
  iam_role_arn               = "arn:aws:iam::<ACCOUNT_ID>:role/et-flowlogs-role"
  log_destination            = null
  log_destination_type       = "cloud-watch-logs"
  log_format                 = "$${version} $${account-id} $${interface-id} $${srcaddr} $${dstaddr} $${srcport} $${dstport} $${protocol} $${packets} $${bytes} $${start} $${end} $${action} $${log-status}"
  max_aggregation_interval   = 60
  subnet_id                  = null
  tags = {
    Name = "et-db-flowlog"
  }
  tags_all = {
    Name = "et-db-flowlog"
  }
  traffic_type                  = "ALL"
  transit_gateway_attachment_id = null
  transit_gateway_id            = null
  vpc_id                        = "vpc-04409d739c492c202"
}

# __generated__ by Terraform from "igw-087a2af3f3c09ff8a"
resource "aws_internet_gateway" "usw1_igw_087a2af3f3c09ff8a" {
  provider = aws.usw1
  tags = {
    Name = "Account B IGW"
  }
  tags_all = {
    Name = "Account B IGW"
  }
  vpc_id = "vpc-04409d739c492c202"
}

# __generated__ by Terraform
resource "aws_route_table" "usw1_rtb_0ed49f6bbeaa9c641" {
  provider         = aws.usw1
  propagating_vgws = []
  route = [{
    carrier_gateway_id         = ""
    cidr_block                 = "0.0.0.0/0"
    core_network_arn           = ""
    destination_prefix_list_id = ""
    egress_only_gateway_id     = ""
    gateway_id                 = "igw-087a2af3f3c09ff8a"
    ipv6_cidr_block            = ""
    local_gateway_id           = ""
    nat_gateway_id             = ""
    network_interface_id       = ""
    transit_gateway_id         = ""
    vpc_endpoint_id            = ""
    vpc_peering_connection_id  = ""
    }, {
    carrier_gateway_id         = ""
    cidr_block                 = "10.0.0.0/16"
    core_network_arn           = ""
    destination_prefix_list_id = ""
    egress_only_gateway_id     = ""
    gateway_id                 = ""
    ipv6_cidr_block            = ""
    local_gateway_id           = ""
    nat_gateway_id             = ""
    network_interface_id       = ""
    transit_gateway_id         = ""
    vpc_endpoint_id            = ""
    vpc_peering_connection_id  = "pcx-050e386744395d03c"
  }]
  tags = {
    Name = "Route Table Account B"
  }
  tags_all = {
    Name = "Route Table Account B"
  }
  vpc_id = "vpc-04409d739c492c202"
}

# __generated__ by Terraform from "acl-0d7824466427fe00b"
resource "aws_default_network_acl" "usw1_acl_0d7824466427fe00b" {
  provider               = aws.usw1
  default_network_acl_id = "acl-0d7824466427fe00b"
  subnet_ids             = ["subnet-032da692b42c28f29"]
  tags                   = {}
  tags_all               = {}
  egress {
    action          = "allow"
    cidr_block      = "0.0.0.0/0"
    from_port       = 0
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(-1)
    rule_no         = 100
    to_port         = 0
  }
  egress {
    action          = "allow"
    cidr_block      = "10.0.0.0/16"
    from_port       = 0
    icmp_code       = -1
    icmp_type       = -1
    ipv6_cidr_block = null
    protocol        = jsonencode(1)
    rule_no         = 90
    to_port         = 0
  }
  egress {
    action          = "allow"
    cidr_block      = "10.0.0.0/16"
    from_port       = 1024
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(6)
    rule_no         = 91
    to_port         = 65535
  }
  ingress {
    action          = "allow"
    cidr_block      = "0.0.0.0/0"
    from_port       = 0
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(-1)
    rule_no         = 100
    to_port         = 0
  }
  ingress {
    action          = "allow"
    cidr_block      = "10.0.0.0/16"
    from_port       = 0
    icmp_code       = -1
    icmp_type       = -1
    ipv6_cidr_block = null
    protocol        = jsonencode(1)
    rule_no         = 90
    to_port         = 0
  }
  ingress {
    action          = "allow"
    cidr_block      = "10.0.0.0/16"
    from_port       = 8080
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(6)
    rule_no         = 91
    to_port         = 8080
  }
}

# __generated__ by Terraform from "/et/project/vpcflowlogs"
resource "aws_cloudwatch_log_group" "usw1__et_project_vpcflowlogs" {
  provider          = aws.usw1
  kms_key_id        = null
  log_group_class   = "STANDARD"
  name              = "/et/project/vpcflowlogs"
  name_prefix       = null
  retention_in_days = 1
  skip_destroy      = false
  tags              = {}
  tags_all          = {}
}

# __generated__ by Terraform
resource "aws_subnet" "usw1_subnet_032da692b42c28f29" {
  provider                                       = aws.usw1
  assign_ipv6_address_on_creation                = false
  availability_zone                              = "us-west-1c"
  availability_zone_id                           = "usw1-az3"
  cidr_block                                     = "192.168.0.0/20"
  customer_owned_ipv4_pool                       = null
  enable_dns64                                   = false
  enable_lni_at_device_index                     = 0
  enable_resource_name_dns_a_record_on_launch    = false
  enable_resource_name_dns_aaaa_record_on_launch = false
  ipv6_cidr_block                                = null
  ipv6_native                                    = false
  map_customer_owned_ip_on_launch                = false
  map_public_ip_on_launch                        = false
  outpost_arn                                    = null
  private_dns_hostname_type_on_launch            = "ip-name"
  tags = {
    Name = "Account B subnet 1"
  }
  tags_all = {
    Name = "Account B subnet 1"
  }
  vpc_id = "vpc-04409d739c492c202"
}

# __generated__ by Terraform from "sg-0c25c71ec933935fe"
resource "aws_security_group" "usw1_sg_0c25c71ec933935fe" {
  provider    = aws.usw1
  description = "et-analytics-instance created 2026-10-18T04:48:45.370Z"
  egress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = ""
    from_port        = 0
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "-1"
    security_groups  = []
    self             = false
    to_port          = 0
  }]
  ingress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = ""
    from_port        = 22
    ipv6_cidr_blocks = []
    prefix_list_ids  = ["pl-0e99958a47b22d6ab"]
    protocol         = "tcp"
    security_groups  = []
    self             = false
    to_port          = 22
    }, {
    cidr_blocks      = ["10.0.0.0/16"]
    description      = ""
    from_port        = -1
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "icmp"
    security_groups  = []
    self             = false
    to_port          = -1
    }, {
    cidr_blocks      = ["10.0.0.0/16"]
    description      = ""
    from_port        = 8080
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = []
    self             = false
    to_port          = 8080
  }]
  name                   = "et-analytics-instance"
  name_prefix            = null
  revoke_rules_on_delete = null
  tags                   = {}
  tags_all               = {}
  vpc_id                 = "vpc-04409d739c492c202"
}

# __generated__ by Terraform from "subnet-032da692b42c28f29/rtb-0ed49f6bbeaa9c641"
resource "aws_route_table_association" "usw1_subnet_032da692b42c28f29" {
  provider       = aws.usw1
  gateway_id     = null
  route_table_id = "rtb-0ed49f6bbeaa9c641"
  subnet_id      = "subnet-032da692b42c28f29"
}

# __generated__ by Terraform
resource "aws_vpc" "usw1_vpc_04409d739c492c202" {
  provider                             = aws.usw1
  assign_generated_ipv6_cidr_block     = false
  cidr_block                           = "192.168.0.0/16"
  enable_dns_hostnames                 = false
  enable_dns_support                   = true
  enable_network_address_usage_metrics = false
  instance_tenancy                     = "default"
  ipv4_ipam_pool_id                    = null
  ipv4_netmask_length                  = null
  ipv6_cidr_block                      = null
  ipv6_cidr_block_network_border_group = null
  ipv6_ipam_pool_id                    = null
  ipv6_netmask_length                  = 0
  tags = {
    Name = "Account B"
  }
  tags_all = {
    Name = "Account B"
  }
}

# __generated__ by Terraform from "pcx-050e386744395d03c"
resource "aws_vpc_peering_connection" "use1_pcx_050e386744395d03c" {
  provider      = aws.use1
  auto_accept   = null
  peer_owner_id = jsonencode(<ACCOUNT_ID>)
  peer_region   = "us-west-1"
  peer_vpc_id   = "vpc-04409d739c492c202"
  tags          = {}
  tags_all      = {}
  vpc_id        = "vpc-03181bb3841a34090"
  accepter {
    allow_remote_vpc_dns_resolution = false
  }
  requester {
    allow_remote_vpc_dns_resolution = false
  }
}

# __generated__ by Terraform from "igw-0a920946a527ad1b8"
resource "aws_internet_gateway" "use1_igw_0a920946a527ad1b8" {
  provider = aws.use1
  tags = {
    Name = "Account A IGW"
  }
  tags_all = {
    Name = "Account A IGW"
  }
  vpc_id = "vpc-03181bb3841a34090"
}

# __generated__ by Terraform from "acl-0b86ac012751aa9ce"
resource "aws_default_network_acl" "use1_acl_0b86ac012751aa9ce" {
  provider               = aws.use1
  default_network_acl_id = "acl-0b86ac012751aa9ce"
  subnet_ids             = ["subnet-0b9d204a5e0f2572f"]
  tags                   = {}
  tags_all               = {}
  egress {
    action          = "allow"
    cidr_block      = null
    from_port       = 0
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = "::/0"
    protocol        = jsonencode(-1)
    rule_no         = 101
    to_port         = 0
  }
  egress {
    action          = "allow"
    cidr_block      = "0.0.0.0/0"
    from_port       = 0
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(-1)
    rule_no         = 100
    to_port         = 0
  }
  egress {
    action          = "allow"
    cidr_block      = "192.168.0.0/16"
    from_port       = 0
    icmp_code       = -1
    icmp_type       = -1
    ipv6_cidr_block = null
    protocol        = jsonencode(1)
    rule_no         = 90
    to_port         = 0
  }
  egress {
    action          = "allow"
    cidr_block      = "192.168.0.0/16"
    from_port       = 8080
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(6)
    rule_no         = 91
    to_port         = 8080
  }
  ingress {
    action          = "allow"
    cidr_block      = null
    from_port       = 0
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = "::/0"
    protocol        = jsonencode(-1)
    rule_no         = 101
    to_port         = 0
  }
  ingress {
    action          = "allow"
    cidr_block      = "0.0.0.0/0"
    from_port       = 0
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(-1)
    rule_no         = 100
    to_port         = 0
  }
  ingress {
    action          = "allow"
    cidr_block      = "192.168.0.0/16"
    from_port       = 0
    icmp_code       = -1
    icmp_type       = -1
    ipv6_cidr_block = null
    protocol        = jsonencode(1)
    rule_no         = 90
    to_port         = 0
  }
  ingress {
    action          = "allow"
    cidr_block      = "192.168.0.0/16"
    from_port       = 1024
    icmp_code       = 0
    icmp_type       = 0
    ipv6_cidr_block = null
    protocol        = jsonencode(6)
    rule_no         = 91
    to_port         = 65535
  }
}

# __generated__ by Terraform from "/et/project/vpcflowlogs"
resource "aws_cloudwatch_log_group" "use1__et_project_vpcflowlogs" {
  provider          = aws.use1
  kms_key_id        = null
  log_group_class   = "STANDARD"
  name              = "/et/project/vpcflowlogs"
  name_prefix       = null
  retention_in_days = 1
  skip_destroy      = false
  tags              = {}
  tags_all          = {}
}

# __generated__ by Terraform from "sg-0a445ec381aadfd4b"
resource "aws_security_group" "use1_sg_0a445ec381aadfd4b" {
  provider    = aws.use1
  description = "et-db-test-sg created 2026-10-18T04:56:56.644Z"
  egress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = ""
    from_port        = 0
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "-1"
    security_groups  = []
    self             = false
    to_port          = 0
  }]
  ingress = [{
    cidr_blocks      = ["192.168.0.0/16"]
    description      = ""
    from_port        = -1
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "icmp"
    security_groups  = []
    self             = false
    to_port          = -1
    }, {
    cidr_blocks      = ["192.168.0.0/16"]
    description      = ""
    from_port        = 8080
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = []
    self             = false
    to_port          = 8080
    }, {
    cidr_blocks      = []
    description      = ""
    from_port        = 22
    ipv6_cidr_blocks = []
    prefix_list_ids  = ["pl-0e4bcff02b13bef1e"]
    protocol         = "tcp"
    security_groups  = []
    self             = false
    to_port          = 22
  }]
  name                   = "et-db-test-sg"
  name_prefix            = null
  revoke_rules_on_delete = null
  tags                   = {}
  tags_all               = {}
  vpc_id                 = "vpc-03181bb3841a34090"
}

# __generated__ by Terraform
resource "aws_subnet" "use1_subnet_0b9d204a5e0f2572f" {
  provider                                       = aws.use1
  assign_ipv6_address_on_creation                = false
  availability_zone                              = "us-east-1e"
  availability_zone_id                           = "use1-az3"
  cidr_block                                     = "10.0.0.0/20"
  customer_owned_ipv4_pool                       = null
  enable_dns64                                   = false
  enable_lni_at_device_index                     = 0
  enable_resource_name_dns_a_record_on_launch    = false
  enable_resource_name_dns_aaaa_record_on_launch = false
  ipv6_cidr_block                                = null
  ipv6_native                                    = false
  map_customer_owned_ip_on_launch                = false
  map_public_ip_on_launch                        = false
  outpost_arn                                    = null
  private_dns_hostname_type_on_launch            = "ip-name"
  tags = {
    Name = "Account A subnet 1"
  }
  tags_all = {
    Name = "Account A subnet 1"
  }
  vpc_id = "vpc-03181bb3841a34090"
}

# __generated__ by Terraform from "fl-0f5ae2872b16bc189"
resource "aws_flow_log" "use1_fl_0f5ae2872b16bc189" {
  provider                   = aws.use1
  deliver_cross_account_role = null
  eni_id                     = null
  iam_role_arn               = "arn:aws:iam::<ACCOUNT_ID>:role/et-flowlogs-role"
  log_destination            = null
  log_destination_type       = "cloud-watch-logs"
  log_format                 = "$${version} $${account-id} $${interface-id} $${srcaddr} $${dstaddr} $${srcport} $${dstport} $${protocol} $${packets} $${bytes} $${start} $${end} $${action} $${log-status}"
  max_aggregation_interval   = 60
  subnet_id                  = null
  tags = {
    Name = "et-db-flowlog"
  }
  tags_all = {
    Name = "et-db-flowlog"
  }
  traffic_type                  = "ALL"
  transit_gateway_attachment_id = null
  transit_gateway_id            = null
  vpc_id                        = "vpc-03181bb3841a34090"
}

# __generated__ by Terraform
resource "aws_route_table" "use1_rtb_0798e222198b3c51b" {
  provider         = aws.use1
  propagating_vgws = []
  route = [{
    carrier_gateway_id         = ""
    cidr_block                 = "0.0.0.0/0"
    core_network_arn           = ""
    destination_prefix_list_id = ""
    egress_only_gateway_id     = ""
    gateway_id                 = "igw-0a920946a527ad1b8"
    ipv6_cidr_block            = ""
    local_gateway_id           = ""
    nat_gateway_id             = ""
    network_interface_id       = ""
    transit_gateway_id         = ""
    vpc_endpoint_id            = ""
    vpc_peering_connection_id  = ""
    }, {
    carrier_gateway_id         = ""
    cidr_block                 = "192.168.0.0/16"
    core_network_arn           = ""
    destination_prefix_list_id = ""
    egress_only_gateway_id     = ""
    gateway_id                 = ""
    ipv6_cidr_block            = ""
    local_gateway_id           = ""
    nat_gateway_id             = ""
    network_interface_id       = ""
    transit_gateway_id         = ""
    vpc_endpoint_id            = ""
    vpc_peering_connection_id  = "pcx-050e386744395d03c"
  }]
  tags = {
    Name = "Route Table Account A"
  }
  tags_all = {
    Name = "Route Table Account A"
  }
  vpc_id = "vpc-03181bb3841a34090"
}

# __generated__ by Terraform from "et-flowlogs-role"
resource "aws_iam_role" "use1_et_flowlogs_role" {
  provider = aws.use1
  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "vpc-flow-logs.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
  description           = null
  force_detach_policies = false
  max_session_duration  = 3600
  name                  = "et-flowlogs-role"
  name_prefix           = null
  path                  = "/"
  permissions_boundary  = null
  tags                  = {}
  tags_all              = {}
}

# __generated__ by Terraform from "subnet-0b9d204a5e0f2572f/rtb-0798e222198b3c51b"
resource "aws_route_table_association" "use1_subnet_0b9d204a5e0f2572f" {
  provider       = aws.use1
  gateway_id     = null
  route_table_id = "rtb-0798e222198b3c51b"
  subnet_id      = "subnet-0b9d204a5e0f2572f"
}

# __generated__ by Terraform
resource "aws_instance" "usw1_i_00089fb4f925f5610" {
  provider                             = aws.usw1
  ami                                  = "ami-00f0b088032c72fda"
  associate_public_ip_address          = true
  availability_zone                    = "us-west-1c"
  disable_api_stop                     = false
  disable_api_termination              = false
  ebs_optimized                        = true
  enable_primary_ipv6                  = null
  get_password_data                    = false
  hibernation                          = false
  host_id                              = null
  host_resource_group_arn              = null
  iam_instance_profile                 = null
  instance_initiated_shutdown_behavior = "stop"
  instance_type                        = "t3.micro"
  ipv6_address_count                   = 0
  ipv6_addresses                       = []
  key_name                             = null
  monitoring                           = false
  placement_group                      = null
  placement_partition_number           = 0
  private_ip                           = "192.168.1.20"
  secondary_private_ips                = []
  security_groups                      = []
  source_dest_check                    = true
  subnet_id                            = "subnet-032da692b42c28f29"
  tags = {
    Name = "Account B Instance"
  }
  tags_all = {
    Name = "Account B Instance"
  }
  tenancy                     = "default"
  user_data                   = null
  user_data_base64            = null
  user_data_replace_on_change = null
  volume_tags                 = null
  vpc_security_group_ids      = ["sg-0c25c71ec933935fe"]
  capacity_reservation_specification {
    capacity_reservation_preference = "open"
  }
  cpu_options {
    amd_sev_snp      = null
    core_count       = 1
    threads_per_core = 2
  }
  credit_specification {
    cpu_credits = "unlimited"
  }
  enclave_options {
    enabled = false
  }
  maintenance_options {
    auto_recovery = "default"
  }
  metadata_options {
    http_endpoint               = "enabled"
    http_protocol_ipv6          = "disabled"
    http_put_response_hop_limit = 2
    http_tokens                 = "required"
    instance_metadata_tags      = "disabled"
  }
  private_dns_name_options {
    enable_resource_name_dns_a_record    = false
    enable_resource_name_dns_aaaa_record = false
    hostname_type                        = "ip-name"
  }
  root_block_device {
    delete_on_termination = true
    encrypted             = false
    iops                  = 3000
    kms_key_id            = null
    tags                  = {}
    tags_all              = {}
    throughput            = 125
    volume_size           = 8
    volume_type           = "gp3"
  }
}

# __generated__ by Terraform
resource "aws_vpc" "use1_vpc_03181bb3841a34090" {
  provider                             = aws.use1
  assign_generated_ipv6_cidr_block     = false
  cidr_block                           = "10.0.0.0/16"
  enable_dns_hostnames                 = false
  enable_dns_support                   = true
  enable_network_address_usage_metrics = false
  instance_tenancy                     = "default"
  ipv4_ipam_pool_id                    = null
  ipv4_netmask_length                  = null
  ipv6_cidr_block                      = null
  ipv6_cidr_block_network_border_group = null
  ipv6_ipam_pool_id                    = null
  ipv6_netmask_length                  = 0
  tags = {
    Name = "Account A"
  }
  tags_all = {
    Name = "Account A"
  }
}

# __generated__ by Terraform
resource "aws_instance" "use1_i_0856ba7bf732cda84" {
  provider                             = aws.use1
  ami                                  = "ami-0567589d25e06853e"
  associate_public_ip_address          = true
  availability_zone                    = "us-east-1e"
  disable_api_stop                     = false
  disable_api_termination              = false
  ebs_optimized                        = false
  enable_primary_ipv6                  = null
  get_password_data                    = false
  hibernation                          = false
  host_id                              = null
  host_resource_group_arn              = null
  iam_instance_profile                 = null
  instance_initiated_shutdown_behavior = "stop"
  instance_type                        = "t2.nano"
  ipv6_address_count                   = 0
  ipv6_addresses                       = []
  key_name                             = null
  monitoring                           = false
  placement_group                      = null
  placement_partition_number           = 0
  private_ip                           = "10.0.1.185"
  secondary_private_ips                = []
  security_groups                      = []
  source_dest_check                    = true
  subnet_id                            = "subnet-0b9d204a5e0f2572f"
  tags = {
    Name = "Account A Instance"
  }
  tags_all = {
    Name = "Account A Instance"
  }
  tenancy                     = "default"
  user_data                   = null
  user_data_base64            = null
  user_data_replace_on_change = null
  volume_tags                 = null
  vpc_security_group_ids      = ["sg-0a445ec381aadfd4b"]
  capacity_reservation_specification {
    capacity_reservation_preference = "open"
  }
  cpu_options {
    amd_sev_snp      = null
    core_count       = 1
    threads_per_core = 1
  }
  credit_specification {
    cpu_credits = "standard"
  }
  enclave_options {
    enabled = false
  }
  maintenance_options {
    auto_recovery = "default"
  }
  metadata_options {
    http_endpoint               = "enabled"
    http_protocol_ipv6          = "disabled"
    http_put_response_hop_limit = 2
    http_tokens                 = "required"
    instance_metadata_tags      = "disabled"
  }
  private_dns_name_options {
    enable_resource_name_dns_a_record    = false
    enable_resource_name_dns_aaaa_record = false
    hostname_type                        = "ip-name"
  }
  root_block_device {
    delete_on_termination = true
    encrypted             = false
    iops                  = 3000
    kms_key_id            = null
    tags                  = {}
    tags_all              = {}
    throughput            = 125
    volume_size           = 8
    volume_type           = "gp3"
  }
}
