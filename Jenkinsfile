pipeline {
  agent any
  stages {
    stage('Code Quality') {
      parallel {
        stage('Lint') {
          steps {
            sh 'python3 -m pip install black'
            sh 'python3 -m black ./payu --check'
          }
        }
        stage('Type Check') {
          steps {
            sh 'python3 -m pip install mypy'
            sh 'python3 -m pip install types-requests'
            sh 'python3 -m mypy ./payu'
          }
        }
      }
    }
    stage('Test') {
      steps {
        sh 'python3 -m pip install tox'
        sh 'python3 -m tox'
      }
    }

  }
}