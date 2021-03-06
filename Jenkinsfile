node {
  def acr = 'mycont.azurecr.io'
  def appName = 'nowapka'
  def imageName = "${acr}/${appName}"
  def imageTag = "${imageName}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
  def appRepo = "mycont.azurecr.io/nowapka:v1"

  checkout scm
  
 stage('Build the Image and Push to Azure Container Registry') 
 {
   app = docker.build("${imageName}")
   withDockerRegistry([credentialsId: 'acr_auth', url: "https://${acr}"]) {
      app.push("${env.BRANCH_NAME}.${env.BUILD_NUMBER}")
                }
  }

 stage ("Deploy Application on Azure Kubernetes Service")
 {
  switch (env.BRANCH_NAME) {
    // Roll out to canary environment
    case "canary":
        // Change deployed image in canary to the one we just built
        sh("sudo sed -i.bak 's#${appRepo}#${imageTag}#g' ./canary/*.yml")
        sh("sudo kubectl --namespace=prod3 apply -f ./canary/")
        sh("echo http://`kubectl --namespace=prod3 get service/${appName} --output=json | jq -r '.status.loadBalancer.ingress[0].ip'` > ${appName}")
        break

    // Roll out to production
    case "master":
        // Change deployed image in master to the one we just built
        sh("ls ./*")
        sh("sudo sed -i.bak 's#${appRepo}#${imageTag}#g' ./production/*.yaml")
        sh("sudo kubectl --kubeconfig ~admin12/.kube/config --namespace=prod3 apply -f ./production/")
        //sh("echo http://`kubectl --namespace=prod2 get service/${appName} --output=json | jq -r '.status.loadBalancer.ingress[0].ip'` > ${appName}")
        break

    // Roll out a dev environment
    default:
        // Create namespace if it doesn't exist
        sh("sudo kubectl get ns ${appName}-${env.BRANCH_NAME} || kubectl create ns ${appName}-${env.BRANCH_NAME}")
        // Don't use public load balancing for development branches
        sh("sudo sed -i.bak 's#${appRepo}#${imageTag}#g' ./dev/*.yml")
        sh("sudo kubectl --namespace=${appName}-${env.BRANCH_NAME} apply -f ./dev/")
        echo 'To access your environment run `kubectl proxy`'
        echo "Then access your service via http://localhost:8001/api/v1/proxy/namespaces/${appName}-${env.BRANCH_NAME}/services/${appName}:80"     
    }
  }
}
