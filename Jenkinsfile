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


                    echo '--- 3. Đang chờ 15s để ứng dụng khởi động... ---'
                    sh 'sleep 15' 
                    
                    echo '--- 4. Kiểm tra trạng thái ---'
                    sh 'docker ps'
                    
                    echo '--- 5. Log của Container (xem có lỗi Python không) ---'
                    sh 'docker logs $DOCKER_IMAGE'
                    
                    echo '--- 6. Test kết nối từ BÊN TRONG container ---'
                    // Lệnh này tương đương với việc bạn mở terminal của container và gõ curl
                    // Nó chắc chắn 100% sẽ bắt được kết quả nếu App đang chạy
                    sh "docker exec $DOCKER_IMAGE python -c 'import urllib.request; print(urllib.request.urlopen(\"http://127.0.0.1:5000\").read().decode(\"utf-8\"))'"                }
            }
        }
    }
}