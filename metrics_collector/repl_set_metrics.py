#repl_set_metrics.py

import boto3
import pymongo
from   pymongo import MongoClient
import json
import os
import time
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Config
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")  
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")  
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

cloudwatch = boto3.client(
    "cloudwatch",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)


MONGO_URI = os.getenv("MONGO_URI")
CLOUDWATCH_NAMESPACE = "yourCloudWatchNameSpace"
MONGODB_METRIC_DIMENSIONS = [{"Name": "Cluster", "Value": "ReplicaSet"}]



logger.info(f"🌐 MONGO_URI: {MONGO_URI}")


def get_replica_set_status():
    """RS STATUS"""
    try:
        logger.info(f"🔍 Searching for MongoDB in {MONGO_URI}...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client.admin
        status = db.command("replSetGetStatus")
        client.close()
        return status
    except Exception as e:
        logger.error(f"❌ Error getting Replica Set status: {e}")
        return None


def send_metrics_to_cloudwatch(status):
    """Send metrics to AWS CloudWatch and show it."""
    if status is None:
        logger.warning("⚠️ Failed to get Replica Set status. Exiting...")
        return

    metrics = []

    primary = [member for member in status["members"] if member["stateStr"] == "PRIMARY"]
    is_primary_available = 1 if primary else 0
    metrics.append({
        "MetricName": "PrimaryAvailable",
        "Value": is_primary_available,
        "Unit": "Count"
    })

    logger.info(f"📊 Metrics collected: {json.dumps(metrics, indent=2)}")

    try:
        cloudwatch.put_metric_data(
            Namespace="MongoDBReplicaSet",
            MetricData=metrics
        )
        logger.info("✅ Metrics successfully sent to CloudWatch")
    except Exception as e:
        logger.error(f"❌ Error sending metrics to CloudWatch: {e}")


 
    for member in status["members"]:
      if member["stateStr"] != "PRIMARY":
        try:
            if primary:
                primary_optime = primary[0]["optime"]["ts"].time if "ts" in primary[0]["optime"] else 0
                member_optime = member["optime"]["ts"].time if "ts" in member["optime"] else 0

                
                primary_datetime = datetime.utcfromtimestamp(primary_optime)
                member_datetime = datetime.utcfromtimestamp(member_optime)
                lag = (primary_datetime - member_datetime).total_seconds()
            else:
                lag = 0  
        except Exception as e:
            logger.error(f"⚠️ Error calculating replication for {member['name']}: {e}")
            lag = 0  

     
        metrics.append({
            "MetricName": "ReplicationLag",
            "Dimensions": [{"Name": "Member", "Value": member["name"]}],
            "Value": lag,
            "Unit": "Seconds"
        })


    try:
        
        cloudwatch.put_metric_data(
            Namespace=CLOUDWATCH_NAMESPACE,
            MetricData=metrics
        )
        print("✅ Metrics successfully sent to CloudWatch")
    except Exception as e:
        print(f"❌Error sending metrics to CloudWatch: {e}")



def main():
   while True:
        try:
            logger.info("📡 Getting Replica Set Status...")
            status = get_replica_set_status()
            send_metrics_to_cloudwatch(status)
        except Exception as e:
            logger.error(f"❌ Error in main loop: {e}")

        logger.info("⏳ Waiting 30 seconds before the next collection...")
        time.sleep(30)

if __name__ == "__main__":
    main()



