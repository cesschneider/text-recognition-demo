# kubernetes-deployment.tf
resource "kubernetes_deployment" "application" {
  metadata {
    name = "my-application"
    labels = {
      app = "my-application"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "my-application"
      }
    }

    template {
      metadata {
        labels = {
          app = "my-application"
        }
      }

      spec {
        container {
          image = "cesschneider/hello-docker-world"  # Replace with your Docker image
          name  = "my-application"

          port {
            container_port = 80
          }

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "0.25"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}