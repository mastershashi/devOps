# DevOps, CI/CD, and Related Concepts

---

## 🔧 What Is DevOps?

**DevOps** is a set of practices, tools, and cultural philosophies that aim to unify software development (Dev) and IT operations (Ops). The goal is to shorten the software development lifecycle and provide continuous delivery with high software quality.

### Key Goals

- Faster delivery
- Improved collaboration
- Higher reliability
- Automated workflows
- Rapid recovery from failures

---

## 🧱 Core Principles of DevOps

1. **Collaboration** – Break down silos between Dev, QA, and Ops.
2. **Automation** – Build, test, and deploy software with minimal manual effort.
3. **Continuous Improvement** – Iterate and enhance systems regularly.
4. **Monitoring and Feedback** – Use logs, metrics, and alerts to learn from operations.
5. **Infrastructure as Code (IaC)** – Manage infrastructure with code (e.g., Terraform, Ansible).

---

## 🔁 CI/CD Explained

**CI/CD** stands for **Continuous Integration** and **Continuous Delivery/Deployment**.

### 1. Continuous Integration (CI)

- Developers frequently (daily) merge code changes into a shared repository.
- Each change triggers automated **builds** and **tests** to catch issues early.

**Tools:** Jenkins, GitHub Actions, GitLab CI, CircleCI

### 2. Continuous Delivery (CD)

- Code is automatically tested and prepared for deployment.
- Deployment to staging is automated, but production may need manual approval.

### 3. Continuous Deployment

- After passing tests, code is deployed to production **automatically**.

---

## DevOps Lifecycle Stages

1. **Plan** – Agile planning (e.g., Jira, Trello)
2. **Develop** – Coding (e.g., Git, VS Code)
3. **Build** – Compile and package (e.g., Maven, Gradle)
4. **Test** – Automated testing (e.g., Selenium, JUnit)
5. **Release** – Prepare for deployment (e.g., Helm, Artifactory)
6. **Deploy** – Push to environments (e.g., Kubernetes, ArgoCD)
7. **Operate** – Manage infrastructure (e.g., Docker, Terraform, AWS)
8. **Monitor** – Performance and issue tracking (e.g., Prometheus, Grafana, ELK)

---

## DevOps Toolchain

| Category            | Tools                        |
| ------------------- | ---------------------------- |
| Version Control     | Git, GitHub, GitLab          |
| CI/CD               | Jenkins, GitLab CI, CircleCI |
| Containerization    | Docker, Podman               |
| Orchestration       | Kubernetes, OpenShift        |
| IaC                 | Terraform, CloudFormation    |
| Configuration Mgmt. | Ansible, Chef, Puppet        |
| Monitoring          | Prometheus, Grafana, Datadog |
| Logging             | ELK Stack, Fluentd, Splunk   |

---

## Benefits of DevOps & CI/CD

- Faster time to market
- Reduced errors and rollbacks
- Consistent, repeatable deployments
- Higher developer satisfaction
- Enhanced security and compliance

---

## Example CI/CD Pipeline

1. Developer pushes code to GitHub.
2. GitHub Actions triggers a build.
3. Unit tests run automatically.
4. If passed, app is containerized using Docker.
5. Image is pushed to Docker Hub.
6. Kubernetes pulls the latest image and deploys it to staging.
7. Prometheus + Grafana monitor live metrics.
