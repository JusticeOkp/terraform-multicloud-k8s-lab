Multi-Cloud Kubernetes Infrastructure Lab: Terraform Deployment of AKS & EKS
This repository documents my hands-on lab deploying Kubernetes clusters on both Azure AKS and AWS EKS using Terraform, along with full lifecycle infrastructure management (deploy → validate → destroy).
The project also showcases AI-assisted Terraform troubleshooting using GitHub Copilot inside VS Code, a modern workflow that significantly accelerated debugging and learning.
1. Project Overview
This lab demonstrates how to:
Deploy a fully managed AWS EKS cluster (v1.29)
Deploy a fully managed Azure AKS cluster
Provision VPC networking, subnets, route tables, NAT gateways
Configure IAM roles, policies, and KMS encryption
Export Terraform plans into JSON and YAML formats
Destroy all resources to avoid cloud costs
Use GitHub Copilot as an inline cloud engineering assistant
Included artifacts such as plan.yaml, outputs.yaml, and the plan_to_yaml.py conversion script document each step for educational and audit purposes.
2. AI-Assisted Debugging (GitHub Copilot)
Throughout this project, GitHub Copilot inside VS Code provided contextual guidance that helped troubleshoot:
✔ Terraform errors
Copilot explained and helped fix issues such as:
Module version mismatches
Unsupported arguments (e.g., manage_aws_auth_configmap)
Deprecated inputs in the EKS module
Provider initialization issues
Syntax errors in Terraform blocks
✔ Module inspection
It helped navigate:
.terraform/modules/eks/variables.tf
New EKS module input expectations
The aws-auth ConfigMap changes
✔ Git workflow support
Copilot provided suggestions for:
Cleaning .terraform/
Updating .gitignore
Fixing invalid branches
Improving commit messages
✔ Documentation generation
Used Copilot to automatically outline:
Artifacts
Results
Cleanup actions
Recommendations
This significantly improved speed and productivity while deepening understanding.
3. Repository Structure
/
├── main.tf                     # Terraform configuration for EKS lab
├── plan.yaml                   # Human-readable YAML output of terraform plan
├── outputs.yaml                # Human-readable YAML output of terraform outputs
├── scripts/
│   └── plan_to_yaml.py         # JSON → YAML converter script
├── .gitignore                  # Git hygiene rules
└── README.md                   # Project documentation
4. Terraform Plan Export (JSON → YAML Workflow)
Terraform generates execution plans in a binary .tfplan format.
To make the plan readable and suitable for documentation, I exported the plan through two stages:
Step 1 — Export Terraform plan to JSON
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
Step 2 — Convert JSON → YAML
Using scripts/plan_to_yaml.py:
python3 scripts/plan_to_yaml.py plan.json plan.yaml
Why YAML?
YAML is:
easier to read
easier to review in GitHub
better for documentation
friendly for diffs
widely used in Kubernetes & cloud engineering
The included plan.yaml demonstrates the complete infrastructure Terraform intended to deploy in a clean, readable format.
5. Best Practices (.gitignore)
This project excludes sensitive and auto-generated Terraform files:
.terraform/
terraform.tfstate
terraform.tfstate.backup
.terraform.lock.hcl
plan.tfplan
plan.json
outputs.json
These files should never be committed because they may contain:
Resource IDs
Cloud metadata
Secrets or credentials
Hashicorp provider internal data
Only safe, human-readable artifacts (plan.yaml, outputs.yaml) are included.
6. Full Terraform Workflow
Initialize providers and modules
terraform init
Preview infrastructure changes
terraform plan -out=plan.tfplan
Deploy the infrastructure
terraform apply
Export plan and outputs
terraform show -json plan.tfplan > plan.json
terraform output -json > outputs.json
python3 scripts/plan_to_yaml.py plan.json plan.yaml
python3 scripts/plan_to_yaml.py outputs.json outputs.yaml
Tear down infrastructure
terraform destroy -auto-approve
7. Key Outcomes
✔ EKS cluster deployed successfully
✔ Terraform artifacts exported (plan + outputs in YAML)
✔ All resources destroyed to avoid costs
✔ Repo cleaned with strict Git best practices
✔ GitHub Copilot significantly improved debugging
✔ Full version-controlled documentation included
8. Future Improvements
Add CI/CD using GitHub Actions
Add remote backend (S3 + DynamoDB or Azure Blob)
Deploy sample workloads via Helm
Automate aws-auth ConfigMap
Add Azure AKS Terraform config
Add diagrams for architecture
Author
Justice Okpara (@JusticeOkp)
🚀 END OF README