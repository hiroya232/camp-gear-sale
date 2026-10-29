terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

resource "aws_iam_policy" "CodeBuildBasePolicy_camp_gear_sale_working_ap_northeast_1" {
  name   = "CodeBuildBasePolicy-camp-gear-sale-working-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-working",
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-working:*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::codepipeline-ap-northeast-1-*"
      ],
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:GetBucketAcl",
        "s3:GetBucketLocation"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "codebuild:CreateReportGroup",
        "codebuild:CreateReport",
        "codebuild:UpdateReport",
        "codebuild:BatchPutTestCases",
        "codebuild:BatchPutCodeCoverages"
      ],
      "Resource": [
        "arn:aws:codebuild:ap-northeast-1:969317770908:report-group/camp-gear-sale-working-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup"
      ],
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-working"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "AWSCodePipelineServiceRole_ap_northeast_1_camp_gear_sale_working" {
  name   = "AWSCodePipelineServiceRole-ap-northeast-1-camp-gear-sale-working"
  path   = "/service-role/"
  policy = jsonencode({
  "Statement": [
    {
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEqualsIfExists": {
          "iam:PassedToService": [
            "cloudformation.amazonaws.com",
            "elasticbeanstalk.amazonaws.com",
            "ec2.amazonaws.com",
            "ecs-tasks.amazonaws.com"
          ]
        }
      }
    },
    {
      "Action": [
        "codecommit:CancelUploadArchive",
        "codecommit:GetBranch",
        "codecommit:GetCommit",
        "codecommit:GetRepository",
        "codecommit:GetUploadArchiveStatus",
        "codecommit:UploadArchive"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "codedeploy:CreateDeployment",
        "codedeploy:GetApplication",
        "codedeploy:GetApplicationRevision",
        "codedeploy:GetDeployment",
        "codedeploy:GetDeploymentConfig",
        "codedeploy:RegisterApplicationRevision"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "codestar-connections:UseConnection"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "elasticbeanstalk:*",
        "ec2:*",
        "elasticloadbalancing:*",
        "autoscaling:*",
        "cloudwatch:*",
        "s3:*",
        "sns:*",
        "cloudformation:*",
        "rds:*",
        "sqs:*",
        "ecs:*"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "lambda:InvokeFunction",
        "lambda:ListFunctions"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "opsworks:CreateDeployment",
        "opsworks:DescribeApps",
        "opsworks:DescribeCommands",
        "opsworks:DescribeDeployments",
        "opsworks:DescribeInstances",
        "opsworks:DescribeStacks",
        "opsworks:UpdateApp",
        "opsworks:UpdateStack"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:DeleteStack",
        "cloudformation:DescribeStacks",
        "cloudformation:UpdateStack",
        "cloudformation:CreateChangeSet",
        "cloudformation:DeleteChangeSet",
        "cloudformation:DescribeChangeSet",
        "cloudformation:ExecuteChangeSet",
        "cloudformation:SetStackPolicy",
        "cloudformation:ValidateTemplate"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "codebuild:BatchGetBuilds",
        "codebuild:StartBuild",
        "codebuild:BatchGetBuildBatches",
        "codebuild:StartBuildBatch"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Effect": "Allow",
      "Action": [
        "devicefarm:ListProjects",
        "devicefarm:ListDevicePools",
        "devicefarm:GetRun",
        "devicefarm:GetUpload",
        "devicefarm:CreateUpload",
        "devicefarm:ScheduleRun"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "servicecatalog:ListProvisioningArtifacts",
        "servicecatalog:CreateProvisioningArtifact",
        "servicecatalog:DescribeProvisioningArtifact",
        "servicecatalog:DeleteProvisioningArtifact",
        "servicecatalog:UpdateProduct"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:ValidateTemplate"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:DescribeImages"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "states:DescribeExecution",
        "states:DescribeStateMachine",
        "states:StartExecution"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "appconfig:StartDeployment",
        "appconfig:StopDeployment",
        "appconfig:GetDeployment"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codepipeline/camp-gear-sale-working",
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codepipeline/camp-gear-sale-working:log-stream:*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup"
      ],
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codepipeline/camp-gear-sale-working"
      ]
    }
  ],
  "Version": "2012-10-17"
})
}

