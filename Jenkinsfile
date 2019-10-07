pipeline {
  agent none
  stages {
    stage('Análise estática') {
      agent any
      environment {
        scannerHome = 'sonarscanner'
      }
      steps {
        bitbucketStatusNotify 'INPROGRESS'
        withSonarQubeEnv('sonarqube') {
          sh '../../sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner'
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