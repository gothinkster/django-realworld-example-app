pipeline {
  agent none
  stages {
    stage('analisys') {
      agent any
      environment {
        scannerHome = 'sonnarqube'
      }
      steps {
        bitbucketStatusNotify 'INPROGRESS'
        withSonarQubeEnv('sonarqube') {
          sh '$SONAR_SCANNER/sonar-scanner'
        }

        timeout(time: 6, unit: 'MINUTES') {
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