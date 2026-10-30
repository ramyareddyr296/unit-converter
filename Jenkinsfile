
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        IMAGE_NAME = 'ramyareddy120/unit-converter'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ramyareddyr296/unit-converter.git'

                script {
                    env.IMAGE_TAG = "build-${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-final',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"

                        Write-Host "Checking Docker credentials..."
                        Write-Host "Docker username: $env:DOCKER_USER"
                        Write-Host "Docker token length: $($env:DOCKER_TOKEN.Length)"

                        if ([string]::IsNullOrWhiteSpace($env:DOCKER_USER)) {
                            throw "Docker username is empty"
                        }

                        if ([string]::IsNullOrWhiteSpace($env:DOCKER_TOKEN)) {
                            throw "Docker token is empty"
                        }

                        $env:DOCKER_TOKEN |
                            docker login --username $env:DOCKER_USER --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker login failed"
                        }

                        Write-Host "Docker login successful!"

                        docker push "${env:IMAGE_NAME}:${env:IMAGE_TAG}"

                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker push failed"
                        }

                        Write-Host "Docker image pushed successfully!"
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    $manifest = Get-Content deployment.yaml -Raw

                    $manifest = [regex]::Replace(
                        $manifest,
                        '(?m)^(\s*image:\s*)ramyareddy120/unit-converter:\S+',
                        ('$1' + "${env:IMAGE_NAME}:${env:IMAGE_TAG}")
                    )

                    Set-Content -Path deployment-build.yaml -Value $manifest

                    kubectl --context docker-desktop apply -f deployment-build.yaml

                    if ($LASTEXITCODE -ne 0) {
                        throw "Deployment failed"
                    }

                    kubectl --context docker-desktop apply -f service.yaml

                    if ($LASTEXITCODE -ne 0) {
                        throw "Service configuration failed"
                    }

                    kubectl --context docker-desktop rollout status deployment/unit-converter --timeout=180s

                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubernetes rollout failed"
                    }

                    Write-Host "Kubernetes deployment successful!"
                '''
            }
        }
    }

    post {
        success {
            echo 'Docker image pushed and Kubernetes deployment updated successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the failed stage in Console Output.'
        }
    }
}
