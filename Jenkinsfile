pipeline {
agent any
stages {
    stage ('GIT Checkout'){
        steps {
            git changelog: false, poll: false, url: 'https://github.com/ddesai-sjsu/cmpe-282-TeamProject.git'
        }
    }
    
    stage('build') {
  steps {
    sh 'pip install -r requirements.txt'
  }
}
    stage ('Test'){
        steps {
            sh 'python3 accounts/unit-test.py'
        }
    }
}
}