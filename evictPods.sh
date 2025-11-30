#!/bin/bash

# Get list of nodes and extract node names
# old_version="v1.26.12-eks-5e0fdde"
# nodes=($(kubectl get nodes | grep "$old_version" | awk '{print $1}'))
nodes=(
  ip-10-13-17-23.ap-southeast-1.compute.internal
  ip-10-13-33-181.ap-southeast-1.compute.internal
)
echo $nodes

# Mark node as unschedulable
for node in "${nodes[@]}"; do
  kubectl cordon $node
  echo "Cordon $node"
done

# Loop through nodes and evict all pods
for node in "${nodes[@]}"; do
  # Evict all pods on node
  echo "Drain $node"
  kubectl drain "$node" --force --ignore-daemonsets --delete-emptydir-data

  # Wait for pods to finish starting
  while true; do
    count=$(kubectl get pods -A | awk 'NR>1' | grep -vE "(Running|Completed|Evicted)" | wc -l)
    echo "Pods starting: $count"
    if [ $count -le 30 ]; then
      break
    fi
    echo "sleep $count"
    sleep $count
  done
  sleep 30
done
