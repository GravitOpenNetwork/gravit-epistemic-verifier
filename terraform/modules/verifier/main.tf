resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-cluster"
}

resource "aws_ecs_task_definition" "verifier" {
  family                   = var.app_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"

  container_definitions = jsonencode([
    {
      name  = "verifier"
      image = var.container_image
      portMappings = [{ containerPort = 8000, hostPort = 8000 }]
      environment  = [for k, v in var.environment : { name = k, value = v }]
      logConfiguration = { ... }
    }
  ])
}

resource "aws_lb" "main" {
  name               = "${var.app_name}-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = var.public_subnets
}
