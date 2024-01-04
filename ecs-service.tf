# Create ECS service
resource "aws_ecs_service" "translation_app_service" {
  name            = "translation-app-service"
  cluster         = "${aws_ecs_cluster.translation_app_cluster.id}"
  task_definition = "${aws_ecs_task_definition.translation_app_task.arn}"
  launch_type     = "FARGATE"
  desired_count   = 2

  load_balancer {
    target_group_arn = "${aws_lb_target_group.target_group.arn}"
    container_name   = "${aws_ecs_task_definition.translation_app_task.family}"
    container_port   = 5000
  }

  network_configuration {
    subnets          = ["${aws_default_subnet.subnet_a.id}", "${aws_default_subnet.subnet_b.id}"]
    assign_public_ip = true
    security_groups  = ["${aws_security_group.service_security_group.id}"] # Set up the security group
  }
}

# Service security group
resource "aws_security_group" "service_security_group" {
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    # Allow traffic in ONLY from the load balancer security group
    security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Load balancer app URL logging
output "app_url" {
  value = aws_alb.application_load_balancer.dns_name
}
