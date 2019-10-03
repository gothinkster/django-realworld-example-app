pipeline {
  agent none
  stages {
    stage('version') {
      agent {
        dockerfile {
          filename 'Dockerfile'
        }

      }
      steps {
        sh 'python --version'
      }
    }
    stage('requirements') {
      agent {
        dockerfile {
          filename 'Dockerfile'
        }

      }
      steps {
        sh 'pip freeze'
      }
    }
    stage('static-analasys') {
      agent {
        dockerfile {
          filename 'Dockerfile.sonar'
        }

      }
      steps {
        sh 'sonar-scanner'
      }
    }
  }
}