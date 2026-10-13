#!/bin/bash
set -euo pipefail

SERVICE="rollback-demo"
REGION="asia-south1"
PROJECT="cloud-deployment-rollback"
TAG="candidate"

echo "=== Automated deployment with rollback ==="

# Find the revision currently receiving traffic
STABLE=$(gcloud run services describe "$SERVICE" \
  --region "$REGION" \
  --project "$PROJECT" \
 --format="value(status.traffic[0].revisionName)")

if [ -z "$STABLE" ]; then
  echo "ERROR: Could not find the stable revision."
  exit 1
fi

echo "Stable revision: $STABLE"

# Deploy new code without moving production traffic
gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --project "$PROJECT" \
  --no-traffic \
  --tag "$TAG" \
  --quiet

# Get the candidate URL
TEST_URL=$(gcloud run services describe "$SERVICE" \
  --region "$REGION" \
  --project "$PROJECT" \
  --flatten="status.traffic[]" \
  --filter="status.traffic.tag=$TAG" \
  --format="value(status.traffic.url)")


if [ -z "$TEST_URL" ]; then
  echo "ERROR: Candidate URL not found."
  exit 1
fi

# Check candidate health
HEALTHY=0
for i in {1..5}; do
  CODE=$(curl -sS -o /dev/null -w "%{http_code}" \
    --max-time 10 "$TEST_URL/health" || true)

  if [ "$CODE" = "200" ]; then
    HEALTHY=1
    break
  fi

  echo "Health check $i failed: HTTP ${CODE:-unknown}"
  sleep 3
done

if [ "$HEALTHY" -eq 1 ]; then
  echo "Health check passed. Promoting candidate."
  LATEST=$(gcloud run services describe "$SERVICE" \
    --region "$REGION" --project "$PROJECT" \
    --format="value(status.latestReadyRevisionName)")

  gcloud run services update-traffic "$SERVICE" \
    --region "$REGION" --project "$PROJECT" \
    --to-revisions "$LATEST=100" --quiet

  echo "SUCCESS: New revision is live."
else
  echo "Health check failed. Keeping stable revision live."
  gcloud run services update-traffic "$SERVICE" \
    --region "$REGION" --project "$PROJECT" \
    --to-revisions "$STABLE=100" --quiet

  echo "ROLLBACK: Traffic remains on $STABLE."
fi
