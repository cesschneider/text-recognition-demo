# outputs.tf
output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = module.eks.cluster_security_group_id
}

output "service_url" {
  description = "URL of the deployed application"
  value       = kubernetes_service.application.status[0].load_balancer[0].ingress[0].hostname
}