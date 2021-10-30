pipeline {
  agent any
  stages {
    stage('Lint') {
      parallel {
        stage('Lint') {
          steps {
            sh '''pip3 install black &&
python3 -m black ./payu --check'''
          }
        }

        stage('Type Check') {
          steps {
            sh '''pip3 install mypy &&
mypy --install-types && python3 -m mypy ./payu'''
          }
        }

      }
    }

    stage('Test') {
      steps {
        sh 'pip3 install tox && python3 -m tox'
      }
    }

  }
}