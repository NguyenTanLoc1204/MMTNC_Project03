pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '23127406-23127423-webapp' 
        DOCKERHUB_CREDENTIALS = 'dockerhub-id' 
        DOCKERHUB_USER = '23127406' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKERHUB_USER/$DOCKER_IMAGE:latest .'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-id', passwordVariable: 'DOCKER_REGISTRY_PASS', usernameVariable: 'DOCKER_REGISTRY_USER')]) {
                        sh "echo $DOCKER_REGISTRY_PASS | docker login -u $DOCKER_REGISTRY_USER --password-stdin"
                    }
                }
            }
        }

        stage('Push Image to Docker Hub') { 
            steps {
                script {
                    sh 'docker push $DOCKERHUB_USER/$DOCKER_IMAGE:latest'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    sh 'docker stop $DOCKER_IMAGE || true'
                    sh 'docker rm $DOCKER_IMAGE || true'
                    
                    sh 'docker run -d -p 5000:5000 --name $DOCKER_IMAGE $DOCKERHUB_USER/$DOCKER_IMAGE:latest'
                }
            }
        }
    }
}