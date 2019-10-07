pipeline {
  agent none
  stages {
    stage('analisys') {
      agent any
      environment {
        scannerHome = 'sonarscanner'
      }
      steps {
        bitbucketStatusNotify 'INPROGRESS'
        withSonarQubeEnv('sonarqube') {
          sh 'sonar-scanner'
        }

        timeout(time: 10, unit: 'MINUTES') {
          waitForQualityGate true
        }

      }
    }
  }
  post {
    always {
      echo 'Pipeline encerrada'

    }

    success {
      bitbucketStatusNotify 'SUCCESSFUL'

    }

    failure {
      bitbucketStatusNotify 'FAILED'

    }

  }
}