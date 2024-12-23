# kubernetes-service.tf
resource "kubernetes_service" "application" {
  metadata {
    name = "my-application"
  }

  spec {
    selector = {
      app = kubernetes_deployment.application.metadata[0].labels.app
    }

    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}