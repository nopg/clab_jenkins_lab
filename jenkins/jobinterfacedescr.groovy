pipelineJob("description-update") {
  description()
	keepDependencies(false)
    disabled(false)
    parameters {
      stringParam('DEVICE_ID', '')
      stringParam('INTERFACE_ID', '')
      stringParam('INTERFACE_NAME', '')
      stringParam('INTERFACE_DESC', '')
    }
    triggers {
      genericTrigger {
        genericVariables {
          genericVariable {
            key("DEVICE_ID")
            value("\$.data.device.id")
            expressionType("JSONPath")
            regexpFilterText("")
          }
          genericVariable {
            key("INTERFACE_ID")
            value("\$.data.id")
            expressionType("JSONPath")
          }
          genericVariable {
            key("INTERFACE_NAME")
            value("\$.data.name")
            expressionType("JSONPath")
          }
          genericVariable {
            key("INTERFACE_DESC")
            value("\$.data.description")
            expressionType("JSONPath")
          }
          regexpFilterText("")
          regexpFilterExpression("")
        }
        token('cool_token')
        printContributedVariables(true)
        printPostContent(true)
      }
    }

	definition {
		cps {
      sandbox(true)
      script("""pipeline {
    agent any
    stages {
        stage('update some description') {
            steps {
                // run the container on the same clab network so it can resolve vault and the network devices!
                // see dockerfile for more info on why sudo... its a demo, let it slide :)
                sh "sudo docker run --network clab demo-container:latest description_update.py \$DEVICE_ID \$INTERFACE_ID \$INTERFACE_NAME \$INTERFACE_DESC"
            }
        }
    }
    post {
        always {
            echo 'description update complete'
        }
    }
}""")		
        }
	}
}
