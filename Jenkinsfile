pipeline {
  agent none
  stages {
    stage('analisys') {
      agent any
      environment {
        scannerHome = 'sonnarqube'
      }
      steps {
        withSonarQubeEnv('sonarqube') {
          sh '/home/ubuntu/sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner'
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

    }

    failure {

    }

  }
}