#!/usr/bin/env groovy

pipeline {
  options {
    timeout(time: 4, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '30'))
  }
  agent {
    kubernetes {
        cloud "kubernetes-$environment"
        defaultContainer 'jnlp'
        label "qahaw-$environment"
        yaml """
          apiVersion: v1
          kind: Pod
          metadata:
            annotations:
              iam.amazonaws.com/role: jenkins
          spec:
            serviceAccountName: jenkins-qa
            containers:

            - name: qa-automation-drt-haw
              image: 141380700111.dkr.ecr.us-west-2.amazonaws.com/qa-automation-drt-haw:${params.branch == "master" ? "latest" : params.branch}
              imagePullPolicy: Always
              command:
              - cat
              tty: true
            """
    }
  }

  environment {
    AWS_REGION='us-west-2'
    CREDENTIALS_DEV=credentials('qa-automation-drt-haw-dev')
  }

  stages {
    stage('Run Tests') {
      steps {
                    container('qa-automation-drt-haw') {
                    sh """#!/bin/bash
                    set -uo pipefail
                    echo "AWS_REGION=\$AWS_REGION"
                    echo $environment
                    echo $TESTTYPE
                    echo "Start Execution in "$pwd
                    runner $TESTTYPE $environment $component
        """
      }
      publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'qa_reports', reportFiles: '*.html', reportName: 'HTML Report', reportTitles: ''])
      archiveArtifacts artifacts: 'qa_reports/', fingerprint: true
    }
   }
  }

  post {
		failure {
          slackSend channel: "#team-bumper", color: "danger", message: "COMPONENT: ${COMPONENT}, TESTTYPE: ${TESTTYPE}, JOB: ${JOB_NAME} ${currentBuild.displayName} FAILED: ${BUILD_URL}qa_reports/ in ENV: ${environment}"
        }
        unstable {
          slackSend channel: "#team-bumper", color: "warning", message: "COMPONENT: ${COMPONENT}, TESTTYPE: ${TESTTYPE}, JOB: ${JOB_NAME} ${currentBuild.displayName} UNSTABLE - WITH TEST FAILURE: ${BUILD_URL}qa_reports/ in ENV: ${environment}"
        }
        success {
          slackSend channel: "#team-bumper", color: "good", message: "COMPONENT: ${COMPONENT}, TESTTYPE: ${TESTTYPE}, JOB: ${JOB_NAME} ${currentBuild.displayName} PASSED: ${BUILD_URL}qa_reports/ in ENV: ${environment}"
        }
  }

}
