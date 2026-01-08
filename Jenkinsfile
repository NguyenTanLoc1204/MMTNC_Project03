pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '23127406-webapp-test-security' 
        DOCKERHUB_CREDENTIALS = 'dockerhub-id' 
        DOCKERHUB_USER = '23127406' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Security Scan (SAST) - Bandit') {
            steps {
                script {
                    sh 'pip install bandit'
                    sh 'bandit -r . -f json -o bandit_report.json || true' 
                    sh 'cat bandit_report.json' 
                }
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

        stage('Push Image') { 
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
                    sh 'docker run -d -p 3000:3000 --name $DOCKER_IMAGE $DOCKERHUB_USER/$DOCKER_IMAGE:latest'
                    
                    sh 'sleep 5' 
                }
            }
        }

        stage('Security Scan (DAST) - OWASP ZAP') {
            steps {
                script {
                    sh """
                    docker run --rm --link $DOCKER_IMAGE:target_app \
                    owasp/zap2docker-stable zap-baseline.py \
                    -t http://target_app:3000 \
                    -r zap_report.html \
                    || true
                    """
                }
            }
        }
    }
}