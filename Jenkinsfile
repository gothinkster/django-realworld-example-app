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
          sh '/home/ubuntu/sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner'
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