resource "aws_iam_policy" "CodeBuildBasePolicy_camp_gear_sale_dev_ap_northeast_1" {
  name   = "CodeBuildBasePolicy-camp-gear-sale-dev-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-dev",
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-dev:*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::codepipeline-ap-northeast-1-*"
      ],
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:GetBucketAcl",
        "s3:GetBucketLocation"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "codebuild:CreateReportGroup",
        "codebuild:CreateReport",
        "codebuild:UpdateReport",
        "codebuild:BatchPutTestCases",
        "codebuild:BatchPutCodeCoverages"
      ],
      "Resource": [
        "arn:aws:codebuild:ap-northeast-1:969317770908:report-group/camp-gear-sale-dev-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup"
      ],
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-dev"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildCloudWatchLogsPolicy_camp_gear_sale_dev_ap_northeast_1" {
  name   = "CodeBuildCloudWatchLogsPolicy-camp-gear-sale-dev-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:aws/codebuild/camp-gear-sale-dev",
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:aws/codebuild/camp-gear-sale-dev:*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup"
      ],
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:aws/codebuild/camp-gear-sale-dev"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildBasePolicy_camp_gear_sale_prd_ap_northeast_1" {
  name   = "CodeBuildBasePolicy-camp-gear-sale-prd-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-prd",
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-prd:*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::codepipeline-ap-northeast-1-*"
      ],
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:GetBucketAcl",
        "s3:GetBucketLocation"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "codebuild:CreateReportGroup",
        "codebuild:CreateReport",
        "codebuild:UpdateReport",
        "codebuild:BatchPutTestCases",
        "codebuild:BatchPutCodeCoverages"
      ],
      "Resource": [
        "arn:aws:codebuild:ap-northeast-1:969317770908:report-group/camp-gear-sale-prd-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup"
      ],
      "Resource": [
        "arn:aws:logs:ap-northeast-1:969317770908:log-group:/aws/codebuild/camp-gear-sale-prd"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildSecretsManagerPolicy_camp_gear_sale_working_ap_northeast_1" {
  name   = "CodeBuildSecretsManagerPolicy-camp-gear-sale-working-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:ap-northeast-1:969317770908:secret:/CodeBuild/*"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildImageRepositoryPolicy_camp_gear_sale_working_ap_northeast_1" {
  name   = "CodeBuildImageRepositoryPolicy-camp-gear-sale-working-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "arn:aws:ecr:ap-northeast-1:969317770908:repository/camp-gear-sale"
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildSecretsManagerPolicy_camp_gear_sale_prd_ap_northeast_1" {
  name   = "CodeBuildSecretsManagerPolicy-camp-gear-sale-prd-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:ap-northeast-1:969317770908:secret:camp-gear-sale-prd-secret-8F7qQI"
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_working_ap_northeast_1_969317770908" {
  name   = "CodeBuildCodeConnectionsSourceCredentialsPolicy-camp-gear-sale-working-ap-northeast-1-969317770908"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "codestar-connections:GetConnectionToken",
        "codestar-connections:GetConnection",
        "codeconnections:GetConnectionToken",
        "codeconnections:GetConnection",
        "codeconnections:UseConnection"
      ],
      "Resource": [
        "arn:aws:codestar-connections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff",
        "arn:aws:codeconnections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_prd_ap_northeast_1_969317770908" {
  name   = "CodeBuildCodeConnectionsSourceCredentialsPolicy-camp-gear-sale-prd-ap-northeast-1-969317770908"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "codestar-connections:GetConnectionToken",
        "codestar-connections:GetConnection",
        "codeconnections:GetConnectionToken",
        "codeconnections:GetConnection",
        "codeconnections:UseConnection"
      ],
      "Resource": [
        "arn:aws:codestar-connections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff",
        "arn:aws:codeconnections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_dev_ap_northeast_1_969317770908" {
  name   = "CodeBuildCodeConnectionsSourceCredentialsPolicy-camp-gear-sale-dev-ap-northeast-1-969317770908"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "codestar-connections:GetConnectionToken",
        "codestar-connections:GetConnection",
        "codeconnections:GetConnectionToken",
        "codeconnections:GetConnection",
        "codeconnections:UseConnection"
      ],
      "Resource": [
        "arn:aws:codestar-connections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff",
        "arn:aws:codeconnections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_dev_test_ap_northeast_1" {
  name   = "CodeBuildCodeConnectionsSourceCredentialsPolicy-camp-gear-sale-dev-test-ap-northeast-1"
  path   = "/service-role/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "codestar-connections:GetConnectionToken",
        "codestar-connections:GetConnection",
        "codeconnections:GetConnectionToken",
        "codeconnections:GetConnection",
        "codeconnections:UseConnection"
      ],
      "Resource": [
        "arn:aws:codestar-connections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff",
        "arn:aws:codeconnections:ap-northeast-1:969317770908:connection/ee0258c7-92e9-433a-84c4-860fe853d6ff"
      ]
    }
  ]
})
}

