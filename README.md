# The Swarna Rao Group // Advanced AI & Data Science Portfolio Platform
[![Python](https://img.shields.io/badge/Python-3.13-fuchsia.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Django-5.0-cyan.svg)](https://docs.djangoproject.com/)
[![Docker Container](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Production Live](https://img.shields.io/badge/Live-www.theswarnaraogroup.com-brightgreen.svg)](https://www.theswarnaraogroup.com)

An elite, high-performance, containerized full-stack web application showcasing advanced AI/Data Science portfolios and managing an independent commercial consulting intake engine. Engineered with strict architectural separation of concerns, automated infrastructure deployments, and dynamic state synchronization via a multi-relational database engine.

---

## Architectural Blueprint & Core Features

- **Dynamic State Routing Engine:** Implements advanced Django view routing paired with unified template parameters (`request.resolver_match.url_name`) to run dynamic, high-contrast visual state state changes across the presentation layer seamlessly.
- **Multi-Selection Session Booking Matrix:** Re-architected transactional intake data schema supporting multi-checkbox compilation. Incoming browser arrays are ingested, validated, and compressed into comma-separated text blocks for manual CRM tracking.
- **Neo-Noir Hyper-Contrast UI:** Built explicitly on top of **Tailwind CSS**, discarding generic minimal structures for an aggressive, high-impact dark theme built for modern, technical presentation.
- **Relational Data Management:** Backed by an optimized backend database that houses structured schemas for career logs, computational project repositories, and customer inquiry strings.

---

## Tech Stack & Computations

- **Core Framework:** Python 3.13 // Django 5.x // Gunicorn WSGI
- **Frontend Matrix:** Tailwind CSS // HTML5 Custom Boilerplates // Vanilla JavaScript
- **Containerization & Environment:** Docker Engine // Docker Compose // Anaconda Virtual Environments
- **CI/CD & DevOps Automation:** GitHub Actions (`deploy.yml`) // Secure Runner Workflows
- **Production Infrastructure:** DigitalOcean Droplet Linux Environment
- **Security & Network Infrastructure:** NGINX Reverse Proxy // Let's Encrypt TLS/SSL End-to-End Encryption

---

## Containerization & Local Microservices

The architecture is entirely decoupled and containerized to guarantee environment parity from local staging to cloud execution. 

### Local Microservice Ingestion Setup
To stand up the application layer along with its detached storage state locally, clone the repository matrix and execute the Docker orchestration system:

```bash
# Clone the analytical asset repository
git clone [https://github.com/SwarnaRao24/MyPortfolio.git](https://github.com/SwarnaRao24/MyPortfolio.git)
cd MyPortfolio

# Spin up the container stack via Docker Compose
docker-compose up --build -d

# Execute core database system check and migrations inside the active runtime
docker-compose exec web python manage.py migrate

# Establish master administrative privileges
docker-compose exec web python manage.py createsuperuser
```
---

## Cloud Architecture & CI/CD Pipeline
The application features a production-grade GitOps delivery engine. Any commit pushed to the production branch triggers an automated build and delivery cycle without downtime.

### Production Blueprint Pipeline Flow
- **Source Check:** Code commit pushes to main.
- **GitHub Actions (deploy.yml):** Intercepts push event, mounts custom runners, verifies Python dependencies, and runs standard Django system integrity checks.
- **Secure SSH Handshake:** Authenticates using encrypted repo secrets directly into the DigitalOcean Droplet.
- **Autonomous Deployment:** Triggers the remote server to execute an immediate git pull, rebuilds the target Docker image states, re-allocates static resource directories, and runs data structural migrations.
- **Reverse Proxy Routing:** NGINX acts as an edge router, handling secure incoming traffic on port 80/443 and channeling it upstream to the underlying Python/Gunicorn service workers.
- **SSL Handshake Protection:** Automated Let's Encrypt scripts manage cryptographic challenges to maintain full TLS/SSL protection continuously.

---

## Repository Structural Overview
```
MyPortfolio/
├── .github/workflows/
│   └── deploy.yml          # Automated CI/CD execution script matrix
├── core/
│   ├── settings.py         # Root system configurations
│   └── urls.py             # Global HTTP entry routing mappings
├── portfolio/
│   ├── models.py           # Multi-relational schema maps (Experience, Project, Service, Contact)
│   ├── views.py            # Computational logic layers & POST response management
│   ├── admin.py            # Administrative dashboard registries
│   └── templates/          # High-contrast UI presentation layer blueprints
├── static/
│   └── profile.jpg         # Asset entry vector for professional biography portrait
├── Dockerfile              # Immutable application environment blueprint
├── docker-compose.yml      # Orchestration instructions for local service dependencies
├── manage.py               # Framework execution entry-point CLI
└── requirements.txt        # Verified lock-step Python packages configuration
```
---
**Developer:** Swarna Rao  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/swarnamukhirchintalapudi)

**Focus:** Python | CI/CD | Docker | Web Development | UI/UX

---

