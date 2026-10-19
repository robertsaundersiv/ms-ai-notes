import {
  provider = aws.use1
  to       = aws_vpc.use1_vpc_03181bb3841a34090
  id       = "vpc-03181bb3841a34090"
}

import {
  provider = aws.use1
  to       = aws_subnet.use1_subnet_0b9d204a5e0f2572f
  id       = "subnet-0b9d204a5e0f2572f"
}

import {
  provider = aws.use1
  to       = aws_internet_gateway.use1_igw_0a920946a527ad1b8
  id       = "igw-0a920946a527ad1b8"
}

import {
  provider = aws.use1
  to       = aws_route_table.use1_rtb_0798e222198b3c51b
  id       = "rtb-0798e222198b3c51b"
}

import {
  provider = aws.use1
  to       = aws_route_table_association.use1_subnet_0b9d204a5e0f2572f
  id       = "subnet-0b9d204a5e0f2572f/rtb-0798e222198b3c51b"
}

import {
  provider = aws.use1
  to       = aws_security_group.use1_sg_0a445ec381aadfd4b
  id       = "sg-0a445ec381aadfd4b"
}

import {
  provider = aws.use1
  to       = aws_default_network_acl.use1_acl_0b86ac012751aa9ce
  id       = "acl-0b86ac012751aa9ce"
}

import {
  provider = aws.use1
  to       = aws_instance.use1_i_0856ba7bf732cda84
  id       = "i-0856ba7bf732cda84"
}

import {
  provider = aws.use1
  to       = aws_flow_log.use1_fl_0f5ae2872b16bc189
  id       = "fl-0f5ae2872b16bc189"
}

import {
  provider = aws.use1
  to       = aws_cloudwatch_log_group.use1__et_project_vpcflowlogs
  id       = "/et/project/vpcflowlogs"
}

import {
  provider = aws.use1
  to       = aws_vpc_peering_connection.use1_pcx_050e386744395d03c
  id       = "pcx-050e386744395d03c"
}

import {
  provider = aws.usw1
  to       = aws_vpc.usw1_vpc_04409d739c492c202
  id       = "vpc-04409d739c492c202"
}

import {
  provider = aws.usw1
  to       = aws_subnet.usw1_subnet_032da692b42c28f29
  id       = "subnet-032da692b42c28f29"
}

import {
  provider = aws.usw1
  to       = aws_internet_gateway.usw1_igw_087a2af3f3c09ff8a
  id       = "igw-087a2af3f3c09ff8a"
}

import {
  provider = aws.usw1
  to       = aws_route_table.usw1_rtb_0ed49f6bbeaa9c641
  id       = "rtb-0ed49f6bbeaa9c641"
}

import {
  provider = aws.usw1
  to       = aws_route_table_association.usw1_subnet_032da692b42c28f29
  id       = "subnet-032da692b42c28f29/rtb-0ed49f6bbeaa9c641"
}

import {
  provider = aws.usw1
  to       = aws_security_group.usw1_sg_0c25c71ec933935fe
  id       = "sg-0c25c71ec933935fe"
}

import {
  provider = aws.usw1
  to       = aws_default_network_acl.usw1_acl_0d7824466427fe00b
  id       = "acl-0d7824466427fe00b"
}

import {
  provider = aws.usw1
  to       = aws_instance.usw1_i_00089fb4f925f5610
  id       = "i-00089fb4f925f5610"
}

import {
  provider = aws.usw1
  to       = aws_flow_log.usw1_fl_0e1b7bd98d02f5204
  id       = "fl-0e1b7bd98d02f5204"
}

import {
  provider = aws.usw1
  to       = aws_cloudwatch_log_group.usw1__et_project_vpcflowlogs
  id       = "/et/project/vpcflowlogs"
}

import {
  provider = aws.usw1
  to       = aws_vpc_peering_connection_accepter.usw1_pcx_050e386744395d03c
  id       = "pcx-050e386744395d03c"
}

import {
  provider = aws.use1
  to       = aws_iam_role.use1_et_flowlogs_role
  id       = "et-flowlogs-role"
}

