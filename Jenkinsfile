pipeline {
    agent any
    tools {
        go 'Go 1.16.3'
    }
    environment {
        GO111MODULE = 'on'
    }
    stages {
        stage('Build') {
            steps {
                echo 'Compiling...'
                sh 'go version'
                sh 'go build main.go'
                sh './main'
            }
        }
    }
}
