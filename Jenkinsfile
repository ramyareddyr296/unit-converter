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