pipeline {
  agent any
  stages {
    stage('Lint') {
      parallel {
        stage('Lint') {
          steps {
            sh '''pip3 install black &&
python3 -m black ./payu'''
          }
        }

        stage('Type Check') {
          steps {
            sh 'sh \'pip install mypy && mypy ./payu\''
          }
        }

      }
    }

    stage('Test') {
      steps {
        sh 'sh \'pip install tox && tox\''
      }
    }

  }
}