pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('version') {
      steps {
        sh 'python --version'
      }
    }
    stage('requirements') {
      steps {
        sh 'pip freeze'
      }
    }
  }
}