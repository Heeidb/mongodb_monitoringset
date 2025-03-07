README.md

This is a solution that allows you to monitor and manage the status, latency and performance of a Replica Set or a sharded cluster, with a focus on high availability and data replication. 

You will use:
 MONGODB
 DOCKER
 CLOUDWATCH (CUSTOM METRICS)

 
MongoDB Replica Set or Sharded Cluster in Docker: Simulates a environment for MongoDB by replicating primary and secondary nodes in Docker containers.
AWS CloudWatch: Used to log custom metrics (node ​​health, latency, active connections, resource usage) and set alarms to detect critical issues such as disconnections or high replication latency.
Docker: Docker containers allow you to create a controlled environment to test and validate MongoDB configurations without relying on physical hardware

STRUCTURE
mongo-monitoring
│──  metrics-collector/      # Metrics collection service
│   ├──  replica_set_metrics.py  # Python script to collect MongoDB metrics
│   ├──  requirements.txt     # Dependencies: pymongo, boto3
│   ├── Dockerfile           # Image for the collector servicee
│──  docker/                  # Docker configuration files
│   ├──  docker-compose.yml   # Defines MongoDB containers and the collector
│   ├──  mongo-keyfile/       # MongoDB authentication key
│──  #.env.example            # Template for credentials (DO NOT USE in production) remove the # at the beginning of .env
│── README.md                # Documentation
│──  LICENSE                  # License for the project
│──  .gitignore               # Avoids pushing sensitive files to GitHub


**Installation**
-----------------------------------------------------------------------------------------------------------------------------------
<><>**PREREQUISITES**<><> (1)
1.  Docker & Docker Compose installed → https://www.docker.com/products/docker-desktop/
2.  AWS Account & IAM User → Required to use AWS CloudWatch
2.  MongoDB URI (Replica Set Enabled)

-----------------------------------------------------------------------------------------------------------------------------------
[@]You will need to create a AWS Account for this and create an IAM user.
-----------------------------------------------------------------------------------------------------------------------------------
<><>**Clone the Repository**<><> (2)
git clone https://github.com/Heeidb/mongo-monitoring.git
cd mongo-monitoring
-----------------------------------------------------------------------------------------------------------------------------------
<><>**Set Up Environment Variables**<><> (3) 
#You will need to create an .env following the template/ fill with your credentials  without spaces or quotes & MONGO_URI:


cp #.env.example .env

#Create a .en"v file by copying the template.
#remove the "#" at the beginning of .env don't create your .env  file with "#".  Use nano or VSC 


AWS_ACCESS_KEY="________your__AK"
AWS_SECRET_KEY ="_________your_SK" 
AWS_DEFAULT_REGION=ur-region
MONGO_URI=mongodb://___________
 -WARNING: Custom metrics are NOT FREE. Check AWS pricing before use.
 -----------------------------------------------------------------------------------------------------------------------------------
.......**DEPLOYMENT**

.Start the Containers
In your terminal:

docker-compose up --build -d


VERIFY LOGS:

In your terminal:
docker logs -f metrics-collector




SCALABLE.
This project is modular and scalable, meaning you can: Expand it to monitor Sharding in addition to Replica Sets.
Add more custom metrics (e.g., CPU usage, disk I/O, query performance).
Integrate it with Grafana or Prometheus for better visualization.


Let's connect! → https://www.linkedin.com/in/heidi-e-851ab827b/