resource "aws_iam_policy" "camp_gear_sale_dev_event_bridge_scheduler_policy" {
  name   = "camp-gear-sale-dev-event-bridge-scheduler-policy"
  path   = "/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:RunTask"
      ],
      "Resource": [
        "arn:aws:ecs:ap-northeast-1:969317770908:task-definition/camp-gear-sale-*"
      ],
      "Condition": {
        "ArnLike": {
          "ecs:cluster": "arn:aws:ecs:ap-northeast-1:969317770908:cluster/camp-gear-sale-dev-ecs-cluster"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": [
        "*"
      ],
      "Condition": {
        "StringLike": {
          "iam:PassedToService": "ecs-tasks.amazonaws.com"
        }
      }
    }
  ]
})
}

resource "aws_iam_policy" "camp_gear_sale_prd_event_bridge_scheduler_policy" {
  name   = "camp-gear-sale-prd-event-bridge-scheduler-policy"
  path   = "/"
  policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:RunTask"
      ],
      "Resource": [
        "arn:aws:ecs:ap-northeast-1:969317770908:task-definition/camp-gear-sale-*"
      ],
      "Condition": {
        "ArnLike": {
          "ecs:cluster": "arn:aws:ecs:ap-northeast-1:969317770908:cluster/camp-gear-sale-prd-ecs-cluster"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": [
        "*"
      ],
      "Condition": {
        "StringLike": {
          "iam:PassedToService": "ecs-tasks.amazonaws.com"
        }
      }
    }
  ]
})
}

resource "aws_iam_role" "codebuild_camp_gear_sale_dev_service_role" {
  name               = "codebuild-camp-gear-sale-dev-service-role"
  path               = "/service-role/"
  assume_role_policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_dev_service_role__AmazonEC2ContainerRegistryPowerUser" {
  role       = aws_iam_role.codebuild_camp_gear_sale_dev_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_dev_service_role__CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_dev_ap_northeast_1_969317770908" {
  role       = aws_iam_role.codebuild_camp_gear_sale_dev_service_role.name
  policy_arn = aws_iam_policy.CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_dev_ap_northeast_1_969317770908.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_dev_service_role__CodeBuildBasePolicy_camp_gear_sale_dev_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_dev_service_role.name
  policy_arn = aws_iam_policy.CodeBuildBasePolicy_camp_gear_sale_dev_ap_northeast_1.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_dev_service_role__CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_dev_test_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_dev_service_role.name
  policy_arn = aws_iam_policy.CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_dev_test_ap_northeast_1.arn
}

resource "aws_iam_role" "codebuild_camp_gear_sale_prd_service_role" {
  name               = "codebuild-camp-gear-sale-prd-service-role"
  path               = "/service-role/"
  assume_role_policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_prd_service_role__AmazonEC2ContainerRegistryPowerUser" {
  role       = aws_iam_role.codebuild_camp_gear_sale_prd_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_prd_service_role__CodeBuildSecretsManagerPolicy_camp_gear_sale_prd_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_prd_service_role.name
  policy_arn = aws_iam_policy.CodeBuildSecretsManagerPolicy_camp_gear_sale_prd_ap_northeast_1.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_prd_service_role__CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_prd_ap_northeast_1_969317770908" {
  role       = aws_iam_role.codebuild_camp_gear_sale_prd_service_role.name
  policy_arn = aws_iam_policy.CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_prd_ap_northeast_1_969317770908.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_prd_service_role__CodeBuildBasePolicy_camp_gear_sale_prd_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_prd_service_role.name
  policy_arn = aws_iam_policy.CodeBuildBasePolicy_camp_gear_sale_prd_ap_northeast_1.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_prd_service_role__CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_prd_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_prd_service_role.name
  policy_arn = "arn:aws:iam::969317770908:policy/service-role/CodeBuildCodeConnectionsSourceCredentialsPolicy-camp-gear-sale-prd-ap-northeast-1"
}

resource "aws_iam_role" "codebuild_camp_gear_sale_working_service_role" {
  name               = "codebuild-camp-gear-sale-working-service-role"
  path               = "/service-role/"
  assume_role_policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_working_service_role__CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_working_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_working_service_role.name
  policy_arn = "arn:aws:iam::969317770908:policy/service-role/CodeBuildCodeConnectionsSourceCredentialsPolicy-camp-gear-sale-working-ap-northeast-1"
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_working_service_role__CodeBuildSecretsManagerPolicy_camp_gear_sale_working_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_working_service_role.name
  policy_arn = aws_iam_policy.CodeBuildSecretsManagerPolicy_camp_gear_sale_working_ap_northeast_1.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_working_service_role__CodeBuildBasePolicy_camp_gear_sale_working_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_working_service_role.name
  policy_arn = aws_iam_policy.CodeBuildBasePolicy_camp_gear_sale_working_ap_northeast_1.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_working_service_role__CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_working_ap_northeast_1_969317770908" {
  role       = aws_iam_role.codebuild_camp_gear_sale_working_service_role.name
  policy_arn = aws_iam_policy.CodeBuildCodeConnectionsSourceCredentialsPolicy_camp_gear_sale_working_ap_northeast_1_969317770908.arn
}

resource "aws_iam_role_policy_attachment" "codebuild_camp_gear_sale_working_service_role__CodeBuildImageRepositoryPolicy_camp_gear_sale_working_ap_northeast_1" {
  role       = aws_iam_role.codebuild_camp_gear_sale_working_service_role.name
  policy_arn = aws_iam_policy.CodeBuildImageRepositoryPolicy_camp_gear_sale_working_ap_northeast_1.arn
}

resource "aws_iam_role" "camp_gear_sale_dev_ecs_role" {
  name               = "camp-gear-sale-dev-ecs-role"
  path               = "/"
  assume_role_policy = jsonencode({
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "camp_gear_sale_dev_ecs_role__AmazonECSTaskExecutionRolePolicy" {
  role       = aws_iam_role.camp_gear_sale_dev_ecs_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "camp_gear_sale_prd_ecs_role" {
  name               = "camp-gear-sale-prd-ecs-role"
  path               = "/"
  assume_role_policy = jsonencode({
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "camp_gear_sale_prd_ecs_role__AmazonECSTaskExecutionRolePolicy" {
  role       = aws_iam_role.camp_gear_sale_prd_ecs_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "camp_gear_sale_dev_event_bridge_scheduler_role" {
  name               = "camp-gear-sale-dev-event-bridge-scheduler-role"
  path               = "/service-role/"
  assume_role_policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "scheduler.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "969317770908"
        }
      }
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "camp_gear_sale_dev_event_bridge_scheduler_role__camp_gear_sale_dev_event_bridge_scheduler_policy" {
  role       = aws_iam_role.camp_gear_sale_dev_event_bridge_scheduler_role.name
  policy_arn = aws_iam_policy.camp_gear_sale_dev_event_bridge_scheduler_policy.arn
}

resource "aws_iam_role" "camp_gear_sale_prd_event_bridge_scheduler_role" {
  name               = "camp-gear-sale-prd-event-bridge-scheduler-role"
  path               = "/service-role/"
  assume_role_policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "scheduler.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "969317770908"
        }
      }
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "camp_gear_sale_prd_event_bridge_scheduler_role__camp_gear_sale_prd_event_bridge_scheduler_policy" {
  role       = aws_iam_role.camp_gear_sale_prd_event_bridge_scheduler_role.name
  policy_arn = aws_iam_policy.camp_gear_sale_prd_event_bridge_scheduler_policy.arn
}

resource "aws_codebuild_project" "camp_gear_sale_dev" {
  name         = "camp-gear-sale-dev"
  service_role = aws_iam_role.codebuild_camp_gear_sale_dev_service_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux-aarch64-standard:3.0-24.10.02"
    type         = "ARM_CONTAINER"
  }

  source {
    type     = "GITHUB"
    location = "https://github.com/hiroya232/camp-gear-sale"
  }

  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }
  }
}

resource "aws_codebuild_project" "camp_gear_sale_working" {
  name         = "camp-gear-sale-working"
  service_role = aws_iam_role.codebuild_camp_gear_sale_working_service_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux-aarch64-standard:3.0-24.10.02"
    type         = "ARM_CONTAINER"
  }

  source {
    type     = "GITHUB"
    location = "https://github.com/hiroya232/camp-gear-sale"
  }

  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }
  }
}

resource "aws_codebuild_project" "camp_gear_sale_prd" {
  name         = "camp-gear-sale-prd"
  service_role = aws_iam_role.codebuild_camp_gear_sale_prd_service_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux-aarch64-standard:3.0-24.10.02"
    type         = "ARM_CONTAINER"
  }

  source {
    type     = "GITHUB"
    location = "https://github.com/hiroya232/camp-gear-sale"
  }

  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }
  }
}

resource "aws_cloudwatch_log_group" "aws_codebuild_camp_gear_sale_dev" {
  name = "/aws/codebuild/camp-gear-sale-dev"
}

resource "aws_cloudwatch_log_group" "aws_codebuild_camp_gear_sale_prd" {
  name = "/aws/codebuild/camp-gear-sale-prd"
}

resource "aws_cloudwatch_log_group" "aws_codebuild_camp_gear_sale_working" {
  name = "/aws/codebuild/camp-gear-sale-working"
}
